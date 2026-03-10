"""
This is the main module for the application. It serves as the entry point for the program and is responsible for initializing the application. 

The ideia is to get the performece ranking of differents cellphone models from the website "https://www.antutu.com/web/ranking" and get the bests prices for each model from the weebsite "https://www.tudocelular.com/".

In the future, I plan to add a cost-benefit graphic comparing the performance gain by the price increase.
"""

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


def extract_antutu_html(limit: int = 30):
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




def extract_antutu_table(): 
    with open(PATH_HTML_ANTUTU, 'rb') as f:
        html = f.read().decode("utf-8", errors="strict")  # or "replace" if needed
    
    start, final = '<table ', '</table>'
    table_pos_init = html.find(start)
    table_pos_final = html.find(final, table_pos_init) + len(final)

    with open(PATH_TABLE_ANTUTU, 'w') as f:
        f.write(html[table_pos_init:table_pos_final])


def extract_antutu_models_scores(): pass
#     # 2) Fallback: parse por texto (quando o site devolve linhas tipo "1Red Magic...; ...; 4002199")
#     text = re.sub(r"<[^>]+>", "\n", html)  # remove tags grosseiramente
#     lines = [ln.strip() for ln in text.splitlines() if ln.strip()]

#     out = []
#     for ln in lines:
#         # pega linhas com padrão: começa com rank + texto + ; ... ; total
#         if ";" in ln and re.match(r"^\d+\s*[A-Za-z]", ln):
#             parts = [p.strip() for p in ln.split(";") if p.strip()]
#             if len(parts) >= 2:
#                 # rank + nome no primeiro pedaço
#                 m = re.match(r"^(\d+)\s*(.+)$", parts[0])
#                 if not m:
#                     continue
#                 rank = int(m.group(1))
#                 name = m.group(2)

#                 # total score costuma ser o último número grande na linha
#                 last = parts[-1]
#                 total_digits = re.sub(r"\D", "", last)
#                 if not total_digits:
#                     continue
#                 total = int(total_digits)

#                 out.append((rank, name, total))

#     out.sort(key=lambda x: x[0])
#     if limit:
#         out = out[:limit]
#     return out

update = False

if __name__ == "__main__":
    
    if update: extract_antutu_html(); print("Table updated.")
    
    extract_antutu_table()
    



    # for rank, model, total in data:
    #     print(f"{rank:>2} | {model} | {total}")
