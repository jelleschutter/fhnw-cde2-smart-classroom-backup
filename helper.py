import getopt
import sys
from pathlib import Path

def get_opts():
    aopts = getopt.getopt(sys.argv[1:], '', ['username=', 'password=', 'hostname=', 'port=', 'service='])

    opts = {}
    for opt in aopts[0]:
        if opt[0].startswith('--'):
            opts[opt[0][2:]] = opt[1]
        else:
            opts[opt[0]] = opt[1]
    return opts

def ensure_dir(path):
    Path(path).mkdir(parents=True, exist_ok=True)