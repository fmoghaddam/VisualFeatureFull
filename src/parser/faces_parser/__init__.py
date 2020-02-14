import json
import pandas as pd
import os
from itertools import chain
from src.parser.base import correct_types


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
    l = list(chain.from_iterable(
        [
            [em.get('Type') for em in face.get('Emotions') if em.get('Confidence') > threshold]
            for face in face_detailes
        ]
                                )
            )
    return {'Emotions': '|'.join(l)}


def parse_one_json(json_path, threshold):
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
        dict_data_of_one_json.update(get_emotions(face_detailes, threshold))
    df = pd.DataFrame(dict_data_of_one_json, index=[0], columns=columns.keys())
    correct_types(df, columns)
    return df

