import json
import pandas as pd
import os
import re


labels_json_report_regex = r"(\d+)\W{1,2}labels\W{1,2}(image-\d+\.jpg)\.json"

def get_labels(labels_json_object):
    return {'no_of_labels' : len(labels_json_object.get('Labels')) \
            , 'names': '|'.join([label.get('Name') for label in labels_json_object.get('Labels')]) \
            , 'confidences': '|'.join([str(label.get('Confidence', 0)) for label in labels_json_object.get('Labels')]) \
           }


def parse_one_json(json_path):
    matches = re.search(labels_json_report_regex, json_path)
    movie_id = matches.group(1)
    frame_id = matches.group(2)
    
    
    with open(json_path,encoding='latin-1') as json_file:
        labels_json_data = json.load(json_file)
        
    labels = get_labels(labels_json_data)
    
    df = pd.DataFrame(labels, index=[0])
    
    return df
