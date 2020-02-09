import requests
import json
import os
import time
import asyncio
from pixivpy_async import *
papi = PixivAPI()
aapi = AppPixivAPI()
index = 0
amount = input("Please enter the amount of images you want to search for: ")
tags = input("Please enter the tags you wish to search for (seperated by spaces): ")
danbooru = json.loads(requests.get('https://danbooru.donmai.us/posts.json?tags={}&limit={}&random=true'.format(tags, amount)).text)
async def download_image(url):
    await aapi.download(url, path=os.getcwd(), name="image{}.jpg".format(index))
for image in danbooru:
    if "i.pximg.net" in image["source"] and not ".zip" in image["source"]:
        print("image found, downloading: {}".format(image["source"]))
        index += 1
        asyncio.run(download_image(image["source"]))
