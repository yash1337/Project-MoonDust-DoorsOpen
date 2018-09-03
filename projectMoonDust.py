from flask import Flask ,render_template ,request, redirect
import sqlite3
from flask import g
from flask import session
import re

app = Flask(__name__)
app.secret_key="b'\x91\x11};\x8f\x84a\x87\xdb*GO\x97\xb6\xb6\xf5\xa2\xaf:\x15v\xaf\xc3\xdc'"

EMAIL_REG=re.compile(r"^[\S]+@[\S]+.[\S]+$")
def email_verify(email):
	return email and EMAIL_REG.match(email)

def generateInstCode(name,university):
	return name.split()[0]+''.join([i[0].upper() for i in university.split()])+"".join(name[name.index(' ') + 1:].split())


@app.before_request
def before_request():
    g.db = sqlite3.connect("db/projectMoonDust.db")

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()

@app.route('/')
def home():
	author="Me"
	name="Yash"
	return render_template('index.html',author=author, name=name)

@app.route('/instructor', methods = ['POST','GET'])
def instructor	():
	return render_template("instructor.html")
    #print("The email address is '" + email + "'")
    #return redirect('/')

@app.route('/instructorSignUp', methods = ['POST','GET'])
def instructorSignUp():
	#return "In the instructorLogIn page"
	return render_template("instructorSignUp.html")
    #print("The email address is '" + email + "'")
    #return redirect('/')


@app.route('/validateInsSignUp', methods = ['POST','GET'])
def validateInsSignUp():
	valid_input=True
	name=request.form['name']
	university=request.form['university']
	email=request.form['email']
	params=dict(name=name,university=university,email=email)

	if not name:
		params['error_name']="Name is required"
		valid_input=False

	if not university:
		params['error_university']="University name is required"
		valid_input=False

	if email:
			if not email_verify(email):
				params['error_email']="That's not an valid email."
				valid_input=False
	else:
		params['error_email']="Email is required"
		valid_input=False

	if not valid_input:
		return render_template("instructorSignUp.html", **params)
	else:
		instCode=generateInstCode(name,university)
		session['name']=name
		session['university']=university
		session['instCode']=instCode
		g.db.execute("INSERT INTO instructors (university, name,instCode) values (?,?,?)",[university,name,instCode])
		g.db.commit()
		return redirect('/instructorGood')

@app.route('/instructorGood', methods = ['POST','GET'])
def instructorGood():
	return render_template("instructorGood.html",name=session['name'])

@app.route('/addClass', methods = ['POST','GET'])
def addClass():
	Class=request.form['Class']
	section=request.form['section']
	ClassCode=request.form['ClassCode']
	valid_input=True
	if not Class:
		params["error_Class"]="Class name is required"
		valid_input=False

	if not section:
		params["error_section"]="Section number is required"
		valid_input=False

	if not ClassCode:
		params["error_ClassCode"]="Class Code is required. This is the code that the students are going to use"
		valid_input=False

	if valid_input:
		return "Successfully added class"
	else:
		return render_template("instructorGood.html", **params)

@app.route('/validateInsCode', methods = ['POST','GET'])
def validateIns():
	login=request.form['instCode']


@app.route('/student', methods = ['POST','GET'])
def studentSignUp():
	return "In the StudentSignUp page"
    #email = request.form['email']
    #print("The email address is '" + email + "'")
    #return redirect('/')

@app.route('/studentLogIn', methods = ['POST'])
def studentLogIn():
	return "In the StudentLogIn	page"
    #email = request.form['email']
    #print("The email address is '" + email + "'")
    #return redirect('/')


if __name__ == '__main__':
    app.run()