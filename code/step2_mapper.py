# step2_mapper.py 
#!/usr/bin/env python3
import sys
import re
import string
import helper_func as hf
import os

# ============================================================
# Step 2 说明（非常重要）：
#
# - Step 1 使用 cleaned_text.txt 是 TA 明确允许的
# - Step 2 要“按书统计 top words 在不同年份的分布”
#
# 因此：
#   - Step 2 必须对 data/* 中的「每一个文件」运行
#   - 每个 mapper 实例只处理“一本书”
#   - 年份必须从【文件名】一次性确定
#
# ❌ 不能从正文 line 中猜 year
# ❌ 不能使用 cleaned_text.txt
# ============================================================

# 读取 Step 1 的 top25 词
# load top words
TOP_WORDS = set()
with open("results/step1_topwords.txt") as f:
    for line in f:
        w, _ = line.strip().split("\t")
        TOP_WORDS.add(w)

# Yuqing
# KNOWN_DATES = {
#     # Sherlock Holmes
#     'study in scarlet': 1887,
#     'sign of the four': 1890,
#     'adventures of sherlock holmes': 1892,
#     'memoirs of sherlock holmes': 1894,
#     'hound of the baskervilles': 1902,
#     'return of sherlock holmes': 1905,
#     'valley of fear': 1915,
#     'his last bow': 1917,
#     'bruce-partington plans': 1908,
#     # Edgar Allan Poe
#     'edgar allan poe': 1845,
#     'works of edgar allan poe': 1845,
#     # Agatha Christie
#     'mysterious affair at styles': 1920,
#     'murder on the links': 1923,
#     'poirot investigates': 1924,
#     'secret adversary': 1922,
#     'man in the brown suit': 1924,
#     # Father Brown by Chesterton
#     'innocence of father brown': 1911,
#     'wisdom of father brown': 1914,
#     # Others
#     'moonstone': 1868,
#     'mystery of the yellow room': 1907,
#     'secret of the night': 1914,
#     'red house mystery': 1922,
#     'whose body': 1923,
#     'hand in the dark': 1920,
# }

# ===============================
# filename -> year mapping
# 说明：
# - 这里的 key 用 “清洗后的文件名” 去匹配（只保留字母数字，小写）
# - 你 data/ 里的文件名很长且可能包含破折号、特殊字符，所以必须清洗
# ===============================
BASENAME_TO_YEAR = {
    "astudyinscarletbyarthurconandoyle": 1887,
    "thesignofthefourbyarthurconandoyle": 1890,
    "theadventuresofsherlockholmesbyarthurconandoyle": 1892,
    "thememoirsofsherlockholmesbyarthurconandoyle": 1894,
    "thehoundofthebaskervillesbyarthurconandoyle": 1902,
    "thereturnofsherlockholmesbyarthurconandoyle": 1905,
    "thevalleyoffearbyarthurconandoyle": 1915,
    "hislastbowsomelaterreminiscencesofsherlockholmesbyarthurconandoyle": 1917,
    "theadventureofthebrucepartingtonplansbyarthurconandoyle": 1908,

    # 注意：你 data 里 Poe 的文件名包含 “—Volume1/2” 这种符号，清洗后会连在一起
    "theworksofedgarallanpoevolume1byedgarallanpoe": 1845,
    "theworksofedgarallanpoevolume2byedgarallanpoe": 1845,

    "themysteriousaffairatstylesbyagathachristie": 1920,
    "themurderonthelinksbyagathachristie": 1923,
    "poirotinvestigatesbyagathachristie": 1924,
    "thesecretadversarybyagathachristie": 1922,
    "themaninthebrownsuitbyagathachristie": 1924,

    "theinnocenceoffatherbrownbygkchesterton": 1911,
    "thewisdomoffatherbrownbygkchesterton": 1914,

    "themoonstonebywilkecollins": 1868,
    "themysteryoftheyellowroombygastonleroux": 1907,
    "thesecretofthenightbygastonleroux": 1914,
    "theredhousemysterybyaamilne": 1922,
    "whosebodyalordpeterwimseynovelbydorothylsayers": 1923,
    "thehandinthedarkbyarthurjrees": 1920,
}


# same header/footer handling as step1 - Yuqing
# in_content = True
# current_year = None

# ============================================================
# 从环境变量获取当前输入文件名（由 Makefile 在循环里 export 进来）
# ============================================================
filename = os.environ.get("map_input_file", "")
base = os.path.basename(filename)
key = re.sub(r"[^a-z0-9]", "", base.lower())

# 1) 先精确匹配
current_year = BASENAME_TO_YEAR.get(key)

# 2) 再做 substring 兜底（防止某些文件名与你字典 key 有细微差异导致整本书被跳过）
if current_year is None:
    for k, y in BASENAME_TO_YEAR.items():
        if k in key or key in k:
            current_year = y
            break

# 如果还是无法识别年份，安全退出（避免输出 word\tNone\t1）
if current_year is None:
    sys.exit(0)

# ============================================================
# Content processing
# 正文处理（和 Step 1 一致）
# ============================================================
in_toc = False
for line in sys.stdin:
    line = line.strip()

    # if '*** START OF' in line:
    #     in_content = True
    #     continue
    # if '*** END OF' in line:
    #     in_content = False
    #     current_year = None
    #     continue
    
    # ======================================================================
    # 原有 Title 行识别逻辑（保留，但在 cleaned_text.txt 中无效）
    # cleaned_text.txt 中已经移除了 Title: 行，
    # 因此该逻辑不会被触发，current_year 会一直为 None。
    # ======================================================================
    # if not in_content and current_year == None:
    #     # detect title to assign year
    #     if 'Title:' in line:
    #         low = line.lower()
    #         for title in KNOWN_DATES:
    #             if title in low:
    #                 current_year = KNOWN_DATES[title]
    #                 break
    #     continue

    # if not current_year:
    #     continue
    
    # Table of Contents detection（保留）
    if hf.is_table_of_contents(line):
        in_toc = True
        continue
            
    if in_toc and hf.is_toc_entry(line):
        continue
    else:
        in_toc = False
    
    # ======================================================================
    # 原有统计逻辑（增加安全防护）
    # 防止在极端情况下 current_year 仍为 None，
    # 输出 word\tNone\t1 这种脏数据，影响 reducer 统计。
    # ======================================================================
    words = re.findall(r"[a-zA-Z]+", line)
    for w in words:
        w = w.lower()
        if w in TOP_WORDS:
            print(f"{w}\t{current_year}\t1")