import csv
import io
import logging
from datetime import datetime

import psycopg

from database.db import Database
from services.services import hash_file_data

STATS = 'stats_data'


def get_stats():
    database = Database()
    conn = database.get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(f'select * from {STATS}')
            rows = cur.fetchall()
            cols = [description[0] for description in cur.description]
            return cols, rows
    except psycopg.Error as e:
        logging.error(f"Error getting stats from the database: {e}.")
        return None, None


def stats_to_csv(columns, data):
    try:
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(columns)
        writer.writerows(data)
        csv_data = output.getvalue()
        return csv_data
    except (io.UnsupportedOperation, csv.Error) as e:
        logging.error(f"Error converting stats to CSV: {e}.")
        return None


def generate_filename(data):
    try:
        data_to_hash = [','.join(map(str, row)) for row in data]
        hashed_data = hash_file_data('\n'.join(data_to_hash))[-4:]
        current_date = datetime.now().strftime('%Y-%m-%d')
        file_name = f'stats_data_{current_date}_{hashed_data}.csv'
        return file_name
    except Exception as e:
        logging.error(f"Error generating filename for stats data: {e}.")
        return None
