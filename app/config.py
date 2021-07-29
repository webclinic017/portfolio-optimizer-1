from environs import Env

env = Env()
env.read_env()


class Config:
    alpha_vantage_key = env.str("ALPHA_VANTAGE_KEY")
