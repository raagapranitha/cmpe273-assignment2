from flask_sqlalchemy import SQLAlchemy
from flask import Flask, escape, request,jsonify,send_file
import json
from typing import Dict
import os.path
from os.path import isfile,join
# from werkzeug import secure_filename

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db =SQLAlchemy(app)

AnswerKey =["A","B","C","D","E"]
curr_dir = os.getcwd()
uploads_dir = os.path.join(curr_dir,'uploads')
os.makedirs(uploads_dir,exist_ok=True)

class Test(db.Model):
	__tablename__='tests'
	_test_id = db.Column("test_id",db.Integer,primary_key=True)
	subject = db.Column("subject",db.String(100), nullable=False)
	answer_keys = db.Column("answer_keys",db.PickleType, nullable=False)
	submissions = db.Column("submissions", db.PickleType, nullable=False)

	@property
	def serialize(self):
		return {
				"test_id" :self._test_id,
				"subject":self.subject,"answer_keys":self.answer_keys,
				"submissions":self.submissions
		}

class Submission(db.Model):
	__tablename__='submissions'
	_scantron_id=db.Column("scantron_id",db.Integer,primary_key=True)
	name = db.Column("name",db.String(100))
	subject = db.Column("subject",db.String(100), nullable=False)
	score =db.Column("Score",db.Integer,default=0)
	scantron_url=db.Column("Scantron_url",db.String(100))
	result = db.Column("result",db.PickleType)

	@property
	def serialize(self):
		return {
				"scantron_id" :self._scantron_id,"name":self.name,
				"subject":self.subject,"scantron_url":self.scantron_url,
				"score":self.score,"result":self.result
		}



@app.route("/api/tests", methods=["POST"])
def create_table_keys():
	input_data = json.loads(request.data.decode('utf8'))
	subject = input_data['subject']
	answer_keys = input_data['answer_keys']
	submissions= []
	if valid_test(answer_keys):
		db.session.add(Test(subject = subject, answer_keys = answer_keys,submissions=submissions))
		db.session.commit()
		tests = Test.query.filter_by(subject=subject).first()
		return jsonify(tests.serialize),201
	else:
		return jsonify("Test not valid")


@app.route("/api/tests/<int:test_id>/scantrons", methods=["POST"])
def create_submission(test_id):


	curr_dir = os.getcwd()
	file = request.files['file']
	file.save(os.path.join(curr_dir+"/uploads", file.filename))
	curr_dir = os.getcwd()
	path = os.path.join(curr_dir+"/uploads",file.filename)
	with open(path) as f:
		input_data =json.load(f)

	scantron_url = "http://localhost:5000/files/"+file.filename
	result,score = getResults(test_id,input_data['answers'])
	db.session.add(Submission(name=input_data['name'],subject = input_data['subject'], 
		score=score,scantron_url=scantron_url,result = result))
	db.session.commit()
	submissions = Submission.query.filter_by(subject=input_data['subject']).first()
	return jsonify(submissions.serialize),201
	

@app.route('/files/<string:filename>', methods=['GET'])
def download_file(filename):
	curr_dir = os.getcwd()
	path = os.path.join(curr_dir+"/uploads",filename)
	return send_file(path, as_attachment=True)

@app.route("/api/tests/<int:test_id>", methods=["GET"])
def getAll(test_id):
	tests = Test.query.filter_by(_test_id=test_id).first()
	data = tests.serialize
	submissions = Submission.query.filter_by(subject=data['subject'])
	for sub in submissions:
		scantron = sub.serialize
		data['submissions'].append(scantron)
	return jsonify(data)


def valid_test(answer_keys):
	print(len(answer_keys.keys()))
	if len(answer_keys.keys())!=50:
		return False
	for val in answer_keys.values():
		if val not in AnswerKey:
			return False
	return True

def getResults(test_id,answers_scantron):
	results={}
	score = 0
	query_res = Test.query.filter_by(_test_id=test_id).first()
	print(query_res)
	test = query_res.serialize
	answer_keys = test['answer_keys']
	for i in range(1,51):
		new_dict={}
		new_dict['actual'] = answers_scantron[str(i)]
		new_dict['expected'] = answer_keys[str(i)]
		results[str(i)] = new_dict
		if answer_keys[str(i)] == answers_scantron[str(i)]:
			score+=1
	return results,score


db.create_all()

