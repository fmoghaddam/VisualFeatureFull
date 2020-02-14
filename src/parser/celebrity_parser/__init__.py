import json
import pandas as pd
import os
from src.parser.base import correct_types

columns = {'movie_id': str
           , 'image_name': str
           , 'no_of_celebrities': float
           , 'celebrity_names': str
           , 'celebrity_ids': str
           }


def get_celebrity_names(celebrities):
    return '|'.join([c.get('Name') for c in celebrities])


def get_celebrity_ids(celebrities):
    return '|'.join([c.get('Id') for c in celebrities])


def parse_one_json(json_path, threshold):
    dict_data_of_one_json = {}
    dict_data_of_one_json['movie_id'] = int(
        os.path.split(os.path.split(os.path.split(json_path)[0])[0])[1])
    dict_data_of_one_json['image_name'] = os.path.split(json_path)[1].replace('.json', '')
    with open(json_path, 'r') as f:
        celeb = json.load(f)
    celebrities = [d for d in celeb['CelebrityFaces'] if d.get('MatchConfidence') > threshold]
    no_of_celebs = len(celebrities)
    dict_data_of_one_json['no_of_celebrities'] = no_of_celebs
    if no_of_celebs > 0:
        dict_data_of_one_json['celebrity_names'] = get_celebrity_names(celebrities)
        dict_data_of_one_json['celebrity_ids'] = get_celebrity_ids(celebrities)
    df = pd.DataFrame(dict_data_of_one_json, index=[0], columns=columns.keys())
    correct_types(df, columns)
    return df

