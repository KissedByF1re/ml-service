import pathlib
import tempfile

import pandas as pd
import pickle

path = pathlib.Path(__file__).parent

MODEL_NAME_TO_MODEL_PATH = {
    "catboost": path / "models" / "catboost.pkl",
    "logistic_regression": path / "models" / "logistic_regression.pkl",
    "random_forest": path / "models" / "random_forest.pkl",
    "svm": path / "models" / "svm.pkl",
}


class ModelPredictor:
    def __init__(self, model_name: str) -> None:
        model_path = MODEL_NAME_TO_MODEL_PATH[model_name]
        with open(model_path, "rb") as f:
            self.model = pickle.load(f)

    def predict_from_csv(self, file_path: str) -> str:
        df = pd.read_csv(file_path)
        predictions = self.model.predict(df)
        df["Churn"] = predictions

        _, temp_file_path = tempfile.mkstemp()
        df.to_csv(temp_file_path, index=False)

        return temp_file_path
