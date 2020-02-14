from tqdm import tqdm_notebook as tqdm
import pandas as pd


def correct_types(df, columns):
    for col in df.columns:
        type_ = columns.get(col)
        if type_ is not None:
            df[col] = df[col].astype(type_)


def dump_to_db(con, table_name, df):
    con.put(key=table_name, value=df, format='table', data_coulmns=True, append=True,
            min_itemsize=500)


def parse_jsons(l_json, con, threshold, subject):
    dfs = []
    package = f'src.parser.{subject}_parser'
    parse_one_json = getattr(__import__(package, fromlist=['parse_one_json']), 'parse_one_json')
    for i, json_path in tqdm(enumerate(l_json), total=len(l_json)):
        if subject not in json_path:
            continue

        dfs.append(parse_one_json(json_path, threshold))
        if len(dfs) > 99:

            df = pd.concat(dfs, ignore_index=True)
            dump_to_db(con, table_name=subject, df=df)
            dfs = []
    if len(dfs) > 0:
        df = pd.concat(dfs, ignore_index=True)
        dump_to_db(con, table_name=subject, df=df)
