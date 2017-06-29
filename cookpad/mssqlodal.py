# -*- coding: utf-8 -*-


import pymssql

from sqlalchemy import create_engine
from scrapy.conf import settings
import logging

class MsSQLDAL:
    
    def __init__(self):
        logging.basicConfig()
        logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)
        self.mypool = create_engine("mssql+pymssql://%s:%s@%s/%s?charset=utf8" % (
            settings['MSSQL_USER'], settings['MSSQL_PASSWORD'], settings['MSSQL_SERVER'], settings['MSSQL_DB']),\
                                      pool_size=100,  pool_recycle=3600, echo=False)

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


    def execute_none_query(self, query="",sp_params=[],app_name=""):
        """ Execute none query """
        query = query % sp_params
        with self.mypool.connect() as conn:
            trans = conn.begin()
            try:
              conn.execute(query)
              trans.commit()
            except:
                trans.rollback()
                pass
            conn.close()

