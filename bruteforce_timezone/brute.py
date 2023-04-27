import os
import sys
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo


def script_path():
    """set current path, to script path"""
    current_path = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(current_path)
    return current_path
    
    
def utcoffset(tz: ZoneInfo):
    dt = datetime(2023, 1, 1)
    return tz.utcoffset(dt).total_seconds()
    
    
script_path()

# https://github.com/python/tzdata/blob/master/src/tzdata/zones
# https://raw.githubusercontent.com/python/tzdata/master/src/tzdata/zones
zones = Path('zones.txt').read_text().splitlines()

needed_pairs = [
    ('north_pole', 3600),
    ('south_pole', 3600),
    ('cape_canaveral', -18000.0),
]

# bruteforce
for (name, value) in needed_pairs:
    for zone in zones:
        try:
            zone_obj = ZoneInfo(zone)
        except Exception:
            print(f'error for: {zone}')
            continue
        if utcoffset(zone_obj) == value:
            print('FOUND!')
            print(f'    {name}: {zone}')
            break
            