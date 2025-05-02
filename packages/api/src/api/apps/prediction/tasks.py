import os

from celery import shared_task

from api.apps.prediction.predictor import ModelPredictor


@shared_task()  # type: ignore[misc]
def predict_task(file_path: str, model_name: str) -> dict[str, str]:
    try:
        predictor = ModelPredictor(model_name=model_name)
        predicted_file_path = predictor.predict_from_csv(file_path=file_path)
    finally:
        os.remove(file_path)

    return {"file_path": predicted_file_path, "file_name": f"{model_name}_prediction.csv"}
