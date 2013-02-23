#!/usr/bin/env python
# -*- coding: utf-8 -*-
# cma - 2013

import argparse
import pymssql

parser = argparse.ArgumentParser(description="Check master MSSQL server for a specific database.")
parser.add_argument("-t", "--timeout", action="store", type=int, help="Timeout for connection and login in seconds", default="60", dest="timeout")
parser.add_argument("--query-timeout", action="store", type=int, help="Query timeout in seconds", default="60", dest="query_timeout")
parser.add_argument("-H", "--host", action="store", help="Host name or IP address to connect to", required=True, dest="host")
parser.add_argument("-p", "--port", action="store", type=int, help="SQL Server port number (only change if you know you need to)", default=1433, dest="port")
parser.add_argument("-U", "--user", action="store", help="User name to connect as (does not support Windows built in or Active Directory accounts)", required=True, dest="user")
parser.add_argument("-P", "--password", action="store", help="Password to for user you are authenticating as", required=True, dest="password")
parser.add_argument("-D", "--database", action="store", help="Database name that need to be verified", required=True, dest="dbname")
parser.add_argument("-v", "--verbose", action="store_true", help="Turn script output on", default=False, dest="verbose")
results = parser.parse_args()

connect_host = "%s:%s" % (results.host,str(results.port))

try:
    conn = pymssql.connect(user = results.user, password = results.password, host = connect_host, timeout = results.query_timeout, login_timeout = results.timeout)
except Exception, err:
    if results.verbose:
        print "Error connecting to the server: %s" % str(err)
    exit(1)

tsql_cmd = """
SELECT
    CASE COUNT(d.name) WHEN 1 THEN 0 ELSE 1 END AS MIRROR
FROM
    sys.database_mirroring m
JOIN
    sys.databases d ON m.database_id = d.database_id
WHERE
    mirroring_state_desc IS NOT NULL AND
    mirroring_role_desc = 'PRINCIPAL' AND
    name = '%s'
 """ % results.dbname

cur = conn.cursor()
cur.execute(tsql_cmd)
exit(cur.fetchone()[0])
conn.close()
