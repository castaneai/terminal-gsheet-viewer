import os
import sys
import json
import pygsheets
from terminaltables import AsciiTable

if len(sys.argv) < 3:
    print('Usage: ./terminal_gsheet_viewer.py <spreadsheet_key> <worksheet_gid> [<use_cache? 1 or 0>=0]')
    exit(0)

spreadsheet_key = sys.argv[1]
worksheet_gid = int(sys.argv[2])
use_cache = len(sys.argv) < 4 or int(sys.argv[3]) != 0

data = []
cache_path = os.path.dirname(os.path.realpath(__file__)) + '/.cache/{}-{}.json'.format(spreadsheet_key, worksheet_gid)
if use_cache and os.path.exists(cache_path):
    with open(cache_path) as cf:
        data = json.load(cf)
else:
    gc = pygsheets.authorize()
    sh = gc.open_by_key(spreadsheet_key)
    wks = sh.worksheet('id', worksheet_gid)
    data = wks.get_all_values(returnas='matrix')
    with open(cache_path, 'w') as cf:
        json.dump(data, cf)

asct = AsciiTable(data)
print(asct.table)
