import requests
import pandas as pd
from bs4 import BeautifulSoup
import urllib.request
import re
import zipfile
import os
import aiohttp        
import aiofiles
import asyncio
import glob

async def main():
    contents = requests.get('https://www.ncei.noaa.gov/data/local-climatological-data/access/2021/')
    contents_soup = BeautifulSoup(contents.text, 'html.parser')
    contents_tr = contents_soup.find_all('tr')
    download_uris = []
    for tr in contents_tr:
        if "2022-02-07 14:03" in str(tr):
            file_name = re.search(r'href="(.*?)"', str(tr)).group(1)
            download_uris.append(f"https://www.ncei.noaa.gov/data/local-climatological-data/access/2021/{file_name}")
    if not os.path.isdir("./downloads"):
        os.makedirs("./downloads")
        
    async with aiohttp.ClientSession() as session:
        for url in download_uris:
            local_filename = url.split('/')[-1]
            if not os.path.isfile(f"./downloads/{local_filename}"):
                try:
                    async with session.get(url) as resp:
                        if resp.status == 200:
                            f = await aiofiles.open(f'./downloads/{local_filename}', mode='wb')
                            await f.write(await resp.read())
                            await f.close()
                            print(f"successfully downloaded {local_filename}")
                except:
                    print(f"failed to download {local_filename}")
    all_files = glob.glob(os.path.join('./downloads', "*.csv"))
    records = []
    for file_path in all_files:
        try:
            df = pd.read_csv(file_path, low_memory=False)
            records.append(int(df['HourlyDryBulbTemperature'].max()))
        except:
            # print(f"failed to extract value from {file_path.split('/')[-1]}")
            pass
    print("Highest HourlyDryBulbTemperature is", max(records))
if __name__ == "__main__":
    asyncio.run(main())
