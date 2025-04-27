import os
import tempfile
import typing

from celery.result import AsyncResult
from django.http import FileResponse
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.request import Request
from rest_framework.response import Response

from api.apps.prediction.tasks import predict_task


class PredictionAPIView(GenericAPIView):  # type: ignore[type-arg]
    parser_classes = [MultiPartParser]

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="model_name",
                type=OpenApiTypes.STR,
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
        model_name = request.GET.get("model_name")

        _, temp_file_path = tempfile.mkstemp()
        with open(temp_file_path, "wb") as temp_file:
            for chunk in file_obj.chunks():
                temp_file.write(chunk)

        task: AsyncResult = predict_task.s(file_path=temp_file_path, model_name=model_name).apply_async()
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
