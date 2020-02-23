import json
import pandas as pd
import os
import re

celebrity_json_report_regex = r"(\d+)\W{1,2}celebrity\W{1,2}(image-\d+\.jpg)\.json"

def extract_celebrity_info(celebrity_face_jsonobject,movie_id,frame_id):
    return {'movie_id': movie_id,\
            'image_name':frame_id,\
            'match_confidence':celebrity_face_jsonobject['MatchConfidence'], \
            'celebrity_name': celebrity_face_jsonobject['Name'], \
            'celebrity_id': celebrity_face_jsonobject['Id'], \
            'celebrity_urls': '|'.join(celebrity_face_jsonobject['Urls']) \
           }

def parse_one_json(json_path):
    matches = re.search(celebrity_json_report_regex, json_path)
    movie_id = matches.group(1)
    frame_id = matches.group(2)
    
    celebrities = []
    with open(json_path,encoding='latin-1') as json_file:
         json_data = json.load(json_file)
        
    for celebrity_face in json_data['CelebrityFaces']:
        extracted_celebrity_info = extract_celebrity_info(celebrity_face,movie_id,frame_id)
        celebrities.append(extracted_celebrity_info)
            
    df = pd.DataFrame(celebrities)
    return df