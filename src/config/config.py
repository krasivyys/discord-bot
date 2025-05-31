from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

class Settings(BaseSettings):
    DISCORD_TOKEN: str
    VK_TOKEN: str
    VK_GROUP_ID: int
    DB_HOST: str
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_PORT: int = 3306
    SERVER_ID: int
    MUTED_ROLE_ID: int
    PRISON_ROLE_ID: int
    
    CHANNELS: dict = {
        "VOICE": 1070794259516637195,
        "INFO": 942497494053564496,
        "CAPTURE": 1010984029148958741,
        "REPORTS": 942397029101998087
    }
    
    ROLES: dict = {
        "MAFIA_MEMBER": 942397028770656260,
        "GHETTO_MEMBER": 942515120679043122,
        "YAKUZA": 942397028770656261,
        "WARLOCK": 942397028770656262,
        "LCN": 942397028770656264,
        "RUSSIAN": 942397028770656263,
        "GROVE": 942515302518898688,
        "VAGOS": 942515470513369099,
        "BALLAS": 942515516453552168,
        "NW": 942515628122701854,
        "AZTEC": 942515673932922950,
        "RIFA": 942515575337390090
    }
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings() 