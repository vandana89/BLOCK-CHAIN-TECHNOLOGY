from flask import Flask,render_template,request,url_for,flash,redirect,session
import pandas as pd
import os
from hashlib import sha256
import hashlib
import json
from time import time
import datetime

import mysql.connector
db=mysql.connector.connect(user='root',host='localhost',password='Tejadeep@1755',port=3306,database='charity')
cur=db.cursor()

app=Flask(__name__)
app.secret_key="kjvnsdjfbv84ry3478AMcjksdcver8t54561489xcmuioc"
app.config['upload']=r"\upload"



class Blockchain(object):
    def __init__(self):
        self.chain=[]
        self.pending_transactions=[]
        self.new_block(previous_hash="the time 03/jan/2009",proof=100)

    def new_block(self, proof, previous_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.pending_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1])
        }

        self.pending_transactions = []
        self.chain.append(block)
        return block

    @property
    def last_block(self):
        return self.chain[-1]

    def new_transaction(self, sender, recipient, amount):
        transaction = {
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        }
        self.pending_transactions.append(transaction)
        return self.last_block['index'] + 1
    def hash(self,block):
        string_object=json.dumps(block,sort_keys=True)
        block_string=string_object.encode()
        raw_hash=hashlib.sha256(block_string)
        hex_hash=raw_hash.hexdigest()
        return hex_hash

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/charitylog',methods=['POST','GET'])
def charitylog():
    if request.method =='POST':
        sql="select * from charityinformation where Charityemail=%s and Charitypassword=%s"
        val=(request.form['charity_mailid'],request.form['charity_password'])
        session['charityemail']=request.form['charity_mailid']
        cur.execute(sql,val)
        data=cur.fetchall()
        db.commit()
        if len(data)==0:
            flash("details are not valid......!","success")
            return render_template('charitylog.html')
        else:
            return render_template('charityhome.html',charityname=data[0][1])
    return render_template('charitylog.html')

@app.route('/charityregistration',methods=['POST','GET'])
def charityregistration():
    if request.method=='POST':
        Charity_name=request.form['Charity_name']
        Charity_email=request.form['Charity_email']
        charity_password=request.form['charity_password']
        charity_confirmpassword=request.form['charity_confirmpassword']
        charity_address=request.form['charity_address']
        charity_contact=request.form['charity_contact']
        if charity_password == charity_confirmpassword :
            sql="select * from charityinformation where Charityemail=%s and Charitypassword=%s"
            val=(Charity_email,charity_password)
            cur.execute(sql,val)
            data=cur.fetchall()
            db.commit()
            if len(data) ==0:
                status='pending'
                sql="insert into charityinformation(Charityname,Charityemail,Charitypassword,Charityaddress,Charitycontact,status)values(%s,%s,%s,%s,%s,%s)"
                val=(Charity_name,Charity_email,charity_password,charity_address,charity_contact,status)
                cur.execute(sql,val)
                db.commit()
                return render_template('charitylog.html')
            else:
                flash("Charity Details already exists","success")
                return redirect('charityregistration')
    return render_template('charityregistration.html')

@app.route('/viewdonations')
def viewdonations():
    sql="select Charityname,Charityemail,Charityaddress,Useremail from donation where Status='accept'"
    data=pd.read_sql_query(sql,db)
    return render_template("viewdonations.html",cols=data.columns.values,rows=data.values.tolist())


@app.route('/donationrequest')
def donationrequest():
    sql="select Slno,Charityname,Charityemail,Useremail from donation where Status='pending'"
    data=pd.read_sql_query(sql,db)
    return render_template("donationrequest.html",cols=data.columns.values,rows=data.values.tolist())

@app.route('/acceptrequest/<c>')
def acceptrequest(c=0):
    sql="update donation set Status='accept' where Slno='%s' and status='pending'"%(c)
    cur.execute(sql)
    db.commit()
    return render_template('charitydetails.html')

@app.route('/charitybanking',methods=["POST","GET"])
def charitybanking():
    if request.method=="POST":
        bankaccount=request.form['accountnumber']
        ifsccode=request.form['accountIFSCcode']
        print(bankaccount)
        print(ifsccode)
        print(session['charityemail'])
        status="pending"
        sql="insert into transactiondetails (Charityemail,Charityaccountnumber,charityifsccode,status)values(%s,%s,%s,%s)"
        val=(session['charityemail'],bankaccount,ifsccode,status)
        cur.execute(sql,val)
        db.commit()
        flash("Account Details sent to the user","success")

    return render_template("charityinfo.html")

@app.route("/charitylogout")
def charitylogout():
    return redirect("/")


@app.route('/admin',methods=["POST","GET"])
def admin():
    if request.method=="POST":
        cloud_mailid=request.form['admin_mailid']
        cloud_password=request.form['admin_password']
        if cloud_mailid=="admin@gmail.com" and cloud_password =="admin":
            return render_template("adminhome.html",x="admin")
    return render_template('admin.html')

@app.route("/viewallcharities")
def viewallcharities():
    sql="select Slno,Charityname,Charityemail,Charityaddress,Charitycontact from charityinformation"
    data=pd.read_sql_query(sql,db)
    return render_template("allcharities.html",cols=data.columns.values,rows=data.values.tolist())


@app.route("/viewallusers")
def viewallusers():
    sql = "select Id,Username,useremail,age,contact,address from userinformation"
    data = pd.read_sql_query(sql, db)
    return render_template('allusers.html',cols=data.columns.values,rows=data.values.tolist())

@app.route("/alldonations")
def alldonations():
    sql="select * from donation"
    data=pd.read_sql_query(sql,db)
    return render_template("alldonations.html",cols=data.columns.values,rows=data.values.tolist())

@app.route('/adminlogout')
def adminlogout():
    return redirect('/')

@app.route("/userreg",methods=["POST","GET"])
def userreg():
    if request.method=="POST":
        user_name=request.form['user_name']
        user_email=request.form['user_email']
        password=request.form['password']
        confirmpassword=request.form['confirmpassword']
        age=request.form['age']
        contact=request.form['contact']
        address=request.form['address']
        status='pending'
        if password == confirmpassword:
            sql="select * from userinformation where useremail='%s' and password='%s'"%(user_email,password)
            cur.execute(sql)
            data=cur.fetchall()
            db.commit()
            if len(data)==0:
                sql="insert into userinformation (Username,useremail,password,age,contact,address,Status)values(%s,%s,%s,%s,%s,%s,%s)"
                val=(user_name,user_email,password,age,contact,address,status)
                cur.execute(sql,val)
                db.commit()
                return redirect(url_for('userlog'))
        else:
            flash("something went wrong", "success")
            return redirect(url_for('userreg'))
    return render_template('userreg.html')

@app.route('/userlog',methods=["GET","POST"])
def userlog():
    if request.method=='POST':
        user_email=request.form['User_email']
        session['user_email']=user_email
        user_password=request.form['user_password']
        sql="select * from userinformation where useremail=%s and password=%s"
        val=(user_email,user_password)
        cur.execute(sql,val)
        data=cur.fetchall()
        db.commit()
        if len(data)!= 0:
            return render_template('userhome.html',username=data[0][1])
        else:
            flash("Credentials are not valid.....!","success")
            return redirect('userlog')
    return render_template('userlog.html')


@app.route('/viewcharities')
def viewcharities():
    sql="select Slno,Charityname,Charityemail,Charityaddress,Charitycontact from charityinformation"
    data=pd.read_sql_query(sql,db)
    return render_template('viewcharities.html',cols=data.columns.values,rows=data.values.tolist())

@app.route('/donate/<v>')
def donate(v=0):
    print(v)
    print(session['user_email'])
    sql="select * from charityinformation where Slno='%s'"%(v)
    cur.execute(sql)
    data=cur.fetchall()
    db.commit()
    print(data)
    charity_name=data[0][1]
    charity_email=data[0][2]
    charity_address=data[0][4]
    status='pending'
    sql="insert into donation (Charityname,Charityemail,Charityaddress,Useremail,status)values(%s,%s,%s,%s,%s)"
    val=(charity_name,charity_email,charity_address,session['user_email'],status)
    cur.execute(sql,val)
    db.commit()
    sql = "select Slno,Charityname,Charityemail,Charityaddress,Charitycontact,status from charityinformation"
    data = pd.read_sql_query(sql, db)
    flash("Your request sent successfuly","success")
    return render_template("viewcharities.html",cols=data.columns.values,rows=data.values.tolist())


        # filedata=request.files['filename']
        # x=filedata.filename
        # fileda = filedata.read()
        # pathfile=os.path.join("upload/",x)
        # filedata.save(pathfile)
        # datetoday=datetime.datetime.now().date()
        # status='pending'
        # sql="insert into donation(Filename,Information,Date,Status)values(%s,AES_ENCRYPT(%s,'key'),%s,%s)"
        # val=(x,fileda,datetoday,status)
        # cur.execute(sql,val)
        # db.commit()
        # flash("file Uploaded successfuly","success")
    # return render_template('donate.html',v=v)

@app.route('/charityresponse')
def charityresponse():
    data=pd.read_sql_query("select Id,Charityemail,Charityaccountnumber,charityifsccode from transactiondetails",db)
    return render_template('charityresponse.html',cols=data.columns.values,rows=data.values.tolist())

@app.route("/makedonate/<v>",methods=["POST","GET"])
def makedonate(v=0):
    if request.method=="POST":
        amount=request.form['amount']
        Username=request.form['Username']
        usercardnumber=request.form['usercardnumber']
        expiredate=request.form['expiredate']
        cvv=request.form['cvv']

        blockchain = Blockchain()
        t1 = blockchain.new_transaction(Username, session['charityemail'],amount)
        blockchain.new_block(1)
        for i in blockchain.chain:
            if i.get('transactions') == []:
                pass
            else:
                f=open("files/"+session['user_email']+".txt","w+")
                f.write(str(i)+'\n')
        sql="select Userename,usercardnumber,expiredate,cvv,amount from transactiondetails  where Id=%s"%(v)
        cur.execute(sql)
        data=cur.fetchall()
        db.commit()

        if data==[]:
            sql="update transactiondetails set Userename=%s,usercardnumber=%s,expiredate=%s,cvv=%s,amount=%s where Id=%s"
            val=(Username,usercardnumber,expiredate,cvv,amount,v)
            cur.execute(sql,val)
            db.commit()
        else:
            sql="select Charityemail,CharityaccountNumber,charityifsccode from transactiondetails where Id='%s'"%(v)
            cur.execute(sql)
            data=cur.fetchall()
            db.commit()
            print(data)
            data=[i for x in data for i in x]
            print(data)
            x=data[0]
            y=data[1]
            z=data[2]
            sql="insert into transactiondetails(Charityemail,CharityaccountNumber,charityifsccode,Userename,usercardnumber,expiredate,cvv,amount)values(%s,%s,%s,%s,%s,%s,%s,%s) "
            val=(x,y,z,Username,usercardnumber,expiredate,cvv,amount)
            cur.execute(sql,val)
            db.commit()
    return render_template("makedonate.html",v=v)


@app.route("/userlogout")
def userlogout():
    return redirect("/")



if __name__=="__main__":
    app.run(debug=True,port=8000)