import json
import pandas as pd
import os
import re

confidence_value_attributes = ['Gender', \
                               'Eyeglasses', \
                               'Sunglasses', \
                               'Gender', \
                               'EyesOpen', \
                               'Smile', \
                               'MouthOpen', \
                               'Mustache', \
                               'Beard']

# https://docs.aws.amazon.com/rekognition/latest/dg/API_Emotion.html
emotion_types = ['HAPPY' , 'SAD' , 'ANGRY' \
                  , 'CONFUSED', 'DISGUSTED' ,'SURPRISED' \
                  , 'CALM', 'UNKNOWN','FEAR']


face_json_report_regex = r"(\d+)\W{1,2}faces\W{1,2}(image-\d+\.jpg)\.json"

def extract_face_details(actor_face_jsonobject,movie_id,frame_id):
    features = {'movie_id': movie_id,\
                'image_name':frame_id,\
                'confidence':actor_face_jsonobject['Confidence'], \
                'age_range_high': actor_face_jsonobject['AgeRange']['High'], \
                'age_range_low': actor_face_jsonobject['AgeRange']['Low'], \
               }
    # fill all the emotions with zero confidence
    for emotion_type in emotion_types:
        features[emotion_type.lower()] = 0
    
    for emotion in actor_face_jsonobject['Emotions']:
        features[emotion['Type'].lower()] = emotion['Confidence']
     
    for attribute in confidence_value_attributes:
        features[attribute.lower()+'_confidence'] = actor_face_jsonobject[attribute]['Confidence']
        features[attribute.lower()+'_value'] =actor_face_jsonobject[attribute]['Value']
        
    return features


def parse_one_json(json_path):
    matches = re.search(face_json_report_regex, json_path)
    movie_id = matches.group(1)
    frame_id = matches.group(2)
    
    faces_details = []
    with open(json_path,encoding='latin-1') as json_file:
         json_data = json.load(json_file)
            
    for face_details in json_data['FaceDetails']:
        extracted_face_details = extract_face_details(face_details,movie_id,frame_id)
        faces_details.append(extracted_face_details)
                                                    
    df = pd.DataFrame(faces_details)
    return df

