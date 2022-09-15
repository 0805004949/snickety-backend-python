from dataclasses import dataclass
import platform
from os import environ


@dataclass
class Global:
    secret_name = "dev/app/mysql"
    region_name = "ap-northeast-2"


@dataclass
class Prod(Global):
    env_state = "prod"


@dataclass
class Dev(Global):
    env_state = "dev"


@dataclass
class Local(Global):
    env_state = "local"


class FactorySettings:
    @staticmethod
    def load():
        config = dict(prod=Prod, local=Local, dev=Dev)
        env_state = environ.get("ENV_STATE", "local")  # default로 로컬
        return config[env_state if env_state else "local"]()


settings = FactorySettings.load()
