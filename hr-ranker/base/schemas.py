from pydantic import BaseModel
from typing import Optional, List, Union
from stop_words import get_stop_words
import difflib
from nltk.stem.snowball import SnowballStemmer
from pymystem3 import Mystem
import numpy as np
import orjson
import re
import pandas as pd
from tqdm import tqdm

STOP_WORDS = list(get_stop_words("russian"))
MAX_ROUNDING = 10
STEMMER = SnowballStemmer("russian")
MYSTEM = Mystem()

NO_SALARY = "з/п не указана"

XA_STRING = "\xa0"
DEFAULT_AGE = 18
DEFAULT_EXP_YEARS = 0
DEFAULT_SALARY_SCORE = 0.5

ENGLISH_LABEL = "Английский"
LANGUAGE_LEVELS = {
    'A1': 0.,
    'A2': 0.2,
    'B1': 0.4,
    'B2': 0.6,
    'C1': 0.8,
    'C2': 1.0,
    'Родной': 1.0
}

RESUME_EXAMPLE = {
    "name": "",
    "age": "34 года",
    "date_of_birth": "1 мая 1987",
    "address": "Москва",
    "metro": "",
    "position": "Руководитель отдела информационной безопасности / Архитектор ИБ",
    "salary": "270 000 руб.",
    "specialization": [
        "компьютерная безопасность"
    ],
    "specialization_category": "Информационные технологии, интернет, телеком",
    "exprerience": "Опыт работы 12 лет 7 месяцев",
    "last_work": "Начальник отдела анализа программного кода",
    "work_place_count": "7",
    "skills": [
        "Аудит безопасности",
        "Информационная безопасность",
        "Внедрение систем информационной безопасности",
        "Технические средства информационной защиты",
        "Проектирование",
        "Внутренний аудит информационных систем",
        "sdlc",
        "анализ программного кода",
        "тестирование на проникновение",
        "анализ защищенности приложений",
        "Linux",
        "TCP/IP",
        "OWASP",
        "Этичный хакинг"
    ],
    "has_education": True,
    "languages": [
        "Русский — Родной",
        "Английский — B2 — Средне-продвинутый"
    ],
    "link": "https://hh.ru/resume/907708b30003b732df00000dc95054394c3039"
}


def flatten(t):
    return [item for sublist in t for item in sublist]


def clean_stopwords(string: str = ""):
    words = re.sub('^[^0-9a-zA-ZА-Яа-я ]+', '', string.lower()).split(" ")
    return [MYSTEM.lemmatize(word)[0] for word in words if word not in STOP_WORDS]


def words_diff(one: str, two: str, rounding: int = MAX_ROUNDING):
    return round(difflib.SequenceMatcher(
        None,
        re.sub(r'\W+', '', one.lower()),
        re.sub(r'\W+', '', two.lower())).ratio(),
                 rounding)


class Model(BaseModel):
    @classmethod
    def from_json(cls, path: str):
        with open(path, "r") as reader:
            return cls(**orjson.loads(reader.read()))

    @classmethod
    def from_json_list(cls, path: str):
        with open(path, "r") as reader:
            return [cls(**inst) for inst in orjson.loads(reader.read())]

    @classmethod
    def from_list_dict(cls, data: List[dict]):
        return [cls(**item) for item in data if item is not None]


class Vacancy(Model):
    companyName: str
    employeeMode: str
    experience: str
    link: str
    salary: str
    tags: List[str]
    title: str
    description: str

    def get_min_salary(self):
        match = re.search(r'от\s?[\xa0]?\d{1,4}\s?[\u202f]?\d{1,4}', self.salary)
        if not match:
            return -1
        return int(re.sub(r"\D+", "", match[0]))

    def get_max_salary(self):
        match = re.search(r'до\s?[\xa0]?\d{1,4}\s?[\u202f]?\d{1,4}', self.salary)
        if not match:
            return -1
        return int(re.sub(r"\D+", "", match[0]))

    def get_low_experience(self):
        match = re.search(r'\d.', self.experience)
        if not match:
            return -1
        return int(re.sub(r"\D+", "", match[0]))

    def get_high_experience(self):
        match = re.search(r'.\d', self.experience)
        if not match:
            return -1
        return int(re.sub(r"\D+", "", match[0]))

    def get_company_popularity(self):
        pass


class Resume(Model):
    link: str
    position: str
    exprerience: str
    last_work: str
    work_place_count: str
    has_education: bool
    skills: List[str]
    salary: Optional[str]
    specialization: Optional[Union[List[str], str]]
    specialization_category: Optional[str]
    name: Optional[str]
    age: Optional[str]
    date_of_birth: Optional[str]
    address: Optional[str]
    metro: Optional[str]
    languages: Optional[List[str]]

    def get_age(self):
        parsed = re.search(r'\d{2}', self.age)
        if parsed:
            return int(parsed[0])
        else:
            return DEFAULT_AGE

    def get_exprerience_years(self):
        years = re.search(r'работы\s?\d{1,2}[\xa0]?\s?лет', self.exprerience)
        if years is None:
            return DEFAULT_EXP_YEARS
        years = float(re.sub(r'[^A-Za-z0-9]+', '', years[0]))
        months = re.search(r'лет\s?\d{1,2}[\xa0]?\s?месяцев', self.exprerience)
        if months is not None:
            months = int(re.sub(r'[^A-Za-z0-9]+', '', months[0]))
            return years + round(months / 12, 2)
        return years

    def know_english(self) -> float:
        if self.languages is None:
            return 0
        for education in self.languages:
            if ENGLISH_LABEL not in education:
                continue
            for key, value in LANGUAGE_LEVELS.items():
                if key in education:
                    return value
        return 0.0

    def get_education(self):
        if self.has_education:
            return 1
        else:
            return 0

    def get_last_work_similarity(self, work_title: str):
        return words_diff(self.last_work, work_title)

    def get_last_work_words(self):
        return clean_stopwords(self.last_work)

    def get_salary_diff(self, vacancy_salary: Union) -> float:
        if not self.salary:
            return DEFAULT_SALARY_SCORE
        return vacancy_salary / int(re.sub(r'\D+', '', self.salary))

    def get_skills_match_score(self, vacancy_skills: List[str], rounding: int = MAX_ROUNDING):
        if self.skills is None or len(self.skills) == 0:
            return 0
        scores = []
        for vac_skill in vacancy_skills:
            scores.append(np.max([words_diff(vac_skill, skill) for skill in self.skills]))
        return round(np.mean(scores), rounding)

    def get_last_work_count(self):
        return int(self.work_place_count)

    def get_work_experience_score(self, rounding: int = MAX_ROUNDING) -> float:
        if self.get_last_work_count() == 0:
            return -1.0
        return round(self.get_exprerience_years() / self.get_last_work_count(), rounding)

    def get_work_experience_score_over_ages(self, rounding: int = MAX_ROUNDING):
        return round(
            self.get_work_experience_score(rounding=rounding) * self.get_exprerience_years() / self.get_age(),
            rounding)

    def get_specialization_match(self, vac_specialization: str):
        if not self.specialization:
            return -1
        if isinstance(self.specialization, str):
            self.specialization = [self.specialization]
        vac_words = clean_stopwords(vac_specialization)
        self_spec_words = flatten([clean_stopwords(x) for x in self.specialization])
        if not vac_words or not self_spec_words:
            return -1
        return np.mean(
            [np.max([words_diff(vac_word, word) for word in self_spec_words]) for vac_word in
             vac_words])

    def get_features_from_vacancy(self, vacancy: Vacancy):
        return {
            "age": self.get_age(),
            "exprerience_years": self.get_exprerience_years(),
            "know_english": self.know_english(),
            "education": self.get_education(),
            "last_work_similarity": self.get_last_work_similarity(vacancy.title),
            "min_salary_diff": self.get_salary_diff(vacancy.get_min_salary()),
            "max_salary_diff": self.get_salary_diff(vacancy.get_max_salary()),
            "skills_match": self.get_skills_match_score(vacancy.tags),
            "last_work_count": self.get_last_work_count(),
            "work_experience_score": self.get_work_experience_score(),
            "aged_work_experience_score": self.get_work_experience_score_over_ages(),
            "title_specialization_match_score": self.get_specialization_match(vacancy.title)
        }


def get_dataset(resume_list: List[Resume], vacancy_list: List[Vacancy], labels: List[Union[bool, int, float]]):
    assert len(resume_list) == len(vacancy_list) == len(labels)
    dataset = []
    for resume, vacancy, label in tqdm(zip(resume_list, vacancy_list, labels)):
        data_item = resume.get_features_from_vacancy(vacancy)
        data_item["label"] = label
        dataset.append(data_item)
    return pd.DataFrame(dataset)


if __name__ == '__main__':
    import random
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
