import boto3

class RDS_lsy:
    def __init__(self, type='rds', region='ca-central-1',
                 key_id='AKIAVQQFIHD7VWDDT76Z',
                 access_key='Y2nIOsZ6ylucQj8oDWQ9998zjADTtHdFIQkxXywP'):
        self.rds = boto3.client(type,
                    region,
                    aws_access_key_id=key_id,
                    aws_secret_access_key=access_key)

    def test_connect(self):
        try:
            dbs = self.rds.describe_db_instances()
            print('connect successfully')
            for db in dbs['DBInstances']:
                print('{}@{}: {} {}'.format(db['MasterUsername'], db['Endpoint']['Address'],
                                db['Endpoint']['Port'], db['DBInstanceStatus']))
        except Exception as e:
            print(e)

        return self

# key_id = AKIAVQQFIHD7W5MBS54L
# access_key = +BzPXOKwytt+ZA0z8zn/4v+p0c5AwV7Vai8lCNWR

def main():
    l = RDS_lsy()
    l.test_connect()

if __name__ == "__main__":
    main()



'''import pandas as pd
import pymysql


host = "testdb1.cwdxpxelx0qi.ca-central-1.rds.amazonaws.com"
port = 3306
dbname = "TGH"
user = "admin"
password = "RDSLSY1123"
conn = pymysql.connect(host, user=user, port=port, passwd=password, db=dbname)

cursor = conn.cursor()
sql_txt = "insert into user_info (name, password) values ('abbx', '1123');"
cursor.execute(sql_txt)
conn.commit()'''
