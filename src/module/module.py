"""
This file implements module's main logic.
Data outputting should happen here.

Edit this file to implement your module.
"""

from logging import getLogger
from .params import PARAMS
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

log = getLogger("module")

# connect to Apache Cassandra Cluster
cluster = None
if PARAMS['USERNAME'] and PARAMS['PASSWORD']:
    auth_provider = PlainTextAuthProvider(username=PARAMS['USERNAME'], password=PARAMS['PASSWORD'])
    cluster = Cluster(contact_points=[PARAMS['HOST']], port=PARAMS['PORT'], auth_provider=auth_provider)
else:
    cluster = Cluster(contact_points=[PARAMS['HOST']], port=PARAMS['PORT'])
session = cluster.connect()

def module_main(received_data: any) -> str:
    """
    Send received data to the next module by implementing module's main logic.
    Function description should not be modified.

    Args:
        received_data (any): Data received by module and validated.

    Returns:
        str: Error message if error occurred, otherwise None.

    """

    log.debug("Outputting ...")

    try:
        if type(received_data) == dict:
            return insert_data(received_data)
        else:
            for data in received_data:
                resp_error = insert_data(data)
                if resp_error:
                    return resp_error
            return None

    except Exception as e:
        return f"Exception in the module business logic: {e}"

def insert_data(data):
    # build columns artefact
    columns = ""
    for c in PARAMS['COLUMNS']:
        columns += f"{c},"
    columns = "(" + columns[:-1] + ")"

    # build values
    values = ""
    for label in PARAMS['LABELS']:
        if type(data[label]) == str:
            values += f"\'{data[label]}\',"
        else:
            values += f"{data[label]},"
    values = "(" + values[:-1] + ")"

    # build SQL Query
    SQL = f"INSERT INTO {PARAMS['KEYSPACE']}.{PARAMS['TABLE_NAME']} {columns} VALUES {values};"
    log.debug(f'SQL: {SQL}')

    try:
        log.debug("Writing data...")
        session.execute(SQL)

        return None

    except Exception as e:
        return f'Error when inserting to Apache CassandraDB: {e}'
