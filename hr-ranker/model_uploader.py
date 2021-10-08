"""
    Скрипт обновляет модель раз в N времени
"""
from base.adapters import BackendAdapter
from base.predictor import RankModel, PREDICT_LABEL
from base.cache import FastLRUCache
from decouple import config
from base.schemas import get_dataset
import asyncio
import pandas as pd
from tqdm import tqdm
import sys
import logging

MODEL_CONFIG_PATH = config("MODEL_CONFIG_PATH", default="./configs/ranker_config.yml", cast=str)
ADAPTER_CONFIG_PATH = config("MODEL_CONFIG_PATH", default="./configs/adapter_config.yml", cast=str)
SLEEP_SECONDS = config("SLEEP_SECONDS", default=300, cast=int) # default 5 min
LOG_LEVEL = config("LOG_LEVEL", default="DEBUG", cast=lambda x: str(x).upper())
CACHE_SIZE = config("CACHE_SIZE", default=100000, cast=int)
log = logging.getLogger(__name__)
log.setLevel(LOG_LEVEL)
log.addHandler(logging.StreamHandler(sys.stdout))

cache_vacancies = FastLRUCache(CACHE_SIZE)
cache_resume = FastLRUCache(CACHE_SIZE)
ranker = RankModel.from_yaml(MODEL_CONFIG_PATH)
adapter = BackendAdapter.from_yaml(ADAPTER_CONFIG_PATH)

async def train_model():
    while True:
        log.info(f"Initializing training loop")
        log.info(f"Initializing Collecting feedbacks")
        feedback_list = await adapter.feedback_all()
        log.info(f"Collected {len(feedback_list)} feedbacks")
        train_resume = []
        train_vacancy = []
        train_labels = []
        if len(feedback_list) == 0:
            log.info(f"Application will sleep for {SLEEP_SECONDS} seconds")
            await asyncio.sleep(SLEEP_SECONDS)
            continue
        for feedback in tqdm(feedback_list):
            vac_ids = feedback.get_vacancy_id()
            # vacancy = cache_vacancies.get(vac_ids)
            # if not vacancy:
            #     vacancy = await adapter.vacancy_by_id(vac_ids) or await adapter.hh_vacancy_get(vac_ids)
            #     cache_vacancies[vac_ids] = vacancy
            vacancy = await adapter.vacancy_by_id(vac_ids) or await adapter.hh_vacancy_get(vac_ids)
            if vacancy is None:
                continue
            res_id = feedback.get_resume_id()
            resume = await adapter.resume_by_id(res_id) or await adapter.hh_resume_get(res_id)
            # resume = cache_resume.get(res_id)
            # if not resume:
            #     resume = await adapter.resume_by_id(res_id) or await adapter.hh_resume_get(res_id)
            #     cache_resume[res_id] = resume
            if resume is None:
                continue
            if not feedback.label:
                continue
            train_resume.append(resume)
            train_vacancy.append(vacancy)
            train_labels.append(float(feedback.label))
        log.info(f"Dataset prepared, starting to train model...")
        train_dataset = get_dataset(train_resume, train_vacancy, train_labels)
        print(train_dataset.columns)
        ranker.fit()
        log.info(f"Model trained! Saving")
        ranker.save_file()
        log.info(f"Model Saved")
        log.info(f"Application will sleep for {SLEEP_SECONDS} seconds")
        await asyncio.sleep(SLEEP_SECONDS)


def main():
    log.info(f"Starting application")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(train_model())


if __name__ == '__main__':
    main()
