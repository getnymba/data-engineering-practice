import requests
import zipfile
import os
import aiohttp        
import aiofiles
import asyncio
download_uris = [
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2018_Q4.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q1.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q2.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q3.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q4.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2020_Q1.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2220_Q1.zip",
]


async def main():
    # your code here
    if not os.path.isdir("./downloads"):
        os.makedirs("./downloads")
    async with aiohttp.ClientSession() as session:
        for url in download_uris:
            local_filename = url.split('/')[-1]
            try:
                async with session.get(url) as resp:
                    if resp.status == 200:
                        f = await aiofiles.open(f'./downloads/{local_filename}', mode='wb')
                        await f.write(await resp.read())
                        await f.close()
                        with zipfile.ZipFile(f'./downloads/{local_filename}', 'r') as zip_ref:
                            zip_ref.extractall('./downloads/')
                        os.remove(f"./downloads/{local_filename}")
                        print(f"successfully downloaded {local_filename}")
            except:
                print(f"failed to download {local_filename}")


if __name__ == "__main__":
    asyncio.run(main())
