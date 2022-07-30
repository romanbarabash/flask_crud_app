from environs import Env

env = Env()
env.read_env(verbose=True)

DB_CONNECT = env.str('DB_CONNECT')
POSTGRES_USER = env.str('POSTGRES_USER')
POSTGRES_PASSWORD = env.str('POSTGRES_PASSWORD')
POSTGRES_DB = env.str('POSTGRES_USER')
