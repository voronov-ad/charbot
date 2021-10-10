from decouple import config

MANAGER_SCENARIO_WEBHOOK = config(
    "MANAGER_SCENARIO_WEBHOOK",
    cast=lambda x: str(x).strip(),
    default="https://smartapp-code.sberdevices.ru/chatadapter/chatapi/webhook/sber_nlp2/YVQzMyZP:2ba00f91b1388ba5f4ce8f9b4533d23299ee4a67"
)

RESUME_SCENARIO_WEBHOOK = config(
    "RESUME_SCENARIO_WEBHOOK",
    cast=lambda x: str(x).strip(),
    default="https://smartapp-code.sberdevices.ru/chatadapter/chatapi/webhook/sber_nlp2/aDiuLgne:a284b64c225020ceee53f7834eeb909e43891e0f"
)

SCREENING_SCENARIO_WEBHOOK = config(
    "SCREENING_SCENARIO_WEBHOOK",
    cast=lambda x: str(x).strip(),
    default="https://smartapp-code.sberdevices.ru/chatadapter/chatapi/webhook/sber_nlp2/TtqWopAl:518003018d2fd748c329106d5a4f7e2a45970f4a"
)

SUGGEST_PATH = config(
    "SUGGEST_PATH",
    cast=lambda x: str(x).strip(),
    default="http://192.168.1.149:8001/suggest"
)

BACKEND_PATH = config(
    "BACKEND_PATH",
    cast=lambda x: str(x).strip(),
    default="http://localhost:8060"
)

LOGGING_LEVEL = config("LOGGING_LEVEL", cast=lambda x: str(x).strip().upper(), default="INFO")
