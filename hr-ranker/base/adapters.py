from aiohttp import ClientSession
from pydantic import BaseModel
from typing import Union
from base.schemas import Resume, Vacancy
from asyncio import BoundedSemaphore
import yaml


class BackendAdapterConfig(BaseModel):
    address: str
    bound: int = 40


class BackendAdapter:
    _client: ClientSession
    _sema: BoundedSemaphore
    _config: BackendAdapterConfig

    VACANCY_BY_ID = "http://{address}:8060/api/v1/vacancy/{id}"
    VACANCY_SEARCH = "http://{address}:8090/resume-search"
    VACANCY_GET = "http://{address}:8070/vacancy"
    VACANCY_ALL = "http://{address}:8060//api/v1/vacancy"
    VACANCY2RESUME = "http://{address}:8060/api/related-vacancy?id={id}"
    FEEDBACK_SEND = "http://{address}:8060/feedback"
    RESUME_SEARCH = "http://{address}:8090/resume-search"
    RESUME_GET = "http://{address}:8090/resume"
    RESUME_ALL = "http://{address}:8060/api/v1/resume"
    RESUME_BY_ID = "http://{address}:8060/api/v1/resume/{id}"

    def __init__(self, config: BackendAdapterConfig):
        self._config = config
        self._client = ClientSession()
        self._sema = BoundedSemaphore(self._config.bound)

    async def close_session(self):
        await self._client.close()

    @classmethod
    def from_yaml(cls, path: str):
        with open(path, "r") as reader:
            return cls(BackendAdapterConfig(**yaml.safe_load(reader)))

    async def hh_resume_search(self, title: str):
        async with self._client.post(
                url=self.RESUME_SEARCH.format(address=self._config.address), json={"title": title},
                ssl=False) as resp:
            if resp.status == 200:
                return [Resume(**resp_item) for resp_item in await resp.json()]

    async def hh_resume_get(self, ids: str):
        async with self._client.post(
                url=self.RESUME_GET.format(address=self._config.address), json={"id": ids},
                ssl=False) as resp:
            if resp.status == 200:
                return Resume(**await resp.json())

    async def hh_vacancy_get(self, ids: str):
        async with self._client.post(
                url=self.VACANCY_GET.format(address=self._config.address), json={"id": ids},
                ssl=False) as resp:
            if resp.status == 200:
                return Vacancy(**await resp.json())

    async def hh_vacancy_to_resume(self, ids: str):
        async with self._client.get(
                url=self.FEEDBACK_SEND.format(address=self._config.address, id=ids), ssl=False) as resp:
            if resp.status == 200:
                return Resume(**await resp.json())

    async def feedback_post(self, vacancy_url: str, resume_ids: str, label: Union[int, float, bool]):
        async with self._client.post(
                url=self.FEEDBACK_SEND.format(address=self._config.address),
                json={"url_vacancy": vacancy_url, "url_candidate": resume_ids, "label": label},
                ssl=False) as resp:
            if resp.status == 200:
                return True

    async def vacancy_all(self):
        async with self._client.get(
                url=self.VACANCY_ALL.format(address=self._config.address), ssl=False) as resp:
            if resp.status == 200:
                return await resp.json()

    async def resume_all(self):
        async with self._client.get(
                url=self.RESUME_ALL.format(address=self._config.address), ssl=False) as resp:
            if resp.status == 200:
                return await resp.json()

    async def vacancy_by_id(self, ids: str):
        async with self._client.get(
                url=self.VACANCY_BY_ID.format(address=self._config.address, id=ids), ssl=False) as resp:
            if resp.status == 200:
                return Vacancy(**await resp.json())
            else:
                return None

    async def resume_by_id(self, ids: str):
        async with self._client.get(
                url=self.RESUME_BY_ID.format(address=self._config.address, id=ids), ssl=False) as resp:
            if resp.status == 200:
                return Resume(**await resp.json())
