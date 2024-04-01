import logging
import psycopg
from database.db import Database

STATS = 'stats_data'


def save_stats(users_config):
    database = Database()
    conn = database.get_connection()
    try:
        with conn.cursor() as cur:
            for hashed_user_id, config in users_config.items():
                src_lang = config['src_lang']
                dest_lang = config['dest_lang']
                cur.execute(f'''
                    insert into {STATS} (hashed_user_id, src_lang, dest_lang, created_at)
                    values (%s, %s, %s, current_timestamp)
                    ''', (hashed_user_id, src_lang, dest_lang))
            conn.commit()
        logging.info("Stats saved successfully.")
    except psycopg.Error as e:
        logging.error(f"Error saving stats: {e}.")
        conn.rollback()
