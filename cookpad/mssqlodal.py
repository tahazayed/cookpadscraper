# -*- coding: utf-8 -*-


import pymssql
from scrapy.conf import settings

class MsSQLDAL:
    
    def __init__(self):
        pymssql.set_max_connections(1000)
        pass


    def read(self, query="",sp_params=(),app_name=""):
        """ Read from MSSQL and Store into DataFrame """
        results=[]
        # Connect to MSSQL
        with pymssql.connect(server=settings['MSSQL_SERVER'], user=settings['MSSQL_USER'], \
                             password=settings['MSSQL_PASSWORD'], database=settings['MSSQL_DB'] \
                , autocommit=True, charset='UTF-8', appname=app_name) as conn:
            with conn.cursor(as_dict=True) as cursor:
               try:
                    cursor.callproc(query, sp_params)
                    results = list(cursor)
               except:
                    pass
               cursor.close()
            conn.close()
        return results


    def execute_none_query(self, query="",sp_params=(),app_name=""):
        """ Execute none query """

        with pymssql.connect(server=settings['MSSQL_SERVER'], user=settings['MSSQL_USER'], \
                             password=settings['MSSQL_PASSWORD'], database=settings['MSSQL_DB'] \
                , autocommit=True, charset='UTF-8', appname=app_name) as conn:
            with conn.cursor(as_dict=True) as cursor:
               try:
                   cursor.callproc(query, sp_params)
                   conn.commit()
               except:
                   pass
               cursor.close()
            conn.close()

