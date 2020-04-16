from flask import Flask, escape, request,jsonify
import json
import sqlite3 
import copy
from collections import OrderedDict
from database import print_rows

app = Flask(__name__)

# conn = sql.connect('database.db')
DATABASE = 'database.db'
conn = sqlite3.connect(DATABASE)
conn.row_factory = sqlite3.Row
c= conn.cursor()
print('Opened database successfully')

c.execute("""CREATE TABLE  IF NOT EXISTS scantron_student_answers(
					scantron_id integer NOT NULL PRIMARY KEY,
					scantron_url text,
					name text,
					subject text,
					score integer,
					`1` text,
					`2` text,
					`3` text,
					`4` text,
					`5` text
					)""")

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

conn.commit()
print('Table scantron_student_answers created successfully')


c.execute("""CREATE TABLE  IF NOT EXISTS scantron_keys(
					test_id integer,
					subject text,
					`1` text,
					`2` text,
					`3` text,
					`4` text,
					`5` text
					)""")
conn.commit()
print('Table scantron_keys created successfully')
# query = "INSERT INTO scantron_student_answers VALUES (1,'https://sdfjo','test','cmpe273',40,'a','b','c','d','e')"
# query2 = "INSERT INTO scantron_keys VALUES (1,'cmpe273','a','b','c','d','e')"
# cursor = conn.cursor()
# # cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
# # print(cursor.fetchall())
# cursor.execute(query)
# cursor.execute(query2)
# cursor.execute("SELECT * FROM scantron_student_answers WHERE `subject` = 'cmpe273'")
# result = cursor.fetchall()
# for row in result:
# 	print(row[1])
# cursor.execute("SELECT * FROM scantron_keys WHERE `subject` = 'cmpe273'")
# result = cursor.fetchall()
# for row in result:
# 	print(row[1])

stud ={'scantron_url':'https://sfjie',
		'name':'test','subject':'cmpe273','score':40,'1':'A','2':'B',
		'3':'C','4':'E','5':'C'}
scantron_dict = {'name':'test_student','subject':'cmpe273','1':'A',"2":'B','3':'C','4':'D','5':'E'}

@app.route('/api/test/testing',methods=["GET"])
def getStudents():
	stud_dict ={}
	keys_dict ={}
	insert_dict_into_table('scantron_test',scantron_dict)
	stud_dict = print_rows('scantron_student_answers')
	# keys_dict = getDict('scantron_keys')
	# new_dict ={}
	# for i in range(1,51):
	# 	temp_dict={}
	# 	temp_dict['expected'] = keys_dict[str(i)]
	# 	temp_dict['actual'] = stud_dict[str(i)]
	return jsonify(stud_dict),201



# @app.route('/api/test/<int:test_id>',methods=["POST"])
# def create_student_scantron(test_id): 
# 	student_scantron_dict = getDict(scantron_student_answers)

# @app.route('/api/tests/<int:test_id>/scantrons',methods=["GET"])
# def getAllScantrons(test_id):
	


@app.route('/api/tests',methods=["POST"])
def create_key():
	dict_from_post = {}
	dict_to_database= {}
	temp ={}
	test_id = 1 
	dict_from_post['test_id'] = test_id
	dict_from_post['subject'] = get_data_from_input(request.data.decode('utf8'),'subject')
	dict_to_database = get_data_from_input(request.data.decode('utf8'),'answer_keys')
	temp = dict(dict_to_database)
	temp.update(dict_from_post)
	dict_to_database = temp
	dict_from_post['submissions'] =[] 
	dict_from_post['answer_keys'] = get_data_from_input(request.data.decode('utf8'),'answer_keys')
	
	insert_dict_into_table('scantron_keys',dict_to_database)
	return jsonify(dict_from_post),201


def calculate_Score(keys,student_answers):
	score = 0 
	for i in range(1,51):
		if keys[str(i)] == student_answers[str(i)] :
			score+=1
	return score

def insert_dict_into_table(table_name, student_dict):
	columns = ', '.join( "`"+str(x).replace('/', '_') + "`" for x in student_dict.keys())
	values = ', '.join("'" + str(x).replace('/', '_') + "'" for x in student_dict.values())
	query = "INSERT INTO %s ( %s ) VALUES ( %s );" % (table_name, columns, values)
	with sqlite3.connect(DATABASE) as conn:
		c = conn.cursor()
		c.execute(query)
		conn.commit()

def getDict(table_name):
	column_names =[]
	query = "SELECT * FROM "+table_name
	with sqlite3.connect(DATABASE) as conn:
		c= conn.cursor()
		c.execute(query)
		r = c.fetchall()
		print("r = c.fectchone()"+str(r))
		column_names = (r.keys())
		print(column_names)
		for i in column_names:
			new_dict[str(i)] = r[str(i)]
	return new_dict

def get_data_from_input(input_data,s):
	new_dict=json.loads(input_data)
	return new_dict[s]
    
if __name__=="__main__":
	app.run(Debug=True,port=8080)
