import logging

import psycopg
from cachetools import TTLCache, cached

from database.db import Database

USERS_CONFIG = 'users_config'

cache = TTLCache(maxsize=100, ttl=300)


def update_cached_users_config():
    cache.clear()


@cached(cache=cache)
def load_users_config():
    database = Database()
    conn = database.get_connection()
    users_config = {}
    try:
        with conn.cursor() as cur:
            cur.execute(f'select hashed_user_id, src_lang, dest_lang from {USERS_CONFIG}')
            rows = cur.fetchall()
            for row in rows:
                hashed_user_id, src_lang, dest_lang = row
                users_config[str(hashed_user_id)] = {'src_lang': src_lang, 'dest_lang': dest_lang}
    except psycopg.Error as e:
        logging.error(f"Error loading users config: {e}.")
    return users_config


def save_users_config(users_config):
    database = Database()
    conn = database.get_connection()
    with conn.cursor() as cur:
        try:
            for hashed_user_id, config in users_config.items():
                src_lang = config['src_lang']
                dest_lang = config['dest_lang']
                cur.execute(f'''
                    insert into {USERS_CONFIG} (hashed_user_id, src_lang, dest_lang)
                    values (%s, %s, %s)
                    on conflict (hashed_user_id) do update
                    set src_lang = excluded.src_lang, dest_lang = excluded.dest_lang
                            ''', (hashed_user_id, src_lang, dest_lang))
            update_cached_users_config()
        except psycopg.Error as e:
            logging.error(f"Error saving users config: {e}.")
            conn.rollback()
