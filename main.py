"""
Author: Felipe Sallazar
Github: https://github.com/Sallada07

This is the main module for the application. It serves as the entry point for the program and is responsible for initializing the application. 

The ideia is to get the performece ranking of differents cellphone models from the website "https://www.antutu.com/web/ranking" and get the bests prices for each model from the website "https://www.tudocelular.com/".

In the future, I plan to add a cost-benefit graphic comparing the performance gain by the price increase.
"""

import numpy as np
import os
import pandas as pd
import re
import requests

# PATHs
ROOT = '.'
FOLDER_TEMP = 'temp'
FILE_HTML_ANTUTU = 'antutu_html.txt'
FILE_TABLE_ANTUTU = 'antutu_table.txt'

PATH_HTML_ANTUTU = os.path.join(ROOT, FOLDER_TEMP, FILE_HTML_ANTUTU)
PATH_TABLE_ANTUTU = os.path.join(ROOT, FOLDER_TEMP, FILE_TABLE_ANTUTU)

URL_ANTUTU = "https://antutu.com/en/ranking/rank1.htm"  # trocar pelo link: https://antutu.com/web/ranking


def get_div(text:str, div_name:str, start:int = 0):
    init, final = f'<{div_name}', f'</{div_name}>'
    pos_init = text.find(init, start)
    pos_final = text.find(final, pos_init) + len(final) if pos_init != -1 else -1
    return pos_init, pos_final


def _extract_antutu_html(limit: int = 30):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }

    r = requests.get(URL_ANTUTU, headers=headers, timeout=limit)  # Last test (version_1.0.1 | 2026-02-09 a-m-d): <Response [200]>
    r.raise_for_status()
    html = r.content

    with open(PATH_HTML_ANTUTU, 'wb') as f:
        f.write(html)


def _extract_antutu_table(): 
    with open(PATH_HTML_ANTUTU, 'rb') as f:
        html = f.read().decode("utf-8", errors="strict")  # or "replace" if needed
    
    start, final = '<table ', '</table>'
    table_pos_init = html.find(start)
    table_pos_final = html.find(final, table_pos_init) + len(final)

    with open(PATH_TABLE_ANTUTU, 'w') as f:
        f.write(html[table_pos_init:table_pos_final])


def _extract_antutu_models_scores():

    with open(PATH_TABLE_ANTUTU, 'r') as f:
        table = f.read()

    head_cut = get_div(table, 'thead')
    head = table[head_cut[0]:head_cut[1]]  # separates the header from the body of the table.
    text = re.sub(r"<[^>]+>", "\n", head)  # replace tags by "\n"
    head =  [line.strip() for line in text.splitlines() if line.strip()]  # clean header (probably with seven items: 'Rank', 'Device / Spec', 'CPU', 'GPU', 'MEM', 'UX', 'Total Score')
    head = head[:1] + [item.strip() for item in head[1].split('/')] + head[2:]  # clean header (probably with eight items)
    

    body_cut = get_div(table, 'tbody', start=head_cut[1])
    body = table[body_cut[0]:body_cut[1]]  # separates the body of the table.
    
    ranges = []
    gap = get_div(body, 'tr')
    while gap[0] != -1:
        ranges.append(gap)
        gap = get_div(body, 'tr', gap[1])
    
    lines = []
    for gap in ranges:
        line = body[gap[0]:gap[1]]
        text = re.sub(r"<[^>]+>", "\n", line)  # replace tags by "\n"
        line =  [item.strip() for item in text.splitlines() if item.strip()] # clean lines (probably nine items: 'Rank', 'Device, 'Spec', '| Spec', 'CPU', 'GPU', 'MEM', 'UX', 'Total Score'))
        line = line[:2] + [''.join(line[2:-5])] + line[-5:]   # clean lines (probably with eight items) 
        lines.append(line)

    return pd.DataFrame(data=lines, columns=head)


def _get_price_from_tudocelular(): pass


def create_db():
    db = _extract_antutu_models_scores()
    df = db[["Device", "Total Score"]].copy()
    df["Price"] = np.nan
    

def update_table():
    _extract_antutu_html(); print("HTML updated.")
    _extract_antutu_table(); print("Table updated.")

update = False

if __name__ == "__main__":
    
    if update: update_table()
    
    create_db()
    
    

    # for rank, model, total in data:
    #     print(f"{rank:>2} | {model} | {total}")
