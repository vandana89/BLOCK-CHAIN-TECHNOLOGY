from flask import Flask,render_template,request,url_for,flash,redirect,session
from blockchain import Blockchain_for_user,Blockchain_for_transaction
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

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

blockchain=Blockchain_for_user()
transaction_blockchain=Blockchain_for_transaction()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/charityhome/<chaname>',methods=['POST','GET'])
def charityhome(chaname):
    return render_template('charityhome.html',chaname=chaname)

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
            return render_template('charityhome.html',chaname=data[0][1])
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
                blockchain.add_block_user(Charity_name,Charity_email)
                present=blockchain.userchain[len(blockchain.userchain)-1]
                previous_hash="0"
                present_hash=present.hash
                sql="select * from charityinformation"
                data1=pd.read_sql_query(sql,db)
                row,col=data1.shape
                if(row!=0):
                    data1=data1.iloc[row-1]
                    #print(data1)
                    previous_hash=data1.present_hash
                    #print(previous_hash)
                    present_hash=present.hash
                sql="insert into charityinformation(Charityname,Charityemail,Charitypassword,Charityaddress,Charitycontact,status,previous_hash,present_hash)values(%s,%s,%s,%s,%s,%s,%s,%s)"
                val=(Charity_name,Charity_email,charity_password,charity_address,charity_contact,status,previous_hash,present_hash)
                cur.execute(sql,val)
                db.commit()

                sql="""CREATE TABLE `%s_transactiondetails` (
                    `Id` int NOT NULL AUTO_INCREMENT,
                    `Charityname` varchar(200) DEFAULT NULL,
                    `Charityemail` varchar(200) DEFAULT NULL,
                    `CharityaccountNumber` varchar(200) DEFAULT NULL,
                    `charityifsccode` varchar(200) DEFAULT NULL,
                    `Userename` varchar(200) DEFAULT NULL,
                    `usercardnumber` varchar(200) DEFAULT NULL,
                    `expiredate` varchar(200) DEFAULT NULL,
                    `cvv` varchar(200) DEFAULT NULL,
                    `amount` varchar(200) DEFAULT NULL,
                    `status` varchar(200) DEFAULT NULL,
                    `previous_hash` varchar(200) DEFAULT NULL,
                    `present_hash` varchar(200) DEFAULT NULL,
                    `hash` varchar(200) DEFAULT NULL,
                    PRIMARY KEY (`Id`)
                    ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci"""%(Charity_name)
                cur.execute(sql)
                db.commit()

                sql1="""CREATE TABLE `%s_donation` (
                `Slno` int(200) NOT NULL AUTO_INCREMENT,
                `Charityname` varchar(200) DEFAULT NULL,
                `Charityemail` varchar(200) DEFAULT NULL,
                `Charityaddress` varchar(200) DEFAULT NULL,
                `Username` varchar(200) DEFAULT NULL,
                `Useremail` varchar(200) DEFAULT NULL,
                `status` varchar(200) DEFAULT NULL,
                `previous_hash` varchar(200) DEFAULT NULL,
                `present_hash` varchar(200) DEFAULT NULL,
                `hash` varchar(200) DEFAULT NULL,
                PRIMARY KEY (`Slno`)
                ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;"""%(Charity_name)
                cur.execute(sql1)
                db.commit()


                sql2="""CREATE TABLE `%s_members` (
                `Slno` int(200) NOT NULL AUTO_INCREMENT,
                `Charityname` varchar(200) DEFAULT NULL,
                `Membername` varchar(200) DEFAULT NULL,
                `Memberemail` varchar(200) DEFAULT NULL,
                `Memberaddress` varchar(200) DEFAULT NULL,
                `Membercontact` varchar(200) DEFAULT NULL,
                `status` varchar(200) DEFAULT NULL,
                `previous_hash` varchar(200) DEFAULT NULL,
                `present_hash` varchar(200) DEFAULT NULL,
                PRIMARY KEY (`Slno`)
                ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;"""%(Charity_name)
                cur.execute(sql2)
                db.commit()

                sql3="""CREATE TABLE `%s_withdraw` (
                `Slno` int(200) NOT NULL AUTO_INCREMENT,
                `Charityname` varchar(200) DEFAULT NULL,
                `event` varchar(200) DEFAULT NULL,
                `eventdescription` varchar(200) DEFAULT NULL,
                `amount` varchar(200) DEFAULT NULL,
                `previous_hash` varchar(200) DEFAULT NULL,
                `present_hash` varchar(200) DEFAULT NULL,
                PRIMARY KEY (`Slno`)
                ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;"""%(Charity_name)
                cur.execute(sql3)
                db.commit()


                sql4="""CREATE TABLE `%s_itemrequest` (
                `Slno` int(200) NOT NULL AUTO_INCREMENT,
                `Charityname` varchar(200) DEFAULT NULL,
                `Username` varchar(200) DEFAULT NULL,
                `Useremail` varchar(200) DEFAULT NULL,
                `Useraddress` varchar(200) DEFAULT NULL,
                `Usercontact` varchar(200) DEFAULT NULL,
                `items` varchar(200) DEFAULT NULL,
                `status` varchar(200) DEFAULT NULL,
                `previous_hash` varchar(200) DEFAULT NULL,
                `present_hash` varchar(200) DEFAULT NULL,
                PRIMARY KEY (`Slno`)
                ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;"""%(Charity_name)
                cur.execute(sql4)
                db.commit()


                sql5="""CREATE TABLE `%s_item` (
                `Slno` int(200) NOT NULL AUTO_INCREMENT,
                `Charityname` varchar(200) DEFAULT NULL,
                `Username` varchar(200) DEFAULT NULL,
                `Useremail` varchar(200) DEFAULT NULL,
                `Useraddress` varchar(200) DEFAULT NULL,
                `Usercontact` varchar(200) DEFAULT NULL,
                `Membername` varchar(200) DEFAULT NULL,
                `items` varchar(200) DEFAULT NULL,
                `status` varchar(200) DEFAULT NULL,
                `present_hash` varchar(200) DEFAULT NULL,
                PRIMARY KEY (`Slno`)
                ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;"""%(Charity_name)
                cur.execute(sql5)
                db.commit()

                return render_template('charitylog.html')
            else:
                flash("Charity Details already exists","success")
                return redirect('charityregistration')
    return render_template('charityregistration.html')


@app.route('/charity_profile/<string:chaname>',methods=['POST','GET'])
def charity_profile(chaname):
    sql="select *from charityinformation where Charityname='%s'"%(chaname)
    data=pd.read_sql_query(sql,db)
    return render_template('charity_profile.html',cols=data.columns.values,rows=data.values.tolist(),chaname=chaname)


@app.route('/charity_post_upload/<string:chaname>',methods=['POST','GET'])
def charity_post_upload(chaname):
    return render_template('charity_post_upload.html',chaname=chaname)

@app.route('/post_upload/<string:chaname>',methods=['POST','GET'])
def post_upload(chaname):
    if request.method == 'POST':
        charity_name = request.form.get('charity_name')
        event_name = request.form.get('event_name')
        event_description = request.form.get('event_description')
        event_img = request.files.get('event_img')

        print(event_img)
        if event_img and allowed_file(event_img.filename):
            upload_folder = os.path.join('static', 'uploads')
            if not os.path.exists(upload_folder):
               os.makedirs(upload_folder)
            filename = event_img.filename
            filepath = os.path.join(upload_folder, filename)
            event_img.save(filepath)
           
            sql="INSERT INTO eventdetails (Charityname, event_name, event_description, event_img) VALUES (%s, %s, %s, %s)"
            cur.execute(sql, (charity_name, event_name, event_description, filename))
            #mysql.connection.commit()
            #cur.close()
            db.commit()

            
            return redirect(url_for('charity_event',chaname=charity_name))
        else:
            flash('Invalid file type. Please upload an image (png, jpg, jpeg, gif).', 'danger')

    return render_template('charity_post_upload.html', chaname=chaname)

@app.route('/charity_event/<string:chaname>',methods=['POST','GET'])
def charity_event(chaname):
    sql="select *from eventdetails where Charityname='%s'"%(chaname)
    data=pd.read_sql_query(sql,db)
    rows=data.values.tolist()
    if len(rows) > 0:
            if len(rows[0]) > 4: 
                print(rows[0][4])  
            else:
                print("Not enough columns in the data")
    else:
        print("No data found")
    return render_template('charity_event.html',cols=data.columns.values,rows=rows,chaname=chaname)

@app.route('/charity_member/<string:chaname>',methods=['POST','GET'])
def charity_member(chaname):
    table_name1=str(chaname)+"_members"
    sql=f"select * from {table_name1}"
    data=pd.read_sql_query(sql,db)
    return render_template('charity_member.html',cols=data.columns.values,rows=data.values.tolist(),chaname=chaname)

@app.route('/memberadd/<string:chaname>',methods=['POST','GET'])
def memberadd(chaname):
    if request.method == 'POST':
        charity_name = request.form.get('charity_name')
        Membername=request.form.get('member_name')
        Memberemail=request.form.get('member_email')
        Memberaddress=request.form.get('member_address')
        Membercontact=request.form.get('member_contact')

        blockchain.add_block_user(Membername,chaname)
        present=blockchain.userchain[len(blockchain.userchain)-1]
        previous_hash="0"
        present_hash=present.hash
        table_name1=chaname+"_members"
        sql=f"select * from {table_name1}"
        data1=pd.read_sql_query(sql,db)
        row,col=data1.shape
        if(row!=0):
            data1=data1.iloc[row-1]
            previous_hash=data1.present_hash
            present_hash=present.hash
                
        sql=f"INSERT INTO {table_name1} (Charityname,Membername, Memberemail, Memberaddress, Membercontact,previous_hash,present_hash) VALUES (%s,%s, %s, %s, %s,%s,%s)"
        cur.execute(sql, (charity_name,Membername, Memberemail, Memberaddress, Membercontact,previous_hash,present_hash))
        db.commit()
        return redirect(url_for('charity_member',chaname=chaname))
    return render_template('charity_memberadd.html',chaname=chaname)

@app.route('/charity_memberadd/<string:chaname>',methods=['POST','GET'])
def charity_memberadd(chaname):
    return render_template('charity_memberadd.html',chaname=chaname)

@app.route('/charity_withdraw/<string:chaname>',methods=['POST','GET'])
def charity_withdraw(chaname):
    return render_template('charity_withdraw.html',chaname=chaname)

@app.route('/withdraw_list/<string:chaname>',methods=['POST','GET'])
def withdraw_list(chaname):
    table_name1=chaname+"_withdraw"
    print(table_name1)
    sql=f"select * from {table_name1}"
    data=pd.read_sql_query(sql,db)
    return render_template('withdraw_list.html',cols=data.columns.values,rows=data.values.tolist(),chaname=chaname)

@app.route('/withdraw/<string:chaname>',methods=['POST','GET'])
def withdraw(chaname):
    if request.method == 'POST':
        charity_name = request.form.get('charity_name')
        event_name = request.form.get('event_name')
        event_description = request.form.get('event_description')
        ammount = int(request.form.get('ammount'))
        if(ammount>0):
            table_name1=chaname+"_transactiondetails"
            sql=f"SELECT SUM(amount)FROM {table_name1} WHERE status='completed'"
            data=pd.read_sql_query(sql,db)
            rows=data.values.tolist()
            amount1=rows[0][0]
            if(amount1!=None):
                amount1=int(rows[0][0])
            else:
                amount1=0
            print(amount1)
            table_name2=chaname+"_withdraw"
            sql=f"SELECT SUM(amount)FROM {table_name2} "
            data=pd.read_sql_query(sql,db)
            rows=data.values.tolist()
            amount2=rows[0][0]
            if(amount2!=None):
                amount2=int(rows[0][0])
            else:
                amount2=0
            total_amount=abs(amount1-amount2)
            if(ammount<=total_amount):
                blockchain.add_block_user(ammount,chaname)
                present=blockchain.userchain[len(blockchain.userchain)-1]
                previous_hash="0"
                present_hash=present.hash
                sql=f"select * from {table_name2}"
                data1=pd.read_sql_query(sql,db)
                row,col=data1.shape
                if(row!=0):
                    data1=data1.iloc[row-1]
                    previous_hash=data1.present_hash
                    present_hash=present.hash
                
                sql=f"INSERT INTO {table_name2} (Charityname, event, eventdescription, amount,previous_hash,present_hash) VALUES (%s, %s, %s, %s,%s,%s)"
                cur.execute(sql, (charity_name, event_name, event_description, ammount,previous_hash,present_hash))
                db.commit()


                '''sql="INSERT INTO withdraw(Charityname, event, eventdescription, amount,previous_hash,present_hash) VALUES (%s, %s, %s, %s,%s,%s)"
                cur.execute(sql, (charity_name, event_name, event_description, ammount,previous_hash,present_hash))
                db.commit()
                '''
                flash('withdraw.', 'success')
                return redirect(url_for('charity_withdraw',chaname=charity_name))
            else:
                flash('Insufficient ammount.', 'danger')
        else:
            flash('Invalid ammount.', 'danger')

    return render_template('charity_withdraw.html', chaname=chaname)


@app.route('/viewdonations/<chaname>',methods=['POST','GET'])
def viewdonations(chaname):
    sql="select Id,Charityemail,Charityaccountnumber,Userename,amount,status,previous_hash,present_hash from transactiondetails"
    data=pd.read_sql_query(sql,db)
    return render_template("viewdonations.html",cols=data.columns.values,rows=data.values.tolist(),chaname=chaname)

@app.route('/itemrequest/<chaname>',methods=['POST','GET'])
def itemrequest(chaname):
    table_name=chaname+"_itemrequest"
    sql=F"select *from {table_name}"
    data=pd.read_sql_query(sql,db)
    return render_template("itemrequest.html",cols=data.columns.values,rows=data.values.tolist(),chaname=chaname)

@app.route('/itemassign/<string:chaname>/<int:v>',methods=['POST','GET'])
def itemassign(chaname,v):
    table_name=chaname+"_itemrequest"
    sql=f"select Username,Useraddress,items,Usercontact,Useremail from {table_name} where Slno='%s'"%(v)
    data=pd.read_sql_query(sql,db)
    rows=data.values.tolist()
    usaname=rows[0][0]
    usaaddress=rows[0][1]
    items=rows[0][2]
    usacontact=rows[0][3]
    usaemail=rows[0][4]

    table_name1=chaname+"_members"
    sql=f"select * from {table_name1} where Memberaddress='%s'"%(usaaddress)
    data=pd.read_sql_query(sql,db)
    rows=data.values.tolist()
    if(len(rows)!=0):
        Membername=rows[0][2]
        Memberemail=rows[0][3]
        Memberaddress=rows[0][4]
        Membercontact=rows[0][5]
        status="pending"


        blockchain.add_block_user(chaname,usaname)
        present=blockchain.userchain[len(blockchain.userchain)-1]

        print(usaname)
        table_name2=usaname+"_item"
        sql=f"insert into {table_name2} (Charityname,Charityemail,Membername,Memberemail,Memberaddress,Membercontact,items,status,present_hash)values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        val=(chaname,session['charityemail'],Membername,Memberemail,Memberaddress,Membercontact,items,status,present.hash)
        cur.execute(sql,val)
        db.commit()

        table_name3=chaname+"_item"
        sql=f"insert into {table_name3} (Charityname,Username,Useremail,Useraddress,usercontact,Membername,items,status,present_hash)values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        val= (chaname,usaname,usaemail,usaaddress,usacontact,Membername,items,status,present.hash)
        cur.execute(sql,val)
        db.commit()


        #table_name1=chaname+"_members"
        sql=f"update {table_name} set Status='accept' where Slno='%s' and status='pending'"%(v)
        cur.execute(sql)
        db.commit()

        flash('successfully assign.', 'success')
        return redirect(url_for('itemrequest',chaname=chaname))
    
    flash('Insufficient member.', 'danger')
    return redirect(url_for('itemrequest',chaname=chaname))


@app.route("/charity_item/<string:chaname>")
def charity_item(chaname):

    table_name2=chaname+"_item"
    #sql="select Charityname,Charityemail,Charityaddress,Useremail from donation where Status='accept'"
    sql=f"select Slno,Charityname,Username,Useremail,Useraddress,usercontact,Membername,items,status from {table_name2}"
    data=pd.read_sql_query(sql,db)
    return render_template("charity_item.html",cols=data.columns.values,rows=data.values.tolist(),chaname=chaname)


@app.route("/itemstatus/<string:chaname>/<int:v>")
def itemstatus(chaname,v):

    table_name2=chaname+"_item"
    #sql="select Charityname,Charityemail,Charityaddress,Useremail from donation where Status='accept'"
    sql=f"select Username,items,present_hash status from {table_name2} where Slno='%s'"%(v)
    data=pd.read_sql_query(sql,db)
    rows=data.values.tolist()
    usaname=rows[0][0]
    item1=rows[0][1]
    hash1=rows[0][2]

    table_name3=usaname+"_item"
    sql=f"select Slno,items,present_hash status from {table_name3} where present_hash='%s'"%(hash1)
    data=pd.read_sql_query(sql,db)
    rows=data.values.tolist()
    c=rows[0][0]#use_item id 
    item2=rows[0][1]
    hash2=rows[0][2]
    if item1==item2 and hash1==hash2:
        sql=f"update {table_name2} set Status='accept' where Slno='%s' and status='pending'"%(v)
        cur.execute(sql)
        db.commit()


        sql=f"update {table_name3} set Status='accept' where Slno='%s' and status='pending'"%(c)
        cur.execute(sql)
        db.commit()

        flash("items recevied","success")
        return redirect(url_for('charity_item',chaname=chaname))
    flash("items not present","wrong")
    return redirect(url_for('charity_item',chaname=chaname))



@app.route('/singledonations/<chaname>',methods=['POST','GET'])
def singledonations(chaname):
    table_name1=chaname+"_transactiondetails"
    print(table_name1)
    sql=f"select Id,Charityemail,Charityaccountnumber,Userename,amount,status,previous_hash,present_hash from {table_name1}"
    data=pd.read_sql_query(sql,db)
    return render_template("singledonations.html",cols=data.columns.values,rows=data.values.tolist(),chaname=chaname)

@app.route('/charity_total/<chaname>',methods=['POST','GET'])
def charity_total(chaname):
    table_name1=chaname+"_transactiondetails"
    print(table_name1)
    sql=f"SELECT SUM(amount)FROM {table_name1} WHERE status='completed'"
    data=pd.read_sql_query(sql,db)
    rows=data.values.tolist()
    amount1=rows[0][0]
    if(amount1!=None):
        amount1=int(rows[0][0])
    else:
        amount1=0
    table_name2=chaname+"_withdraw"
    sql=f"SELECT SUM(amount)FROM {table_name2} "
    data=pd.read_sql_query(sql,db)
    rows=data.values.tolist()
    print(type(rows[0][0]))
    amount2=rows[0][0]
    print(amount2)
    if(amount2!=None):
        amount2=int(rows[0][0])
    else:
        amount2=0
    total_ammount=abs(amount1-amount2)

    blockchain.add_block_user(total_ammount,chaname)
    present=blockchain.userchain[len(blockchain.userchain)-1]
    sql=f"select * from {table_name1}"
    data1=pd.read_sql_query(sql,db)
    row,col=data1.shape
    if(row!=0):
        data1=data1.iloc[row-1]
        #print(data1)
        previous_hash=data1.present_hash
        #print(previous_hash)
        present_hash=present.hash
    else:
        previous_hash="0"
        present_hash="0"
    
    return render_template("charity_total.html",cols=data.columns.values,rows=data.values.tolist(),chaname=chaname,amount=total_ammount,previous_hash=previous_hash,present_hash=present_hash)



@app.route('/donationrequest/<chaname>',methods=['POST','GET'])
def donationrequest(chaname):
    table_name=chaname+"_donation"
    sql=f"""select *from {table_name}""" #where Charityname='%s'"%(chaname)
    data=pd.read_sql_query(sql,db)
    return render_template("donationrequest.html",cols=data.columns.values,rows=data.values.tolist(),chaname=chaname)


@app.route('/acceptrequest/<int:c>/<string:chaname>')
def acceptrequest(c,chaname):
    return render_template('charitydetails.html',c=c,chaname=chaname)

@app.route('/charitybanking/<int:c>/<string:chaname>',methods=["POST","GET"])
def charitybanking(c,chaname):
    if request.method=="POST":
        bankaccount=request.form['accountnumber']
        ifsccode=request.form['accountIFSCcode']
        status="accept"
        table_name1=chaname+"_donation"
        sql=f"""select Username,Useremail from {table_name1} where Slno='%s'"""%(c)
        data=pd.read_sql_query(sql,db)
        rows=data.values.tolist()
        print(rows)
        username=rows[0][0]
        useremail=rows[0][1]
        table_name2=username+"_bankdetails"
        blockchain.add_block_user(bankaccount,ifsccode)
        present=blockchain.userchain[len(blockchain.userchain)-1]
        previous_hash="0"
        sql=f"select * from {table_name2}"
        present_hash=present.hash
        data1=pd.read_sql_query(sql,db)
        row,col=data1.shape
        if(row!=0):
            data1=data1.iloc[row-1]
            #print(data1)
            previous_hash=data1.present_hash
            #print(previous_hash)
            present_hash=present.hash
        sql=f"insert into {table_name2} (Charityemail,Charityaccountnumber,charityifsccode,username,useremail,status,previous_hash,present_hash)values(%s,%s,%s,%s,%s,%s,%s,%s)"
        val=(session['charityemail'],bankaccount,ifsccode,username,useremail,status,previous_hash,present_hash)
        cur.execute(sql,val)
        db.commit()

        #for admin
        '''sql="insert into bankdetails(Charityemail,Charityaccountnumber,charityifsccode,useremail,status,previous_hash,present_hash)values(%s,%s,%s,%s,%s,%s,%s)"
        val=(session['charityemail'],bankaccount,ifsccode,useremail,status,previous_hash,present_hash)
        cur.execute(sql,val)
        db.commit()'''

        sql=f"update {table_name1} set Status='accept' where Slno='%s' and status='pending'"%(c)
        cur.execute(sql)
        db.commit()

        #for admin
        sql="update donation set Status='accept' where Slno='%s' and status='pending'"%(c)
        cur.execute(sql)
        db.commit()

        flash("Account Details sent to the user","success")

    return render_template("senddetails.html",chaname=chaname)

@app.route("/charitylogout")
def charitylogout():
    return redirect("/")

#admin function

@app.route('/admin',methods=["POST","GET"])
def admin():
    if request.method=="POST":
        cloud_mailid=request.form['admin_mailid']
        cloud_password=request.form['admin_password']
        if cloud_mailid=="admin@gmail.com" and cloud_password =="admin":
            return render_template("adminhome.html",x="admin")
    return render_template('admin.html')
@app.route('/adminhome',methods=['POST','GET'])
def adminhome():
    return render_template('adminhome.html')

@app.route("/viewallcharities")
def viewallcharities():
    sql="select *from charityinformation"
    data=pd.read_sql_query(sql,db)
    return render_template("allcharities.html",cols=data.columns.values,rows=data.values.tolist())


@app.route("/viewallusers")
def viewallusers():
    sql = "select Id,Username,useremail,age,contact,address from userinformation"
    data = pd.read_sql_query(sql, db)
    return render_template('allusers.html',cols=data.columns.values,rows=data.values.tolist())

@app.route("/alldonations")
def alldonations():
    sql="select Slno,Charityname,Charityemail,Username from donation"
    data=pd.read_sql_query(sql,db)
    return render_template("alldonations.html",cols=data.columns.values,rows=data.values.tolist())

@app.route("/bankinfo/<int:c>")
def bankinfo(c=0):
    '''blockchain.add_block_user("admin","hacked")
    present=blockchain.userchain[len(blockchain.userchain)-1]
    sql="update donation set Status='hacked',present_hash='%s' where Slno='%s'"%(present.hash,c)
    cur.execute(sql)
    db.commit()'''
    return render_template('admin_charitydetails.html',c=c)


@app.route('/admin_charitybanking/<int:c>',methods=["POST","GET"])
def admin_charitybanking(c):
    if request.method=="POST":
        bankaccount=request.form['accountnumber']
        ifsccode=request.form['accountIFSCcode']

        blockchain.add_block_user("admin","hacked")
        present=blockchain.userchain[len(blockchain.userchain)-1]
        sql="update donation set Status='hacked',present_hash='%s' where Slno='%s' and status='pending'"%(present.hash,c)
        cur.execute(sql)
        db.commit()
        
        sql="select Charityname,hash,Username,Charityemail,Useremail from donation where Slno='%s'"%(c)
        data=pd.read_sql_query(sql,db)
        rows=data.values.tolist()
        chaname=rows[0][0]
        hash1=rows[0][1]
        usaname=rows[0][2]
        chanemail=rows[0][3]
        useremail=rows[0][4]
        status="hacked"

        table_name=chaname+"_donation"

        blockchain.add_block_user("admin","hacked")
        present=blockchain.userchain[len(blockchain.userchain)-1]
        sql=f"update {table_name} set Status='hacked',present_hash='%s' where hash='%s'"%(present.hash,hash1)
        cur.execute(sql)
        db.commit()

        ''' sql="select Charityemail,Useremail from donation where Slno='%s'"%(c)
        data=pd.read_sql_query(sql,db)
        print(data)
        rows=data.values.tolist()
        print(rows)
        chanemail=rows[0][0]
        useremail=rows[0][1]'''

        table_name1=usaname+"_bankdetails"
        blockchain.add_block_user(bankaccount,ifsccode)
        present=blockchain.userchain[len(blockchain.userchain)-1]
        sql=f"insert into {table_name1} (Charityemail,Charityaccountnumber,charityifsccode,username,useremail,status,previous_hash,present_hash)values(%s,%s,%s,%s,%s,%s,%s,%s)"
        val=(chanemail,bankaccount,ifsccode,usaname,useremail,status,present.previous_hash,present.hash)
        cur.execute(sql,val)
        db.commit()


        '''status="hacked"
        sql="insert into transactiondetails (Charityemail,Charityaccountnumber,charityifsccode,status)values(%s,%s,%s,%s)"
        val=(session['charityemail'],bankaccount,ifsccode,status)
        cur.execute(sql,val)
        db.commit()'''
        flash("Account Details sent to the user","success")
    
    return render_template("detailssend.html")

@app.route("/admin_bankdetails")
def admin_bankdetails():
    sql="select Id,Charityemail,Charityaccountnumber,charityifsccode from bankdetails"
    data=pd.read_sql_query(sql,db)
    return render_template("admin_bankdetails.html",cols=data.columns.values,rows=data.values.tolist())

@app.route("/admin_transactiodetails")
def admin_transactiodetails():
    sql="select Id,Charityemail,Charityaccountnumber,Userename,amount,status,previous_hash,present_hash from transactiondetails where status='completed'"
    data=pd.read_sql_query(sql,db)
    return render_template("admin_transactiodetails.html",cols=data.columns.values,rows=data.values.tolist())

@app.route('/adminlogout')
def adminlogout():
    return redirect('/')



#user function
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
                #blockchain is applied
                blockchain.add_block_user(user_name,user_email)
                present=blockchain.userchain[len(blockchain.userchain)-1]
                previous_hash="0"
                present_hash=present.hash
                sql="select * from userinformation"
                data1=pd.read_sql_query(sql,db)
                row,col=data1.shape
                if(row!=0):
                    data1=data1.iloc[row-1]
                    #print(data1)
                    previous_hash=data1.present_hash
                    #print(previous_hash)
                    present_hash=present.hash
                sql="insert into userinformation (Username,useremail,password,age,contact,address,Status,previous_hash,present_hash)values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                val=(user_name,user_email,password,age,contact,address,status,previous_hash,present_hash)
                cur.execute(sql,val)
                db.commit()

                sql1="""CREATE TABLE `%s_bankdetails` (
                `Id` int NOT NULL AUTO_INCREMENT,
                `Charityemail` varchar(200) DEFAULT NULL,
                `CharityaccountNumber` varchar(200) DEFAULT NULL,
                `charityifsccode` varchar(200) DEFAULT NULL,
                `username` varchar(200) DEFAULT NULL,
                `useremail` varchar(200) DEFAULT NULL,
                `status` varchar(200) DEFAULT NULL,
                `previous_hash` varchar(200) DEFAULT NULL,
                `present_hash` varchar(200) DEFAULT NULL,
                PRIMARY KEY (`Id`)
                ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci"""%(user_name)
                cur.execute(sql1)
                db.commit()

                sql2="""CREATE TABLE `%s_transactiondetails` (
                    `Id` int NOT NULL AUTO_INCREMENT,
                    `Charityname` varchar(200) DEFAULT NULL,
                    `Charityemail` varchar(200) DEFAULT NULL,
                    `CharityaccountNumber` varchar(200) DEFAULT NULL,
                    `charityifsccode` varchar(200) DEFAULT NULL,
                    `Userename` varchar(200) DEFAULT NULL,
                    `usercardnumber` varchar(200) DEFAULT NULL,
                    `amount` varchar(200) DEFAULT NULL,
                    `status` varchar(200) DEFAULT NULL,
                    `previous_hash` varchar(200) DEFAULT NULL,
                    `present_hash` varchar(200) DEFAULT NULL,
                    PRIMARY KEY (`Id`)
                    ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci"""%(user_name)
                cur.execute(sql2)
                db.commit()


                sql3="""CREATE TABLE `%s_item` (
                `Slno` int(200) NOT NULL AUTO_INCREMENT,
                `Charityname` varchar(200) DEFAULT NULL,
                `Charityemail` varchar(200) DEFAULT NULL,
                `Membername` varchar(200) DEFAULT NULL,
                `Memberemail` varchar(200) DEFAULT NULL,
                `Memberaddress` varchar(200) DEFAULT NULL,
                `Membercontact` varchar(200) DEFAULT NULL,
                `items` varchar(200) DEFAULT NULL,
                `status` varchar(200) DEFAULT NULL,
                `present_hash` varchar(200) DEFAULT NULL,
                PRIMARY KEY (`Slno`)
                ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;"""%(user_name)
                cur.execute(sql3)
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
            return render_template('userhome.html',usaname=data[0][1])
        else:
            flash("Credentials are not valid.....!","success")
            return redirect('userlog')
    return render_template('userlog.html')

@app.route('/userhome/<usaname>',methods=['POST','GET'])
def userhome(usaname):
    return render_template('userhome.html',usaname=usaname)


@app.route('/userprofile/<usaname>',methods=['POST','GET'])
def userprofile(usaname):
    sql="select * from userinformation where Username='%s'"%(usaname)
    data=pd.read_sql_query(sql,db)
    rows=data.values.tolist()
    return render_template('user_profile.html',cols=data.columns.values,rows=data.values.tolist(),usaname=usaname)

@app.route('/userhome1',methods=['POST','GET'])
def userhome1():
    return render_template('userhome1.html')

@app.route('/viewcharities/<string:usaname>',methods=['POST','GET'])
def viewcharities(usaname):
    sql="select *from charityinformation"
    data=pd.read_sql_query(sql,db)
    return render_template('viewcharities.html',cols=data.columns.values,rows=data.values.tolist(),usaname=usaname)

@app.route('/about/<string:usaname>/<int:v>',methods=['POST','GET'])
def about(usaname,v):
    sql="select * from charityinformation where Slno='%s'"%(v)
    data=pd.read_sql_query(sql,db)
    rows=data.values.tolist()

    charity_name=rows[0][1]
    sql="select *from eventdetails where Charityname='%s'"%(charity_name)
    data=pd.read_sql_query(sql,db)
    rows=data.values.tolist()
    if len(rows) > 0:
            if len(rows[0]) > 4: 
                print(rows[0][4])  
            else:
                print("Not enough columns in the data")
    else:
        print("No data found")
    return render_template('about.html',cols=data.columns.values,rows=data.values.tolist(),usaname=usaname,v=v)

@app.route('/singleevent/<string:usaname>/<int:v>/<int:c>',methods=['POST','GET'])
def singleevent(usaname,v,c):
    '''sql="select * from charityinformation where Slno='%s'"%(v)
    data=pd.read_sql_query(sql,db)
    rows=data.values.tolist()

    charity_name=rows[0][1]'''
    sql="select *from eventdetails where Slno='%s'"%(c)
    data=pd.read_sql_query(sql,db)
    rows=data.values.tolist()
    if len(rows) > 0:
            if len(rows[0]) > 4: 
                print(rows[0][4])  
            else:
                print("Not enough columns in the data")
    else:
        print("No data found")
    return render_template('single_event.html',cols=data.columns.values,rows=data.values.tolist(),usaname=usaname,v=v,c=c)

@app.route('/donateitems/<string:usaname>/<int:v>/<int:c>',methods=['POST','GET'])
def donateitems(usaname,v,c):
    print(v)
    if request.method=="POST":
    #print(session['user_email'])
        sql="select * from charityinformation where Slno='%s'"%(v)
        data=pd.read_sql_query(sql,db)
        rows=data.values.tolist()

        charity_name=rows[0][1]

        sql="select * from userinformation where Username='%s'"%(usaname)
        data=pd.read_sql_query(sql,db)
        rows=data.values.tolist()
        Username=rows[0][1]
        Useremail=rows[0][2]
        Useraddress=rows[0][6]
        Usercontact=rows[0][5]
        status='pending'
    
        items=request.form.get('items')
        blockchain.add_block_user(charity_name,Username)
        present=blockchain.userchain[len(blockchain.userchain)-1]
        previous_hash="0"
        present_hash=present.hash
        #table_name=charity_name+"_itemrequest"
        sql="select * from %s_itemrequest"%(charity_name)
        data1=pd.read_sql_query(sql,db)
        row,col=data1.shape
        print(present_hash)
        if(row!=0):
            data1=data1.iloc[row-1]
            #print(data1)
            previous_hash=data1.present_hash
            #print(previous_hash)
            present_hash=present.hash
        table_name=charity_name+"_itemrequest"
        print(table_name)
        sql=f"""insert into {table_name} (Charityname,Username,Useremail,Useraddress,Usercontact,items,status,previous_hash,present_hash)values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        val=(charity_name,Username,Useremail,Useraddress,Usercontact,items,status,previous_hash,present_hash)
        print(sql)
        cur.execute(sql,val)
        db.commit()


        flash("Your request sent successfuly","success")
        return redirect(url_for('about',usaname=usaname,v=v))
    return redirect(url_for('singleevent',usaname=usaname,v=v,c=c))


@app.route('/donate/<string:usaname>/<int:v>',methods=['POST','GET'])
def donate(usaname,v):
    print(v)
    #print(session['user_email'])
    sql="select * from charityinformation where Slno='%s'"%(v)
    data=pd.read_sql_query(sql,db)
    rows=data.values.tolist()

    charity_name=rows[0][1]
    charity_email=rows[0][2]
    charity_address=rows[0][4]

    '''sql="select Useremail from userinformation where Username='%s'"%(usaname)
    data=pd.read_sql_query(sql,db)
    rows=data.values.tolist()

    Useremail=rows[0][0]'''
    status='pending'
    #insert the into donation table.
    blockchain.add_block_user(charity_name,session['user_email'])
    present=blockchain.userchain[len(blockchain.userchain)-1]
    previous_hash="0"
    present_hash=present.hash
    hash=present.hash
    sql="select * from %s_donation"%(charity_name)
    data1=pd.read_sql_query(sql,db)
    row,col=data1.shape
    if(row!=0):
        data1=data1.iloc[row-1]
        #print(data1)
        previous_hash=data1.present_hash
        #print(previous_hash)
        present_hash=present.hash
    table_name=charity_name+"_donation"
    print(table_name)
    sql=f"""insert into {table_name} (Charityname,Charityemail,Charityaddress,Username,Useremail,status,previous_hash,present_hash,hash)values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    val=(charity_name,charity_email,charity_address,usaname,session['user_email'],status,previous_hash,present_hash,hash)
    print(sql)
    cur.execute(sql,val)
    db.commit()

    #for admin
    blockchain.add_block_user(charity_name,session['user_email'])
    present=blockchain.userchain[len(blockchain.userchain)-1]
    previous_hash="0"
    present_hash=present.hash
    sql="select * from donation"
    data1=pd.read_sql_query(sql,db)
    row,col=data1.shape
    if(row!=0):
        data1=data1.iloc[row-1]
        #print(data1)
        previous_hash=data1.present_hash
        #print(previous_hash)
        present_hash=present.hash
    sql="insert into donation(Charityname,Charityemail,Charityaddress,Username,Useremail,status,previous_hash,present_hash,hash)values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    val=(charity_name,charity_email,charity_address,usaname,session['user_email'],status,previous_hash,present_hash,hash)
    print(sql)
    cur.execute(sql,val)
    db.commit()


    sql = "select *from charityinformation"
    data = pd.read_sql_query(sql, db)
    flash("Your request sent successfuly","success")
    return redirect(url_for('about',usaname=usaname,v=v))
    

@app.route('/charityresponse/<string:usaname>',methods=['POST','GET'])
def charityresponse(usaname):
    '''sql="select useremail from userinformation where Username='%s'"%(usaname)
    data1=pd.read_sql_query(sql,db)
    print(data1)
    rows=data1.values.tolist()
    print(rows)
    useremail=rows[0][0]
    table_name=
    data=pd.read_sql_query("select *from bankdetails",db)
    return render_template('charityresponse.html',useremail=useremail,cols=data.columns.values,rows=data.values.tolist(),usaname=usaname)'''

    table_name=usaname+"_bankdetails"
    data=pd.read_sql_query(f"select *from {table_name}",db)
    return render_template('charityresponse.html',cols=data.columns.values,rows=data.values.tolist(),usaname=usaname)

@app.route('/ammount/<string:usaname>/<int:v>',methods=['POST','GET'])
def ammount(usaname,v):
    return render_template('ammount.html',usaname=usaname,v=v)

@app.route('/payment/<string:usaname>/<int:v>',methods=['POST','GET'])
def payment(usaname,v):
    if request.method=="POST":
        print("ekdfhk")
        if(request.form['amount']!=''):
            amount=int(request.form['amount'])
            return render_template('paymentpage.html',usaname=usaname,v=v,amount=amount)
    return render_template('ammount.html',usaname=usaname,v=v)

@app.route('/address/<string:usaname>/<int:v>',methods=['POST','GET'])
def address(usaname,v):
    #here we extract data based on email address in  and charity information
    '''table_name=usaname+"_bankdetails"
    sql=f"select Charityemail from {table_name} where Id='%s'"%(v)
    data1=pd.read_sql_query(sql,db)
    rows=data1.values.tolist()
    print(rows)
    Charityemail=rows[0][0]'''
    sql="select Slno,Charityname,Charityemail,Charityaddress,Charitycontact from charityinformation where Slno='%s'"%(v)
    data=pd.read_sql_query(sql,db)
    #print(type(v))
    info=data.iloc[0]
    print(info)
    return render_template('address.html',usaname=usaname,v=v,info=data.iloc[0])

@app.route('/scann/<string:usaname>/<int:v>',methods=['POST','GET'])
def scann(usaname,v):
    return render_template('scann.html',usaname=usaname,v=v)

'''@app.route('/paymentpage/<int:v>/<int:ammount>',methods=['POST','GET'])
def paymentpage(v):
    return render_template('paymentpage.html',v=v,ammount=ammount)'''

@app.route("/makedonate/<string:usaname>/<int:v>/<int:amount>",methods=["POST","GET"])
def makedonate(usaname,v,amount):
    if request.method=="POST":
        #amount=request.form['amount']
        Username=request.form['Username']
        usercardnumber=request.form['usercardnumber']
        expiredate=request.form['expiredate']
        cvv=request.form['cvv']

        table_name=usaname+"_bankdetails"
        sql=f"select Charityemail,CharityaccountNumber,charityifsccode from {table_name} where Id='%s'"%(v)
        data=pd.read_sql_query(sql,db)
        print(data)
        rows=data.values.tolist()
        print(rows)
        Charityemail=rows[0][0]
        CharityaccountNumber=rows[0][1]
        charityifsccode=rows[0][2]

        sql="select Charityname from charityinformation where Charityemail='%s'"%(Charityemail)
        data=pd.read_sql_query(sql,db)
        rows=data.values.tolist()
        chaname=rows[0][0]


        table_name1=chaname+"_transactiondetails"
        transaction_blockchain.add_block_transaction(Charityemail,CharityaccountNumber,charityifsccode,Username,usercardnumber,expiredate,cvv,amount)
        present=transaction_blockchain.transactiochain[len(transaction_blockchain.transactiochain)-1]
        previous_hash="0"
        present_hash=present.hash
        hash=present.hash
        sql=f"select * from {table_name1}"
        data1=pd.read_sql_query(sql,db)
        row,col=data1.shape
        if(row!=0):
            data1=data1.iloc[row-1]
            #print(data1)
            previous_hash=data1.present_hash
            #print(previous_hash)
            present_hash=present.hash
        sql=f"insert into {table_name1}(Charityname,Charityemail,CharityaccountNumber,charityifsccode,Userename,usercardnumber,expiredate,cvv,amount,status,previous_hash,present_hash,hash)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "
        val=(chaname,Charityemail,CharityaccountNumber,charityifsccode,Username,usercardnumber,expiredate,cvv,amount,"completed",previous_hash,present_hash,hash)
        cur.execute(sql,val)
        db.commit()

        

        table_name2=usaname+"_transactiondetails"
        transaction_blockchain.add_block_transaction(Charityemail,CharityaccountNumber,charityifsccode,Username,usercardnumber,expiredate,cvv,amount)
        present=transaction_blockchain.transactiochain[len(transaction_blockchain.transactiochain)-1]
        previous_hash="0"
        present_hash=present.hash
        sql=f"select * from {table_name2}"
        data1=pd.read_sql_query(sql,db)
        row,col=data1.shape
        if(row!=0):
            data1=data1.iloc[row-1]
            #print(data1)
            previous_hash=data1.present_hash
            #print(previous_hash)
            present_hash=present.hash
        sql=f"insert into {table_name2}(Charityname,Charityemail,CharityaccountNumber,charityifsccode,Userename,amount,status,previous_hash,present_hash)values(%s,%s,%s,%s,%s,%s,%s,%s,%s) "
        val=(chaname,Charityemail,CharityaccountNumber,charityifsccode,Username,amount,"completed",previous_hash,present_hash)
        cur.execute(sql,val)
        db.commit()

         #for admin
        transaction_blockchain.add_block_transaction(Charityemail,CharityaccountNumber,charityifsccode,Username,usercardnumber,expiredate,cvv,amount)
        present=transaction_blockchain.transactiochain[len(transaction_blockchain.transactiochain)-1]
        previous_hash="0"
        present_hash=present.hash
        sql="select * from transactiondetails"
        data1=pd.read_sql_query(sql,db)
        row,col=data1.shape
        if(row!=0):
            data1=data1.iloc[row-1]
            #print(data1)
            previous_hash=data1.present_hash
            #print(previous_hash)
            present_hash=present.hash
        sql="insert into transactiondetails(Charityname,Charityemail,CharityaccountNumber,charityifsccode,Userename,usercardnumber,expiredate,cvv,amount,status,previous_hash,present_hash,hash)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "
        val=(chaname,Charityemail,CharityaccountNumber,charityifsccode,Username,usercardnumber,expiredate,cvv,amount,"completed",previous_hash,present_hash,hash)
        cur.execute(sql,val)
        db.commit()

        '''sql="update donation set Status='accept' where Slno='%s' and status='pending'"
        cur.execute(sql)
        db.commit()'''

    return render_template("success.html",usaname=usaname,v=v)

@app.route("/itemlist/<string:usaname>")
def item_list(usaname):
    table_name2=usaname+"_item"
    #sql="select Charityname,Charityemail,Charityaddress,Useremail from donation where Status='accept'"
    sql=f"select Charityname,Charityemail,Membername,Memberemail,Memberaddress,Membercontact,items,status from {table_name2}"
    data=pd.read_sql_query(sql,db)
    return render_template("itemlist.html",cols=data.columns.values,rows=data.values.tolist(),usaname=usaname)

@app.route("/item_complete/<string:usaname>")
def item_complete(usaname):
    table_name2=usaname+"_item"
    #sql="select Charityname,Charityemail,Charityaddress,Useremail from donation where Status='accept'"
    sql=f"select Charityname,Charityemail,Membername,Memberemail,Memberaddress,Membercontact,items,status from {table_name2} where status='accept'"
    data=pd.read_sql_query(sql,db)
    return render_template("donation_item_complete.html",cols=data.columns.values,rows=data.values.tolist(),usaname=usaname)

@app.route("/item_pending/<string:usaname>")
def item_pending(usaname):
    table_name2=usaname+"_item"
    #sql="select Charityname,Charityemail,Charityaddress,Useremail from donation where Status='accept'"
    sql=f"select Charityname,Charityemail,Membername,Memberemail,Memberaddress,Membercontact,items,status from {table_name2} where status='pending'"
    data=pd.read_sql_query(sql,db)
    return render_template("donation_item_pending.html",cols=data.columns.values,rows=data.values.tolist(),usaname=usaname)


@app.route("/user_transactiondetails/<string:usaname>")
def user_transactiondetails(usaname):
    table_name2=usaname+"_transactiondetails"
    #sql="select Charityname,Charityemail,Charityaddress,Useremail from donation where Status='accept'"
    sql=f"select Id,Charityemail,Charityaccountnumber,Userename,amount,status,previous_hash,present_hash from {table_name2}"
    data=pd.read_sql_query(sql,db)
    return render_template("user_transactiondetails.html",cols=data.columns.values,rows=data.values.tolist(),usaname=usaname)


@app.route("/userlogout")
def userlogout():
    return redirect("/")



if __name__=="__main__":
    app.run(debug=True,port=8000)