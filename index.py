#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bottle import route, run, template
from mger import db
import sqlite3
@route('/')
def index():
    html=''
    con = sqlite3.connect("/www/wwwroot/bottle/peis.db")
    cur = con.cursor()
    rows = None
    error = None
    try:
        res = cur.execute("SELECT * FROM peis_combo WHERE id>:id",{"id":0})
        rows = res.fetchall()
    except sqlite3.Error as e:
        error = str(e)
    finally:
        con.close()
    if error:
        return '<b>'+error+'</b>!'
    for row in rows:
        html += '<p>' + str(row[0]) + '</p>'
    return '<div>'+html+sql+'</div>!'
@route('/hello/<name>')
def hello(name):
    db1 = db('/www/wwwroot/bottle/peis.db')
    html=''
    error=''
    error,sql = db1.query("delete from `peis_combo`",{"code":"xxx","name":"未知"})
    html+=str(sql)
    error,rows = db1.query("SELECT * FROM peis_combo WHERE id>:id ORDER BY id ASC",{"id":0})
    if error:
        return '<b>'+error+'</b>!'
    for row in rows:
        html += '<p>' + str(row['id']) + ',' + str(row['code']) + ',' + str(row['name'] or '') + '</p>'
    return template(html+'<b>Hello {{name}}</b>!', name=name)
@route('/nihao/<name>')
def nihao(name):
    return template('<b>Nihao {{name}}</b>!', name=name)
run(host='0.0.0.0', port=9000)
