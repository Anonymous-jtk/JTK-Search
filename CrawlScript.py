import asyncio
import aiohttp
import aiofiles
import queue
import xml.etree.ElementTree as et
import traceback
import os
import sys

if len(sys.argv) == 1:
    raise

links_to_download = queue.Queue()
header = {
    'User-Agent': ('Mozilla/5.0 (Windows NT 10.0;Win64; x64)\
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98\
    Safari/537.36')
}

tree = et.parse(sys.argv[1])
root = tree.getroot()
board = root[0][0].text.split('/')[-3]
download_path = f'{str(os.path.dirname(os.path.realpath(__file__)))}\\files\\{board}'

if not os.path.exists(download_path):
    os.mkdir(download_path)

files = os.listdir(download_path)
missing_files = list(
    filter(lambda x: str(x[0].text).split('/')[-2] not in files, root)
)

for url in missing_files:
    links_to_download.put(url[0].text)


async def download(url: str):
    print(f'downloading {url}')
    timestamp = str(url).split('/')[-2]
    try:
        async with aiohttp.ClientSession(headers=header) as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    async with aiofiles.open(
                            f'{str(os.path.dirname(os.path.realpath(__file__)))}\\files\\{board}\\{timestamp}.html', 'w', encoding='cp932') as fp:
                                await fp.write(await resp.text(encoding='cp932'))
                                print(f'{timestamp} downloaded')
                else:
                    print(f'error code: {resp.status}')
                    await asyncio.sleep(5.0)
                resp.close()
    except Exception:
        print(traceback.format_exc())


async def main():
    while not links_to_download.empty():
        link = links_to_download.get()
        await download(link)

asyncio.run(main())