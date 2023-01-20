from os import getenv

PARAMS = {
    "HOST": getenv("HOST", ""),
    "PORT": int(getenv("PORT", "")),
    "USERNAME": getenv("USERNAME", ""),
    "PASSWORD": getenv("PASSWORD", ""),
    "KEYSPACE": getenv("KEYSPACE", ""),
    "TABLE_NAME": getenv("TABLE_NAME", ""),
    "COLUMNS": "(" + ",".join([c.strip() for c in getenv("COLUMNS", "").split(",")]) + ")",
    "LABELS": [label.strip() for label in getenv("LABELS", "").split(',')]
}
