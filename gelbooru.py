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
tags = input("Please enter the tags (meta-tags supported) you wish to search for (seperated by spaces): ")
gelbooru = json.loads(requests.get('https://gelbooru.com/index.php?page=dapi&s=post&q=index&json=1&limit={}&tags={}'.format(amount, tags)).text)
async def download_image(url):
    await aapi.download(url, path=os.getcwd(), name="image{}.jpg".format(index))
for image in gelbooru:
    if "i.pximg.net" in image["source"] and not ".zip" in image["source"]:
        if " " in image["source"]:
            realSource = image["source"].split(' ')[1]
            print("image found (realsource pximg), downloading: {}".format(realSource))
            index += 1
            asyncio.run(download_image(realSource))
        else:
            print("image found (pximg), downloading: {}".format(image["source"]))
            index += 1
            asyncio.run(download_image(image["source"]))
    else:
        if "file_url" in image:
            if "img2.gelbooru.com" in image["file_url"]:
                index += 1
                print("image found (gelbooru cdn), downloading: {}".format(image["file_url"]))
                img_data = requests.get(image["file_url"]).content
                with open('image{}.{}'.format(index, image["file_url"].split('.')[3]), 'wb') as handler:
                    handler.write(img_data)
