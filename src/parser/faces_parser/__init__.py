import json
import numpy as np
import pandas as pd
import os
import glob
from tqdm import tqdm_notebook as tqdm
from itertools import chain


l_value_keys = ['Eyeglasses',
                'Sunglasses',
                'Gender',
                'EyesOpen',
                'Smile',
                'MouthOpen',
                'Mustache',
                'Beard']

columns = {'movie_id': str
           , 'image_name': str
           , 'no_faces': float
           , 'Eyeglasses': float
           , 'Sunglasses': float
           , 'Gender': str
           , 'EyesOpen': float
           , 'Smile': float
           , 'MouthOpen': float
           , 'Mustache': float
           , 'Beard': float
           , 'Emotions': str
           }


def get_info_from_keys_with_value(face_details, key):
    l = [face.get(key).get('Value') for face in face_details]
    if isinstance(l[0], str):
        return '|'.join(l)
    else:
        return sum(l)


def get_info_from_keys_with_value_all(face_detailes, l_value_keys):
    output = {}
    for key in l_value_keys:
        output[key] = get_info_from_keys_with_value(face_detailes, key)
    return output


def get_emotions(face_detailes, threshold):
    l = list(chain.from_iterable([[em.get('Type') for em in face.get('Emotions') if em.get('Confidence') > threshold]
                  for face in face_detailes]))
    return {'Emotions': '|'.join(l)}


def parse_one_json(json_path):
    dict_data_of_one_json = {}
    dict_data_of_one_json['movie_id'] = int(
        os.path.split(os.path.split(os.path.split(json_path)[0])[0])[1])
    dict_data_of_one_json['image_name'] = os.path.split(json_path)[1].replace('.json', '')
    with open(json_path, 'r') as f:
        faces = json.load(f)

    face_detailes = faces['FaceDetails']
    no_faces = len(face_detailes)
    dict_data_of_one_json.update({'no_faces': no_faces})

    if no_faces > 0:
        dict_data_of_one_json.update(get_info_from_keys_with_value_all(face_detailes, l_value_keys))
        dict_data_of_one_json.update(get_emotions(face_detailes, 50))
    df = pd.DataFrame(dict_data_of_one_json, index=[0], columns=columns.keys())
    correct_types(df)
    return df


def correct_types(df):
    for col in df.columns:
        type_ = columns.get(col)
        if type_ is not None:
            df[col] = df[col].astype(type_)


def dump_to_db(con, table_name, df):
    con.put(key=table_name, value=df, format='table', data_coulmns=True, append=True,
            min_itemsize=250)


def parse_jsons(l_json, con):
    dfs = []
    table_name = 'faces'
    for i, json_path in tqdm(enumerate(l_json), total=len(l_json)):
        if 'faces' not in json_path:
            continue

        dfs.append(parse_one_json(json_path))
        if i % 100 == 0:
            df = pd.concat(dfs, ignore_index=True)
            dump_to_db(con, table_name, df)
            dfs = []

    df = pd.concat(dfs, ignore_index=True)
    dump_to_db(con, table_name, df)
