# -*- coding: utf-8 -*-


import pymssql
from scrapy.conf import settings

class MsSQLDAL:
    
    def __init__(self):
       pass

    def _open_connection(self):
        self.client = pymssql.connect(server=settings['MSSQL_SERVER'], user=settings['MSSQL_USER'],\
                                      password=settings['MSSQL_PASSWORD'], database=settings['MSSQL_DB'],\
                                      autocommit=True)

    def _close_connection(self):
        self.client.close()  

    def read_mssql(self, query=""):
        """ Read from MSSQL and Store into DataFrame """
        results=[]
        # Connect to MSSQL
        self._open_connection()
        with self.client.cursor(as_dict=True) as cursor:
            cursor.execute(query)
            results=list(cursor.fetchall())
            """
            for row in cursor:
                results.append(row)
            """
        #close connection
        self._close_connection()
        return results


