"""
This is the main module for the application. It serves as the entry point for the program and is responsible for initializing the application. 

The ideia is to get the performece ranking of differents cellphone models from the website "https://www.antutu.com/web/pt/ranking" and get the bests prices for each model from the weebsite "https://www.tudocelular.com/".

In the future, I plan to add a cost-benefit graphic comparing the performance gain by the price increase.

"""

import re
import requests
import pandas as pd  # pip install pandas lxml

def extract_antutu_models_scores(url: str, limit: int|None = None):
    """
    Retorna lista de tuplas: (rank, model, total_score)
    - rank: int
    - model: str (nome do aparelho)
    - total_score: int (pontuação total)
    """
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }

    r = requests.get(url, headers=headers, timeout=30)  # Last test (version_1.0.0 | 2026-02-09 a-m-d): <Response [200]>
    r.raise_for_status()
    html = r.text

#     # 1) Tentativa: ler a tabela HTML diretamente (mais “limpo” quando funciona)
#     try:
#         tables = pd.read_html(html)

#         # Procurar uma tabela que tenha colunas parecidas com "Rank", "Device", "Total Score"
#         best = None
#         for df in tables:
#             cols = [str(c).strip().lower() for c in df.columns]
#             if any("rank" in c for c in cols) and any("total" in c for c in cols):
#                 best = df
#                 break

#         if best is not None:
#             # A AnTuTu pode usar "Device / Spec" ou separar "Device" e "Spec"
#             # Vamos tentar pegar um campo que contenha o nome do aparelho
#             col_rank = next(c for c in best.columns if "rank" in str(c).lower())
#             col_total = next(c for c in best.columns if "total" in str(c).lower())

#             # tentar achar coluna de device
#             device_candidates = [c for c in best.columns if "device" in str(c).lower()]
#             if device_candidates:
#                 col_device = device_candidates[0]
#                 models = best[col_device].astype(str)
#             else:
#                 # fallback: usa a primeira coluna que não seja rank/total e pareça texto
#                 non = [c for c in best.columns if c not in (col_rank, col_total)]
#                 col_device = non[0]
#                 models = best[col_device].astype(str)

#             out = []
#             for _, row in best.iterrows():
#                 try:
#                     rank = int(re.sub(r"\D", "", str(row[col_rank])))
#                     total = int(re.sub(r"\D", "", str(row[col_total])))
#                     model = str(row[col_device]).strip()
#                     if model and total > 0:
#                         out.append((rank, model, total))
#                 except Exception:
#                     continue

#             out.sort(key=lambda x: x[0])
#             if limit:
#                 out = out[:limit]
#             if out:
#                 return out
#     except Exception:
#         pass

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


if __name__ == "__main__":
    URL = "https://antutu.com/en/ranking/rank1.htm"  # troque pelo link da sua foto
    data = extract_antutu_models_scores(URL, limit=30)

    # for rank, model, total in data:
    #     print(f"{rank:>2} | {model} | {total}")
