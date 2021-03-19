#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Download art from https://nftshowroom.com/

DISCLAIMER:
    If you don't want your images in this dataset please send me a message.
    Only use for Educational Purposes. I am not responsible for the things you do with this data.

License:
    The Python script is under the MIT license, All files downloaded are under a different / unknown license.

Author: Arjan de Haan (Vepnar)
"""
import json
import requests
import argparse
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
        return ArtType.IMAGE

def assign_art_types(rows) -> list:
    for row in rows:
        art_type = get_art_type(row)
        row['type'] = art_type.name
    return rows

def retrieve_art_metadata(page=1, limit=100, sort_by: SortBy = SortBy.UPDATED) -> list:
    url = f'https://nftshowroom.com/api/market?page={page}&limit={limit}&sort_by={sort_by.value}'

    request = requests.get(url)
    if request.status_code != 200:
        raise Exception('Status code isn\'t 200')

    return request.json()

def download_art_piece(piece):
    """The art type needs to be assigned"""
    pass