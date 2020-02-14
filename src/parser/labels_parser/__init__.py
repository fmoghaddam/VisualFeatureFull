import json
import pandas as pd
import os
from src.parser.base import correct_types

columns = {'movie_id': str
           , 'image_name': str
           , 'no_of_labels' : float
           , 'labels': str
           }


def get_labels(json_object, threshold):
    return '|'.join([label.get('Name')
                     for label in json_object.get('Labels')
                     if label.get('Confidence', 0) > threshold])


def parse_one_json(json_path, threshold):
    dict_data_of_one_json = {}
    dict_data_of_one_json['movie_id'] = int(
        os.path.split(os.path.split(os.path.split(json_path)[0])[0])[1])
    dict_data_of_one_json['image_name'] = os.path.split(json_path)[1].replace('.json', '')
    with open(json_path, 'r') as f:
        labels = json.load(f)
    no_of_labels = len(labels.get('Labels'))
    dict_data_of_one_json['no_of_labels'] = no_of_labels
    if no_of_labels > 0:
        dict_data_of_one_json['labels'] = get_labels(labels, threshold)
    df = pd.DataFrame(dict_data_of_one_json, index=[0], columns=columns.keys())
    correct_types(df, columns)
    return df
