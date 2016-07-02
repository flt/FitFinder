#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from flask import Flask
from flask import request
import MySQLdb
from flask import json ,jsonify;
app = Flask(__name__)


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello world!')

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)

@app.route('/')
def hello():

    """Return a friendly HTTP greeting."""
    return 'Hello World!'

#login
@app.route('/signIn/',methods=['POST'])
def login():
	if request.method == 'POST':
		username = request.form['username']
		passwd = request.form['pwd'];
		try:
			conn = MySQLdb.connect(host = '166.111.82.59', user = 'fitfinder', passwd = 'fitfinder', db = 'fitfinder')
		except Exception, e:
				print e
				sys.exit()
		cursor = conn.cursor();
		cursor.execute("select * from userinfo where username = %s", (username,))
		if not cursor.fetchone():
			error = 201
			return error
			#print "user does not exist!"
		else:
			cursor.execute("select * from userinfo where username = %s", (username,))
			uinfo = cursor.fetchone()
			print uinfo[2]
			if passwd == uinfo[2]:
				data={
				'height': uinfo[3],
				'weight': uinfo[4],
				'gender': uinfo[9],
				'BodyPartScore':[uinfo[6],uinfo[8],uinfo[7]]
				}
				return jsonify({'result':data}),200;
				
			else:
				error = 201
				return error
				#print "Password error"
	cursor.close()
	conn.close()

@app.route('/signUp/',methods=['POST'])	
def register():
	if request.method == 'POST':
		userName = request.form['userName']
		pwd = request.form['pwd']
		gender = request.form['gender']
		weight = request.form['weight']
		height = request.form['height']
		mHeight = height / 100
		initScore = weight // (mHeight * mHeight)

		try:
			conn = MySQLdb.connect(host = '166.111.82.59', user = 'fitfinder', passwd = 'fitfinder', db = 'fitfinder')
		except Exception, e:
				print e
				sys.exit()
		cursor = conn.cursor();
		cursor.execute("insert into userinfo (userName,userPwd,height,weight,armScore,legScore,coreSore,sex) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)",(userName,pwd,height,weight,time,initScore,initScore,initScore,gender,))
		cursor.execute("select * from uinfo where username = %s", (userName,))
		uinfo = cursor.fetchone()
		data={
				'height': uinfo[3],
				'weight': uinfo[4],
				'gender': uinfo[9],
				'BodyPartScore':[uinfo[6],uinfo[8],uinfo[7]]
		}
		return jsonify({'result':data}),200;
		cursor.close()
		conn.close()

@app.route('/getBodyScore/',methods=['GET'])
def getBodyScore():
	pass

@app.route('/getRecordInfo/',methods=['GET'])
def getRecordInfo():
	pass

@app.route('/searchByPart/',methods=['GET'])
def searchByPart():
	pass

@app.route('/submitPlay/',methods=['POST'])
def submitPlay():
	pass

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.', 404


@app.errorhandler(500)
def application_error(e):
    """Return a custom 500 error."""
    return 'Sorry, unexpected error: {}'.format(e), 500

if __name__ == '__main__':
    app.run()
