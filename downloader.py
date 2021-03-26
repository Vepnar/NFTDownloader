#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Download art from https://nftshowroom.com/

DISCLAIMER:
    If you don't want your images in this dataset please send me a message.
    Only use for Educational Purposes. I am not responsible for the things you do with this data.

License:
    The Python script is under the MIT license, All files downloaded are under a different / unknown license.

TODO:
    Add extra documentation

Author: Arjan de Haan (Vepnar)
"""
import os
import json
import time
import requests
from enum import Enum, auto


class SortBy(Enum):
    """Sorting options for the downloader"""
    UPDATED = 'updated'
    NEWST = 'newest'
    OLDEST = 'oldest'
    PRICE_ASC = 'price_asc'  # Cheapest
    PRICE_DESC = 'price_desc'  # Most expensive


class ArtType(Enum):
    VIDEO = auto()  # Only avi, mp4, mov etc
    PHOTO = auto()  # Only  png, jpeg, jpg etc
    GIF = auto()  # Only .gif
    IMAGE = GIF | PHOTO  # IMAGE = PHOTO + GIF
    ALL = GIF | PHOTO | VIDEO  # ALL = IMAGE + VIDEO


def remove_nsfw(rows: list):
    """Pretty self explainatory

    Args:
        rows (list): Items with nsfw items 

    Returns:
        rows (list): List without nsfw items
    """
    for row in rows:
        if row['nsfw'] == True:
            rows.remove(row)

    return rows


def get_art_type(row) -> ArtType:
    if row['image'] == None:
        return ArtType.VIDEO
    elif row['image'].endswith('.gif'):
        return ArtType.GIF
    else:
        return ArtType.PHOTO


def assign_art_types(rows) -> list:
    for row in rows:
        art_type = get_art_type(row)
        row['type'] = art_type
    return rows


def retrieve_art_metadata(page=1, limit=100, sort_by: SortBy = SortBy.UPDATED) -> list:
    url = f'https://nftshowroom.com/api/market?page={page}&limit={limit}&sort_by={sort_by.value}'

    request = requests.get(url)
    if request.status_code != 200:
        raise Exception('Status code isn\'t 200')

    return request.json()


def download_art_piece(piece, master_dir='./dataset', video_dir='video', image_dir='image', gif_dir='gif'):
    """The art type needs to be assigned"""


    if piece['type'] == ArtType.VIDEO:
        url = piece['video']
    else:
        url = piece['image']

    file_name = ''.join([piece['cid'], '.', url.split('.')[-1]])

    directories = {
        ArtType.PHOTO: image_dir,
        ArtType.GIF: gif_dir,
        ArtType.VIDEO: video_dir
    }

    # Create a local path
    path = os.path.join(master_dir, directories[piece['type']])
    os.makedirs(path, exist_ok=True)
    file_path = os.path.join(path, file_name)
    
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(file_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

    return file_path

def csv_header():
    return 'title,name,creator,art_series,price,symbol,type,likes,nsfw,tokens,year,rights,royalty,cid,path\r\n'

def piece_to_string(piece):
    p = lambda x: '"'+piece[x].strip(',"')+'"' # Sorry for this
    return f"{p('title')},{p('name')},{p('creator')},{p('art_series')},{piece['price']},{p('symbol')},{piece['type'].name},{piece['reactions']['likes']},{piece['nsfw']},{piece['tokens']},{piece['year']},{piece['rights']},{piece['royalty']},{p('cid')},{p('path')}\r\n"

if __name__ == '__main__':
    attempts = 5
    pages = 50
    csv_file = open('./dataset.csv', 'w')
    csv_file.write(csv_header())

    for page in range(1,pages):
        print(f'Downloading page {page}/{pages}')
        art_collection = retrieve_art_metadata(page=page)
        
        art_collection = assign_art_types(art_collection)
        for piece in art_collection:
            for attempt in range(attempts): # Attempts
                try:
                    art_path = download_art_piece(piece)
                    piece['path'] = art_path

                    csv_file.write(piece_to_string(piece))
                    break
                except Exception as e:
                    print(f'Downloading failed, attempts: {attempt+1}/{attempts}', e)
                    time.sleep(5*attempt)

        csv_file.flush()
        print('sleeping...')
        time.sleep(60)
    csv_file.close()
