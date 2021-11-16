import os
from conf import PROJECT_ROOT_DIR
import re
import pandas as pd

from git_util import get_repo_attributes_dict, get_github_client, get_repo_path


def get_repo_status_df(input_df: pd.DataFrame, url_column: str):
    """

    :param input_df:
    :param url_column:
    """
    g = get_github_client()
    repo_df = input_df.copy()
    for idx, row in repo_df.iterrows():
        repo_path = row[url_column]
        if not pd.isna(repo_path):
            try:
                print('processing [{}]'.format(repo_path))
                repo = g.get_repo(repo_path)

                repo_attr_dict = get_repo_attributes_dict(repo)
            except Exception as ex:
                print(ex)
                repo_attr_dict = {}

            for k, v in iter(repo_attr_dict.items()):
                repo_df.loc[idx, k] = v
    return repo_df
