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

def main():
    sql_list_veri_code = "select * from test;"
    cn = rds_connect_lsy()
    re = pd.read_sql_query(sql_list_veri_code, con=cn.conn)
    print(re)
if __name__ == '__main__':
    main()

