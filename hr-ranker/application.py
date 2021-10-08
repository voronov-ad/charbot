from fastapi import FastAPI
from base.api import RequestSearch, ResponseSearch, RequestSuggest
from base.schemas import Resume, Vacancy
from base.adapters import BackendAdapter
from base.cache import FastLRUCache
from base.predictor import RankModel
from decouple import config
from uvicorn import run as uv_run
from tqdm import tqdm


MODEL_CONFIG_PATH = config("MODEL_CONFIG_PATH", default="./configs/ranker_config.yml", cast=str)
ADAPTER_CONFIG_PATH = config("MODEL_CONFIG_PATH", default="./configs/adapter_config.yml", cast=str)
MODEL_ENDPOINT = config("MODEL_ENDPOINT", default="/rank", cast=str)
SUGGEST_ENDPOINT = config("SUGGEST_ENDPOINT", default="/suggest", cast=str)
CACHE_SIZE = config("CACHE_SIZE", default=1000, cast=int)
HOST = config("HOST", default="0.0.0.0", cast=str)
PORT = config("PORT", default=8001, cast=int)
LOG_LEVEL = config("LOG_LEVEL", default="trace", cast=lambda x: str(x).lower())
WORKERS = config("WORKERS", default=1, cast=int)

app = FastAPI()

vacancy_cache = FastLRUCache(max_size=CACHE_SIZE)
ranker = RankModel.from_yaml(MODEL_CONFIG_PATH)
adapter = BackendAdapter.from_yaml(ADAPTER_CONFIG_PATH)


@app.on_event("startup")
async def prepare_adapter():
    load_ids = await adapter.resume_all()
    ranker.save_resume_cache([await adapter.resume_by_id(ids) or
                              await adapter.hh_resume_get(ids) for ids in tqdm(load_ids)])


@app.post(SUGGEST_ENDPOINT)
async def suggest(request: RequestSuggest):
    link = Vacancy.get_new_link()
    vacancy = Vacancy(**{
        "companyName": Vacancy.get_default_company_name(),
        "employeeMode": request.schedule,
        "experience": request.experience,
        "link": link,
        "salary": f"{request.salary_from} {request.salary_to}",
        "tags": request.skills,
        "title": request.title,
        "description": request.comment,
        "company": {
            "city": request.city,
            "area": request.skills,
            "description": request.comment,
            "name": Vacancy.get_default_company_name()
        }
    })
    return ResponseSearch(result=ranker.predict_local(vacancy), vacancy=vacancy.link)


@app.post(MODEL_ENDPOINT)
async def rank(request: RequestSearch) -> ResponseSearch:
    try:
        vacancy = vacancy_cache[request.get_id()]
        print("GOT FROM CACHE")
    except KeyError:
        vacancy = await adapter.vacancy_by_id(request.get_id()) or await adapter.hh_vacancy_get(request.get_id())
        vacancy_cache[request.get_id()] = vacancy
    return ResponseSearch(result=ranker.predict_local(vacancy), vacancy=vacancy.link)


if __name__ == '__main__':
    params = dict()
    params["host"] = HOST
    params["port"] = PORT
    params["log_level"] = LOG_LEVEL  # <- <str> - the Logger level, should be in lower case!
    params["workers"] = WORKERS
    uv_run("application:app", **params)
