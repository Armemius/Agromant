from dotenv import load_dotenv
import os

if os.path.exists(".env"):
    load_dotenv(".env")


def get_value(key: str, mandatory: bool = False) -> str:
    value = os.getenv(key)
    if value is None and mandatory:
        raise ValueError(f"Environment variable {key} is not set")
    return value


def get_flag(key: str, default: bool = False) -> bool:
    value = os.getenv(key)
    if value is None:
        return default
    return value.lower() in ("1", "true", "yes")


class Config:
    def __init__(self):
        self.bot_key = get_value("TG_BOT_API_KEY", mandatory=True)
        self.proxyai_api = get_value("PROXY_AI_API_KEY", mandatory=True)
        self.use_webhooks = get_flag("USE_BOT_WEBHOOKS", default=False)
        self.webhook_url = get_value("WEBHOOK_URL", mandatory=self.use_webhooks)
        self.webhook_path = get_value("WEBHOOK_PATH", mandatory=self.use_webhooks)
        self.webhook_connections = int(get_value("WEBHOOK_CONNECTIONS", mandatory=self.use_webhooks) or 10)
        self.webhook_port = int(get_value("WEBHOOK_PORT", mandatory=self.use_webhooks) or 8443)
        self.mongo_host = get_value("MONGO_HOST") or "localhost"
        self.mongo_port = int(get_value("MONGO_PORT") or 27017)
        self.mongo_username = get_value("MONGO_ROOT_USERNAME", mandatory=True)
        self.mongo_password = get_value("MONGO_ROOT_PASSWORD", mandatory=True)
        self.mongo_database = get_value("MONGO_DATABASE", mandatory=True)
        self.yookassa_shop_id = get_value("YOOKASSA_SHOP_ID", mandatory=True)
        self.yookassa_secret_key = get_value("YOOKASSA_SECRET_KEY", mandatory=True)


def init_config():
    global bot_config


bot_config = Config()
