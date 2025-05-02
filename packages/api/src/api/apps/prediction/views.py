import os
import tempfile
import typing

from celery.result import AsyncResult
from django.http import FileResponse
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from api.apps.billing.models import ServiceOrder
from api.apps.prediction.tasks import predict_task


class PredictionAPIView(GenericAPIView):  # type: ignore[type-arg]
    parser_classes = [MultiPartParser]
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="service_order_id",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                required=True,
            ),
        ],
        request={
            "multipart/form-data": {
                "type": "object",
                "properties": {"file": {"type": "string", "format": "binary"}},
                "required": ["file"],
            }
        },
        responses={
            200: {
                "type": "object",
                "properties": {
                    "task_id": {"type": "string"},
                },
            }
        },
    )
    def post(self, request: Request, *args: typing.Any, **kwargs: typing.Any) -> Response:
        file_obj = request.FILES.get("file")
        service_order_id = request.GET["service_order_id"]
        service_order_query = ServiceOrder.objects.select_related("user", "service").filter(id=service_order_id)
        service_order = service_order_query.first()
        if not service_order:
            return Response(data={"error": "Service order is not found"}, status=status.HTTP_404_NOT_FOUND)
        if service_order.user_id != request.user.id:
            return Response(
                data={"error": "Service order does not belong to current user"}, status=status.HTTP_403_FORBIDDEN
            )
        if service_order.is_provided:
            return Response(data={"error": "Service is already provided"}, status=status.HTTP_400_BAD_REQUEST)
        model_name = service_order.service.model

        _, temp_file_path = tempfile.mkstemp()
        with open(temp_file_path, "wb") as temp_file:
            for chunk in file_obj.chunks():
                temp_file.write(chunk)

        task: AsyncResult = predict_task.s(file_path=temp_file_path, model_name=model_name).apply_async()
        service_order.is_provided = True
        service_order.save()
        return Response(data={"task_id": task.task_id})

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="task_id",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                required=True,
            ),
        ],
        responses={
            200: {
                "type": "object",
                "properties": {
                    "status": {"type": "string"},
                    "result": {"type": "string"},
                },
            }
        },
    )
    def get(self, request: Request, *args: typing.Any, **kwargs: typing.Any) -> Response | FileResponse:
        task_id = request.GET.get("task_id")
        task = AsyncResult(id=task_id)

        if task.state == "SUCCESS":
            task_result = task.result
            if os.path.exists(task_result["file_path"]):
                file_data = open(task_result["file_path"], "rb")
                os.remove(task_result["file_path"])
                return FileResponse(
                    file_data,
                    as_attachment=True,
                    filename=task_result["file_name"],
                )
            return Response(data={"status": "SUCCESS", "result": "File not found."})
        else:
            return Response(data={"status": task.state, "result": None})
