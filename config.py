from dataclasses import dataclass
from environs import Env

log_level = 'WARNING'   # установка общего уровня логирования

@dataclass
class Config:
    username: str
    password: str


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    cfg = Config(env.str("STEPIK_USERNAME"), env.str("STEPIK_PASSWORD"))
    return cfg


if __name__ == '__main__':
    cfg = load_config()
    print(cfg)

