import pandas as pd
import os

from conf import PROJECT_ROOT_DIR
from update_readme import update_readme_section
from update_wiki import format_wiki_df


def gen_wiki_base_projects():
    content_df = pd.read_csv(os.path.join(PROJECT_ROOT_DIR, 'raw_data', 'token_repos.csv'))
    format_df = format_readme_df_base_projects(content_df)
    output_path = os.path.join(PROJECT_ROOT_DIR, 'generated_wiki', 'base_projects.md')
    with open(output_path, 'w') as f:
        content_str = format_df.to_markdown(index=False)
        f.write(content_str)


def update_base_project():
    content_df = pd.read_csv(os.path.join(PROJECT_ROOT_DIR, 'raw_data', 'token_repos.csv'))
    format_df = format_readme_df_base_projects(content_df)
    update_readme_section('Base Projects', format_df)


def format_readme_df_base_projects(content_df: pd.DataFrame):
    """

    :param content_df:
    usage:
    >>> content_df = pd.read_csv('/Users/b3yang/workspace/crypto-resources/raw_data/token_repos.csv')
    """
    valid_columns = ['Symbol',
                     'Name',
                     'Github',
                     'Reddit',
                     'Telegram',
                     'Discord',
                     'Medium',
                     'Block Explorer',
                     'Twitter',
                     'Whitepaper',
                     'Blog']
    url_columns_dict = {
        'Github': '**',
        'Reddit': '**',
        'Telegram': '**',
        'Discord': '**',
        'Medium': '**',
        'Block Explorer': '**',
        'Twitter': '**',
        'Blog': '**',
        'Whitepaper': '**',
        'Symbol': 'Website',

    }
    result_df = format_wiki_df(content_df, valid_columns, sub_columns=valid_columns, url_columns_dict=url_columns_dict)
    return result_df
