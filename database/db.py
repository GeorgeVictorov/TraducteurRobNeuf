import asyncpg
import psycopg
from config_data.config import load_config


async def setup_database():
    config = load_config()
    return await asyncpg.create_pool(database=config.db.database,
                                     user=config.db.db_user,
                                     password=config.db.db_password,
                                     host=config.db.db_host)


async def create_tables(pool):
    async with pool.acquire() as connection:
        await connection.execute('''create table if not exists users_config (
                            id serial primary key,
                            hashed_user_id text unique,
                            src_lang text,
                            dest_lang text
                          )''')

        await connection.execute('''create table if not exists stats_data (
                            id serial primary key,
                            hashed_user_id text,
                            src_lang text,
                            dest_lang text,
                            created_at timestamp,
                            foreign key (hashed_user_id) references {USERS_CONFIG} (hashed_user_id)
                          )''')


async def close_database(pool):
    if pool:
        await pool.close()
