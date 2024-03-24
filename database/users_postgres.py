import psycopg
from cachetools import cached, TTLCache
from config_data.config import load_config

USERS_CONFIG = 'users_config'

config = load_config()
cache = TTLCache(maxsize=100, ttl=300)


def get_connection_str() -> str:
    return (f'dbname={config.db.database} '
            f'user={config.db.db_user} '
            f'password={config.db.db_password} '
            f'host={config.db.db_host}')


def create_table():
    with psycopg.connect(get_connection_str()) as conn:
        with conn.cursor() as cur:
            cur.execute(f'''create table if not exists {USERS_CONFIG} (
                            id serial primary key,
                            hashed_user_id text unique,
                            src_lang text,
                            dest_lang text
                          )''')
            conn.commit()


@cached(cache=cache)
def load_users_config():
    create_table()
    users_config = {}
    with psycopg.connect(get_connection_str()) as conn:
        with conn.cursor() as cur:
            cur.execute(f'select hashed_user_id, src_lang, dest_lang from {USERS_CONFIG}')
            rows = cur.fetchall()
            for row in rows:
                hashed_user_id, src_lang, dest_lang = row
                users_config[str(hashed_user_id)] = {'src_lang': src_lang, 'dest_lang': dest_lang}
    return users_config


def save_users_config(users_config):
    create_table()
    with psycopg.connect(get_connection_str()) as conn:
        with conn.cursor() as cur:
            try:
                conn.autocommit = False
                for hashed_user_id, config in users_config.items():
                    src_lang = config['src_lang']
                    dest_lang = config['dest_lang']
                    cur.execute(f'''
                    insert into {USERS_CONFIG} (hashed_user_id, src_lang, dest_lang)
                    values (%s, %s, %s)
                    on conflict (hashed_user_id) do update
                    set src_lang = excluded.src_lang, dest_lang = excluded.dest_lang
                            ''', (hashed_user_id, src_lang, dest_lang))
                conn.commit()
            except psycopg.Error as e:
                print('Error:', e)
                conn.rollback()