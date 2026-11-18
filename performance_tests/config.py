import locust.stats
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

# Импортируем вложенные модели
from performance_tests.tools.config.grpc import GRPCClientConfig
from performance_tests.tools.config.http import HTTPClientConfig
from performance_tests.tools.config.locust import LocustUserConfig

env_file = Path(__file__).parent.parent / '.env.local'

# Настройка списка процентилей, которые будут попадать в отчёты Locust
locust.stats.PERCENTILES_TO_REPORT = [0.50, 0.60, 0.70, 0.80, 0.90, 0.95, 0.99, 1.0]

# Интервал (в секундах) между записями агрегированной статистики в CSV
locust.stats.CSV_STATS_INTERVAL_SEC = 5

# Интервал (в секундах) между записями "исторической" статистики (динамика значений)
locust.stats.HISTORY_STATS_INTERVAL_SEC = 5

# Интервал (в секундах) между обновлением статистики в консоли Locust
locust.stats.CONSOLE_STATS_INTERVAL_SEC = 5

# Интервал (в секундах) между принудительной записью CSV на диск
locust.stats.CSV_STATS_FLUSH_INTERVAL_SEC = 5


class Settings(BaseSettings):
    # Конфигурация загрузки — откуда брать переменные
    model_config = SettingsConfigDict(
        extra="allow",  # Разрешить дополнительные поля (например, неиспользуемые переменные)
        env_file=env_file,  # Указываем имя и путь до локального .env файла .env.local
        env_file_encoding="utf-8",  # Кодировка файла
        env_nested_delimiter="."  # Позволяет использовать вложенные переменные, например: LOCUST_USER.WAIT_TIME_MIN
    )

    # Вложенные секции настроек
    locust_user: LocustUserConfig  # Настройки виртуального пользователя
    gateway_http_client: HTTPClientConfig  # Настройки HTTP-клиента
    gateway_grpc_client: GRPCClientConfig  # Настройки gRPC-клиента


# Глобальный объект настроек — его можно импортировать в любом месте проекта
settings = Settings()
