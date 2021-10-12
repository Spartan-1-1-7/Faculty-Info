
import re
from flask import Flask, render_template, request, redirect, session, jsonify
from flask.scaffold import F
from flask_session import Session
import mysql.connector

app = Flask(__name__)
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Sreek@r123",
  database="courses_faculty"
)
mycursor=mydb.cursor()
Session(app)

def my_function(x):
  return list(dict.fromkeys(x))

mycursor.execute('SELECT * FROM departments')
departments=mycursor.fetchall()
mycursor.execute('SELECT Semester FROM taughtby')
sem=mycursor.fetchall()
sem = my_function(sem)
mycursor.execute('SELECT * from faculty')
fac=mycursor.fetchall()

@app.route("/")
@app.route("/home")
def begin():
    return render_template("home.html",departments=departments,fac=fac,sem=sem)



@app.route("/login",methods=["GET","POST"])
def login():
  if request.method == "POST" :
    userID=request.form.get("userID")
    password=request.form.get("password")
    mycursor.execute("SELECT * FROM Login_data WHERE userID=%s AND password=%s",(userID,password))
    myvalue=mycursor.fetchone()
    if bool(myvalue) is True:
      session["userID"]=userID
      return redirect("/begin")
    else :
      aler="userID/Password is incorrect! Try again"
      return render_template("login.html",aler=aler)
  return render_template("login.html")


@app.route("/signup",methods=["GET","POST"])
def signup():
  if request.method == "POST" :
    userID = request.form.get("userID")
    password = request.form.get("password")
    phno = request.form.get("phno")
    mycursor.execute("SELECT * FROM Login_data WHERE userID=%s",(userID,))
    myvalue=mycursor.fetchone()
    if bool(myvalue) is False:
      sql = "INSERT INTO Login_data (userID, phno,password) VALUES (%s, %s,%s)"
      val = (userID, phno,password)
      mycursor.execute(sql, val)
      mydb.commit()
      session["userID"]=userID
      return redirect("/begin")
    else :
      aler="userID is already taken Try something different or login into your existing account"
      return render_template("signup.html",aler=aler)
  return render_template("signup.html")

@app.route("/logout",methods=["GET","POST"])
def logout():
  session["userID"] = None
  return redirect("/login")
# DId=""


# @app.route('/coursesearch',methods=["GET","POST"])
# def coursesearch():
#     global DId 
#     DId= request.form.get('depselect')
#     res=""
#     mycursor.execute('SELECT taughtby.CId,courses.CName,taughtby.FId,faculty.FName,taughtby.Semester,taughtby.NumStudents FROM ((taughtby INNER JOIN courses ON courses.CId=taughtby.CId) INNER JOIN faculty ON taughtby.FId=faculty.FId) WHERE courses.DId=%s',(DId,))
#     res=mycursor.fetchall()
#     mycursor.execute('SELECT taughtby.FId,faculty.FName FROM ((taughtby INNER JOIN courses ON courses.CId=taughtby.CId) INNER JOIN faculty ON taughtby.FId=faculty.FId) WHERE courses.DId=%s',(DId,))
#     fac=mycursor.fetchall()
#     fac = my_function(fac)
#     return render_template('home.html',res=res,DId=DId,fac=fac,sem=sem)
# FId=""
# @app.route('/facultysearch',methods=["GET","POST"])
# def facsearch():
#   FId=request.form.get('facultysel')
#   mycursor.execute('SELECT taughtby.CId,courses.CName,taughtby.FId,faculty.FName,taughtby.Semester,taughtby.NumStudents FROM ((taughtby INNER JOIN courses ON courses.CId=taughtby.CId) INNER JOIN faculty ON taughtby.FId=faculty.FId) WHERE( courses.DId=%s AND taughtby.FId=%s)',(DId,FId,))
#   facres=mycursor.fetchall()
#   return render_template('home.html',facres=facres,FId=FId,DId=DId,sem=sem)
# semsearch=""
# @app.route('/semsearch',methods=["GET","POST"])
# def semsearch():
#   global semsearch
#   semsearch=request.form.get('semsearch')
#   mycursor.execute('SELECT taughtby.CId,courses.CName,taughtby.FId,faculty.FName,taughtby.NumStudents FROM ((taughtby INNER JOIN courses ON courses.CId=taughtby.CId) INNER JOIN faculty ON taughtby.FId=faculty.FId) WHERE taughtby.Semester=%s AND taughtby.FId LIKE %s',(semsearch,FId,))
#   courses=mycursor.fetchall()
#   return render_template('home.html',courses=courses,FId=FId,sem=sem,Sem=semsearch,DId=DId)
        
@app.route('/search',methods=["GET","POST"])
def search():
  if request.form.get('facselect')!="" :
    mycursor.execute('SELECT taughtby.CId,courses.CName,taughtby.FId,faculty.FName,taughtby.Semester,taughtby.NumStudents FROM ((taughtby INNER JOIN courses ON courses.CId=taughtby.CId) INNER JOIN faculty ON taughtby.FId=faculty.FId) WHERE( courses.DId LIKE %s AND taughtby.FId LIKE %s AND taughtby.Semester LIKE %s)',('%'+request.form.get('depselect')+'%',request.form.get('facselect'),'%'+request.form.get('semsearch')+'%'))
    result=mycursor.fetchall()
  else:
    mycursor.execute('SELECT taughtby.CId,courses.CName,taughtby.FId,faculty.FName,taughtby.Semester,taughtby.NumStudents FROM ((taughtby INNER JOIN courses ON courses.CId=taughtby.CId) INNER JOIN faculty ON taughtby.FId=faculty.FId) WHERE( courses.DId LIKE %s AND taughtby.FId LIKE %s AND taughtby.Semester LIKE %s)',('%'+request.form.get('depselect')+'%',"%",'%'+request.form.get('semsearch')+'%'))
    result=mycursor.fetchall()
  # print(result)
  return render_template('home.html',result=result,FId=request.form.get('facselect'),DId=request.form.get('depselect'),semester=request.form.get('semsearch'),departments=departments,fac=fac,sem=sem)


  

if __name__ == '__main__':
  app.run(debug=True)