import pytest
from base.schemas import Resume, DEFAULT_AGE, Vacancy
import logging


class TestResumeModel:
    TEST_OBJECT = {
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

    def test_init(self):
        resume = Resume(**self.TEST_OBJECT)
        assert resume.dict() == self.TEST_OBJECT

    def test_get_age(self):
        resume = Resume(**self.TEST_OBJECT)
        assert resume.get_age() == 34
        resume.age = 'nothind'
        assert resume.get_age() == DEFAULT_AGE

    def test_get_exprerience_years(self):
        resume = Resume(**self.TEST_OBJECT)
        assert resume.get_exprerience_years() == 12.58
        resume.exprerience = 'Опыт работы 12\xa0лет'
        assert resume.get_exprerience_years() == 12.0

    def test_has_education(self):
        resume = Resume(**self.TEST_OBJECT)
        assert resume.get_education() == 1
        resume.has_education = False
        assert resume.get_education() == 0

    def test_know_english(self):
        resume = Resume(**self.TEST_OBJECT)
        assert resume.know_english() == 0.6
        resume.languages = ['random', 'random']
        assert resume.know_english() == 0.0
        resume.languages = ['random', 'Английский']
        assert resume.know_english() == 0.0
        resume.languages = ['random', 'Английский — C2 — Средне-продвинутый']
        assert resume.know_english() == 1.0
        resume.languages = ['random', 'Английский — C1 — Средне-продвинутый']
        assert resume.know_english() == 0.8
        resume.languages = ['random', 'Английский — B1 — Средне-продвинутый']
        assert resume.know_english() == 0.4
        resume.languages = ['random', 'Английский — A2 — Средне-продвинутый']
        assert resume.know_english() == 0.2
        resume.languages = ['random', 'Английский — A1 — Средне-продвинутый']
        assert resume.know_english() == 0.0
        resume.languages = ['random', 'Английский — Родной']
        assert resume.know_english() == 1.0
        resume.languages = ['random', 'Русский — Родной']
        assert resume.know_english() == 0.0

    def test_get_last_work_similarity(self):
        resume = Resume(**self.TEST_OBJECT)
        assert resume.get_last_work_similarity(resume.last_work) == 1

    def test_last_work_words(self):
        resume = Resume(**self.TEST_OBJECT)
        words = resume.get_last_work_words()
        assert all([x in words for x in ['начальник', 'отдел', 'анализ', 'программный', 'код']])

    def test_get_salary_diff(self):
        resume = Resume(**self.TEST_OBJECT)
        assert resume.get_salary_diff(270000) == 1

    def test_get_skills_match_score(self):
        resume = Resume(**self.TEST_OBJECT)
        assert resume.get_skills_match_score(
            ["NGINX", "Системный анализ", "проектирование интерфейсов", "Linux", "хакинг"],
            2) == 0.68

    def test_get_last_work_count(self):
        resume = Resume(**self.TEST_OBJECT)
        assert resume.get_last_work_count() == 7

    def test_get_work_experience_score(self):
        resume = Resume(**self.TEST_OBJECT)
        assert resume.get_work_experience_score(3) == 1.797

    def test_get_work_experience_score_over_ages(self):
        resume = Resume(**self.TEST_OBJECT)
        assert resume.get_work_experience_score_over_ages(3) == 0.665

    def test_get_specialization_match(self):
        resume = Resume(**self.TEST_OBJECT)
        assert resume.get_specialization_match("компьютерная безопасность")


class TestVacancyModel:
    TEST_OBJECT = {
        "companyName": "HR Prime",
        "description": "Требуемый опыт работы: 1–3 годаПолная занятость, полный деньВ крупную IT-компанию требуется Middle/Senior Java разработчик.    Один клик - шаг к мечте 😉     Требования:   Отличное знание Java, версия 8 и выше.   Опыт использования Spring, Spring Boot и Hibernate (от 1 года).   Опыт промышленной командной разработки (от 3-х лет).   Знание SQL и опыт работы с одной из промышленных СУБД – PostgreSQL, Oracle, MS SQL, etc.   Опыт работы с одной из интеграционных платформ обмена сообщениями – Kafka, Rabbit MQ, IBM WebSphere MQ, etc.   Условия:   Возможность присоединиться к очень молодой и быстрорастущей команде in-house разработки одного из крупнейших банков России;   Амбициозные интересные проекты;   Достойный уровень дохода + премии;   Добровольное медицинское страхование.        Ключевые навыкиJavaSpring FrameworkSQLHibernate ORMPostgreSQL",
        "employeeMode": "Полная занятость, полный день",
        "experience": "1–3 года",
        "link": "https://hh.ru/vacancy/48565881",
        "salary": "от 300 000 до 525 000 руб. до вычета налогов",
        "tags": [
            "Java",
            "Spring Framework",
            "SQL",
            "Hibernate ORM",
            "PostgreSQL"
        ],
        "title": "Java разработчик"
    }

    def test_init(self):
        vacancy = Vacancy(**self.TEST_OBJECT)
        assert vacancy.dict() == self.TEST_OBJECT

    def test_get_min_salary(self):
        vacancy = Vacancy(**self.TEST_OBJECT)
        assert vacancy.get_min_salary() == 300000

    def test_get_max_salary(self):
        vacancy = Vacancy(**self.TEST_OBJECT)
        assert vacancy.get_max_salary() == 525000

    def get_low_experience(self):
        vacancy = Vacancy(**self.TEST_OBJECT)
        assert vacancy.get_low_experience() == 1

    def test_get_high_experience(self):
        vacancy = Vacancy(**self.TEST_OBJECT)
        assert vacancy.get_high_experience() == 3
