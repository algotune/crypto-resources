import os
import re
import pandas as pd

from conf import PROJECT_ROOT_DIR


def update_readme_section(category_name: str,
                          content_df: pd.DataFrame,
                          n_project_to_include: int = 20,
                          include_title: bool = True):
    """

    :param category_name:
    :param content_df:
    :param n_project_to_include:
    :param include_title:
    usage:
    >>> category_name = 'Base Projects'
    >>> content_df = pd.read_csv('/Users/b3yang/workspace/crypto-resources/raw_data/token_repos.csv')
    >>> n_project_to_include = 20
    >>> include_title = True
    """
    check_str = '[PLACEHOLDER_START:{}]'.format(category_name)
    with open(os.path.join(PROJECT_ROOT_DIR, 'README.md')) as f:
        all_read_me = f.read()
        if check_str not in all_read_me:
            print(f'section {check_str} not found')
            raise Exception

    with open(os.path.join(PROJECT_ROOT_DIR, 'README.md'), 'w') as f:
        table_str = content_df.iloc[:n_project_to_include].to_markdown(index=False)
        if include_title:
            table_str = """## {} \n{}""".format(category_name, table_str)

        new_str = f"<!-- [PLACEHOLDER_START:{category_name}] --> \n"
        new_str += table_str
        new_str += f"<!-- [PLACEHOLDER_END:{category_name}] -->"

        search_start = re.escape('<!-- [PLACEHOLDER_START:{}] -->'.format(category_name))
        search_end = re.escape('<!-- [PLACEHOLDER_END:{}] -->'.format(category_name))
        pattern_s = re.compile(r'{}.*?{}'.format(search_start, search_end), re.DOTALL)
        write_str = re.sub(pattern_s, new_str, all_read_me)
        f.write(write_str)
