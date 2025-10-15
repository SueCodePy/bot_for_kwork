from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
import json
# для указания пути к .env. без этого конфиг не работал/ тфк же если .env находится в той же папке что и config  то прописываем путь Path(__file__).resolve().parent если config глубже env то прописываем Path(__file__).resolve().parent.parent
BASE_DIR = Path(__file__).resolve().parent.parent # .../PythonProject1
ENV_FILE = BASE_DIR / ".env"

class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    BOT: str
    HEADERS: str
    COOKIES: str
    model_config = SettingsConfigDict(env_file=str(ENV_FILE), env_file_encoding="utf-8")

    @property
    def headers(self) -> dict:
        """Возвращает headers как словарь."""
        return json.loads(self.HEADERS)

    @property
    def cookies(self) -> dict:
        """Возвращает cookies как словарь."""
        return json.loads(self.COOKIES)

settings = Settings()


print(settings.COOKIES)