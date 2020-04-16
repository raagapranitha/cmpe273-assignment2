import sqlite3
from flask import Flask, escape, request,jsonify
import json

app = Flask(__name__)

conn = sqlite3.connect('test.db')
conn.row_factory = sqlite3.Row
c= conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS scantron_test(
					scantron_id integer NOT NULL PRIMARY KEY,
					name text,
					subject text,
					`1` text,
					`2` text,
					`3` text,
					`4` text,
					`5` text
					)""")

def insert_scantron(scantron) :
	columns = ', '.join( "`"+str(x).replace('/', '_') + "`" for x in scantron_dict.keys())
	values = ', '.join("'" + str(x).replace('/', '_') + "'" for x in scantron_dict.values())
	sql = "INSERT INTO %s ( %s ) VALUES ( %s );" % ('scantron_test', columns, values)
	c.execute(sql)
	conn.commit()

def print_rows(table_name):
	c.execute("SELECT * FROM "+table_name)
	r = c.fetchone()
	column_names= r.keys()
	print("IN column names ")
	print(column_names)
	new_dict={}
	for i in column_names:
		new_dict[str(i)] = r[str(i)]
	print("After reading to dict ")
	print(new_dict)

scantron_dict = {'name':'test_student','subject':'cmpe273','1':'A',"2":'B','3':'C','4':'D','5':'E'}
insert_scantron(scantron_dict)
print_rows('scantron_test')



conn.close()
