import sqlite3
import time
import os
import sys

if len(sys.argv) <= 2:
    raise

print(f'keywords: {sys.argv[2]}')
start = time.time()

conn = sqlite3.connect(f'{str(os.path.dirname(os.path.realpath(__file__)))}\\db\\{sys.argv[1]}.db')
cur = conn.cursor()
cur.execute('SELECT * FROM thread WHERE Data LIKE ?;', [f'%{sys.argv[2]}%'])
fetch = cur.fetchall()

for result in fetch:
    i = str(result[1]).index(sys.argv[2])
    print(f'{result[0]} | "...{result[1][i-20:i+20]}..."')

end = time.time()
total = end - start
print(f'search completed in {str(total)} second')

conn.close()
