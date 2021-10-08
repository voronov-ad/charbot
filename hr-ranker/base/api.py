from pydantic import BaseModel
from typing import List, Optional, Union
from base.mocks import RESPONSE_MOCK
import re


class RequestSearch(BaseModel):
    vacancy_url: str

    def get_id(self,):
        return re.sub(r'https://hh.ru/vacancy/', '', self.vacancy_url)


class ResultItem(BaseModel):
    url: str
    score: float


class ResponseSearch(BaseModel):
    result: List[ResultItem]
    vacancy: Optional[str]

    @classmethod
    def get_mock(cls):
        return cls(**RESPONSE_MOCK)


class RequestSuggest(BaseModel):
    title: str
    experience: Optional[str]
    skills: Optional[List[str]]
    level: Optional[str]
    city: Optional[str]
    schedule: Optional[str]
    salary_from: Optional[Union[str, int, float]]
    salary_to: Optional[Union[str, int, float]]
    companies: Optional[List[str]]
    education: Optional[str]
    comment: Optional[str]