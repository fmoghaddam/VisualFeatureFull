from tqdm import tqdm_notebook as tqdm
import pandas as pd


def dump_to_db(con, table_name, df):
    con.put(key=table_name, value=df, format='table', data_coulmns=True, append=True,
            min_itemsize=500)

def parse_jsons_as_df(list_of_json_paths,subject):
    package = f'src.parser.{subject}_parser'
    parse_one_json = getattr(__import__(package, fromlist=['parse_one_json']), 'parse_one_json')
    dataframes = []
    for i, json_path in tqdm(enumerate(list_of_json_paths), total=len(list_of_json_paths)):
        dataframes.append(parse_one_json(json_path))
        
        
    return pd.concat(dataframes, ignore_index=True)



def parse_jsons(list_of_json_paths, con, subject):
    dataframes_chunk = []
    chunk_size = 100
    
    package = f'src.parser.{subject}_parser'
    parse_one_json = getattr(__import__(package, fromlist=['parse_one_json']), 'parse_one_json')
    
    for i, json_path in tqdm(enumerate(list_of_json_paths), total=len(list_of_json_paths)):
        if subject not in json_path:
            continue
            
        dataframes_chunk.append(parse_one_json(json_path))
        
        if len(dataframes_chunk) > chunk_size:
            df = pd.concat(dataframes_chunk, ignore_index=True)
            dump_to_db(con, table_name=subject, df=df)
            dataframes_chunk = []
            
    # concat remaining items in the chunk to the dataframes holder
    if len(dataframes_chunk) > 0:
        df = pd.concat(dataframes_chunk, ignore_index=True)
        dump_to_db(con, table_name=subject, df=df)
