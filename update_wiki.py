import os
from typing import List

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
                   status_columns: List = None,
                   rating_columns: List = None,
                   sub_headers: bool = True,
                   order_by: List = None,
                   order_ascend: bool = False):
    output_df = input_df[valid_columns].copy()
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