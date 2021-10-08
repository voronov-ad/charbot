import os
from catboost import CatBoostRegressor
from sklearn.model_selection import train_test_split
from base.api import ResultItem
from pydantic import BaseModel
from base.schemas import Resume, Vacancy, get_dataset
import random
from typing import List, Dict, Any
import yaml
import pandas as pd

PREDICT_LABEL = "label"


class HrAdapter:
    pass


class RankModelConfig(BaseModel):
    model_path: str
    resume_list_size: int = 100
    iterations: int = 10000
    loss: str = "RMSE"
    plot: bool = False
    learning_rate: float = 0.03
    train_size: float = 0.33
    random_state: int = 44

    @classmethod
    def from_yaml(cls, path: str):
        with open(path, "r") as reader:
            return cls(**yaml.safe_load(reader))

class RankModel:
    _model: CatBoostRegressor
    _config: RankModelConfig
    _resume_list: List[Resume]

    def __init__(self, config: RankModelConfig):
        self._config = config
        self._model = CatBoostRegressor(
            iterations=self._config.iterations,
            loss_function=self._config.loss,
            learning_rate=self._config.learning_rate
        )
        self.load_model()
        self._resume_list = []

    def save_resume_cache(self, res_list: List[Resume]):
        self._resume_list = res_list[:self._config.resume_list_size]

    def predict_local(self, vacancy: Vacancy):
        if len(self._resume_list) == 0:
            return []
        return [ResultItem(url=resume.link, score=pred)
                for pred, resume in zip(self.predict(self._resume_list, vacancy), self._resume_list)]

    @classmethod
    def from_yaml(cls, path: str):
        return cls(RankModelConfig.from_yaml(path))

    def load_model(self):
        if os.path.exists(self._config.model_path):
            self._model.load_model(self._config.model_path)

    def predict(self, to_predict: List[Resume], vacancy: Vacancy):
        predict_frame = pd.DataFrame([item.get_features_from_vacancy(vacancy) for item in to_predict])
        return self._model.predict(predict_frame)

    def predict_single(self, resume: Resume, vacancy: Vacancy):
        predict_frame = pd.DataFrame([resume.get_features_from_vacancy(vacancy)])
        return self._model.predict(predict_frame)[0]

    def fit(self, data: pd.DataFrame):
        X_train, X_test, y_train, y_test = train_test_split(
            data[[label for label in train_dataset.columns if label != PREDICT_LABEL]],
            data[PREDICT_LABEL],
            test_size=self._config.train_size,
            random_state=self._config.random_state
        )
        self._model.fit(
            X=X_train,
            y=y_train,
            plot=self._config.plot,
            eval_set=(X_test, y_test)
        )

    def save_file(self):
        self._model.save_model(self._config.model_path)


if __name__ == '__main__':
    conf = RankModelConfig(
        model_path="../model/catboost.cbm"
    )
    ranker = RankModel(config=conf)
    resume_list = Resume.from_json_list("../dataset/resume_list.json")
    vacancy_list = Vacancy.from_json_list("../dataset/vacancy_list.json")
    train_resume = []
    train_vacancy = []
    train_labels = []
    for res in resume_list:
        for vac in vacancy_list:
            train_resume.append(res)
            train_vacancy.append(vac)
            train_labels.append(float(random.randint(0, 1)))
    train_dataset = get_dataset(train_resume, train_vacancy, train_labels)
    ranker.fit(train_dataset)
    print(ranker.predict(train_resume[:1], vacancy=vacancy_list[0]))
    print(ranker.predict_single(train_resume[0], vacancy_list[0]))
    ranker.save_file()
