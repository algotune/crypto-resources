import os
from typing import List, Dict

import pandas as pd
import numpy as np

def get_wiki_status_color(input_text):
    if input_text is None or input_text == 'inactive':
        result_text = ":heavy_multiplication_x:"
    else:
        result_text = ":heavy_check_mark:"
    return '<sub>{}</sub>'.format(result_text)


def get_wiki_rating(input_rating):
    result_text = ''
    if input_rating is not None and not np.isnan(input_rating):
        rating = int(input_rating)
        result_text = ':star:x{}'.format(rating)
    return '<sub>{}</sub>'.format(result_text)


def gen_wiki(input_df: pd.DataFrame, output_path: str, file_name: str):
    output_path_full = os.path.join(output_path, '{}.md'.format(file_name))
    with open(output_path_full, 'w') as f:
        f.write(input_df.to_markdown(index=False))
    print('wiki generated in [{}]'.format(output_path_full))


def format_wiki_df(input_df: pd.DataFrame,
                   valid_columns: List,
                   sub_columns: List = None,
                   url_columns_dict: Dict = None,
                   status_columns: List = None,
                   rating_columns: List = None,
                   sub_headers: bool = True,
                   order_by: List = None,
                   order_ascend: bool = False):
    output_df = input_df[valid_columns].copy()
    if url_columns_dict is not None:
        for k, v in iter(url_columns_dict.items()):
            result_list = []
            if v in input_df.columns:
                for idx, irow in input_df[[k, v]].iterrows():
                    if not pd.isna(irow[v]):
                        result_list.append('[{}]({})'.format(irow[k], irow[v]))
                    else:
                        result_list.append(irow[k])
            else:
                # if value of the url_columns_dict is not a valid column then v becomes the display item,
                # and k is the url
                for x in input_df[k]:
                    if pd.isna(x):
                        result_list.append('NA')
                    else:
                        result_list.append('[{}]({})'.format(v, x))
            output_df[k] = result_list

    if sub_columns is not None:
        for col in sub_columns:
            output_df[col] = output_df[col].apply(lambda x: '<sub>{}</sub>'.format(x))

    if status_columns is not None:
        for col in status_columns:
            output_df[col] = output_df[col].apply(lambda x: get_wiki_status_color(x))

    if rating_columns is not None:
        for col in rating_columns:
            output_df[col] = output_df[col].apply(lambda x: get_wiki_rating(x))

    if sub_headers:
        output_df.columns = ['<sub>{}</sub>'.format(x) for x in output_df.columns]

    if order_by is not None:
        output_df = output_df.sort_values(by=order_by, ascending=order_ascend).reset_index(drop=True)

    return output_df
