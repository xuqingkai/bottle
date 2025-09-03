#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import sqlite3
class db(object):
    def __init__(self, dbfile):
        self._connect_string = dbfile
        
    def query(self, sql, params = ()):
        data = None
        error = None
        try:
            connect = sqlite3.connect(self._connect_string)
            connect.row_factory = sqlite3.Row
            cursor = connect.cursor()
            if sql.upper().startswith('SELECT '):
                cursor.execute(sql, params)
                if sql.upper().endswith(' LIMIT 1'):
                    data = cursor.fetchone()
                else:
                    data = cursor.fetchall()
            elif sql.upper().startswith('INSERT INTO '):
                if isinstance(params,list):
                    if len(params)>0:
                        if isinstance(params[0],dict):
                            sql += '('+(','.join(params[0].keys()))+') VALUES (:'+(',:'.join(params[0].keys()))+')'
                        else:
                            sql += ' VALUES ('+(','.join(['?' for _ in params[0]]))+')'
                    else:
                        pass
                elif ' VALUES ' not in sql.upper():
                    if isinstance(params,dict):
                        sql += '('+(','.join(params.keys()))+') VALUES (:'+(',:'.join(params.keys()))+')'
                    else:
                        sql += ' VALUES ('+(','.join(['?' for _ in params]))+')'
                else:
                    pass
                cursor.execute(sql,params)
                connect.commit()
                data = cursor.rowcount
            elif sql.upper().startswith('UPDATE '):
                if ' SET ' not in sql.upper():
                    sql = sql.replace(' WHERE ',' SET '+(', '.join([key+'=:'+key for key in params]))+' WHERE ')
                cursor.execute(sql, params)
                connect.commit()
                data = cursor.rowcount
            elif sql.upper().startswith('DELETE '):
                if ' SET ' not in sql.upper():
                    sql += ' WHERE ' +(' AND '.join([key+'=:'+key for key in params]))
                cursor.execute(sql, params)
                connect.commit()
                data = cursor.rowcount
            else:
                cursor.execute(sql, params)
                connect.commit()
        except Exception as e:
            error = str(e)
            if connect: connect.rollback()
        finally:
            connect.close()
        return error, data
    
    def test(self):
        return "sadasd"
