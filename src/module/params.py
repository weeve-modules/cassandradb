from os import getenv

PARAMS = {
    "HOST": getenv("HOST", ""),
    "PORT": int(getenv("PORT", "")),
    "USERNAME": getenv("USERNAME", ""),
    "PASSWORD": getenv("PASSWORD", ""),
    "KEYSPACE": getenv("KEYSPACE", ""),
    "TABLE_NAME": getenv("TABLE_NAME", ""),
    "COLUMNS": getenv("COLUMNS", ""),
    "LABELS": getenv("LABELS", ""),
}

# parse columns and labels
if PARAMS['COLUMNS']:
    PARAMS['COLUMNS'] = [header.strip() for header in PARAMS['COLUMNS'].split(',')]
else:
    PARAMS['COLUMNS'] = None

if PARAMS['LABELS']:
    PARAMS['LABELS'] = [label.strip() for label in PARAMS['LABELS'].split(',')]
else:
    PARAMS['LABELS'] = None
