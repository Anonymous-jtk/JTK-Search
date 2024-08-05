import sqlite3
import asyncio
import aiofiles
import queue
import os
import sys

if len(sys.argv) == 1:
    raise

folder = f'{str(os.path.dirname(os.path.realpath(__file__)))}\\files\\{sys.argv[1]}\\'

conn = sqlite3.connect(f'{str(os.path.dirname(os.path.realpath(__file__)))}\\db\\{sys.argv[1]}.db')
cursor = conn.cursor()

q = queue.Queue()
files = os.listdir(folder)


async def main():
    for file in files:
        print(f'inserting {file} ({str(files.index(file)+1)}/{str(len(files))})')
        async with aiofiles.open(folder + file, 'r', encoding='cp932') as fp:
            text = await fp.read()
            q.put((file, text))

asyncio.run(main())

try:
    cursor.execute('CREATE TABLE thread(Name text, Data text);')
except Exception:
    pass

cursor.executemany('INSERT INTO thread VALUES(?, ?);', list(q.queue))

conn.commit()
conn.close()
