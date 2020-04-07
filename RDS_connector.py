import pandas as pd
import pymysql

class rds_connect_lsy:

    def __init__(self):
        host = "testdb1.cwdxpxelx0qi.ca-central-1.rds.amazonaws.com"
        port = 3306
        dbname = "TGH"
        user = "admin"
        password = "RDSLSY1123"
        self.conn = pymysql.connect(host, user=user, port=port, passwd=password, db=dbname)
