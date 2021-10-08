from pydantic import BaseModel
from typing import List
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
