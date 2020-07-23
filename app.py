from chatbot import chatbot
from flask import Flask, render_template, request
#from flask_mysqldb import MySQL
import datetime
from datetime import datetime
#import pandas as pd
from time import time
import os
#from flask_sqlalchemy import SQLAlchemy
import psycopg2
from psycopg2 import Error
import urllib.parse as urlparse



app = Flask(__name__)
app.static_folder = 'static'

#connection =None 
#cur = None

os.environ['DATABASE_URL'] = 'postgres://qkuegbuqampmav:bbd55ba8f536da4bf35bd04aae686e29a5354c6f47ad628d9d2cbba4062fb505@ec2-50-19-26-235.compute-1.amazonaws.com:5432/d8l2o0qtiunehq'

url = urlparse.urlparse(os.environ['DATABASE_URL'])
dbname = url.path[1:]
user = url.username
password = url.password
host = url.hostname
port = url.port



connection = psycopg2.connect(user = user,password = password,host =host,port =port,database = dbname)
cur = connection.cursor()

def create_tables():
    sql = "CREATE TABLE non_veg\
        (\
            id integer NOT NULL,\
            price integer,\
            name text COLLATE pg_catalog.\"default\",\
            CONSTRAINT non_veg_pkey PRIMARY KEY (id)\
        )"
    cur.execute(sql)
    connection.commit()

    sql = "CREATE TABLE veg_list\
        (\
            id integer NOT NULL,\
            price integer,\
            name text COLLATE pg_catalog.\"default\",\
            CONSTRAINT veg_list_pkey PRIMARY KEY (id)\
        )"
    cur.execute(sql)
    connection.commit()

    sql = "CREATE TABLE user_details\
        (\
            id text COLLATE pg_catalog.\"default\" NOT NULL,\
            name text COLLATE pg_catalog.\"default\",\
            street text COLLATE pg_catalog.\"default\",\
            place text COLLATE pg_catalog.\"default\",\
            phone text COLLATE pg_catalog.\"default\",\
            category text COLLATE pg_catalog.\"default\",\
            food text COLLATE pg_catalog.\"default\",\
            \"time\" timestamp without time zone,\
            status text COLLATE pg_catalog.\"default\",\
            CONSTRAINT user_details_pkey PRIMARY KEY (id)\
        )"
    cur.execute(sql)
    connection.commit()


    sql ="""INSERT INTO non_veg(id,price,name) VALUES(%s,%s,%s)"""
    record_to_insert = (1,250,"Chicken Pizza",)
    cur.execute(sql,record_to_insert)
    connection.commit()

    sql ="""INSERT INTO non_veg(id,price,name) VALUES(%s,%s,%s)"""
    record_to_insert = (2,450,"BBQ Chicken Pizza",)
    cur.execute(sql,record_to_insert)
    connection.commit()

    sql ="""INSERT INTO non_veg(id,price,name) VALUES(%s,%s,%s)"""
    record_to_insert = (3,530,"Ham and Cheese Pizza",)
    cur.execute(sql,record_to_insert)
    connection.commit()

    sql ="""INSERT INTO veg_list(id,price,name) VALUES(%s,%s,%s)"""
    record_to_insert = (1,380,"Veggie Delight",)
    cur.execute(sql,record_to_insert)
    connection.commit()

    sql ="""INSERT INTO veg_list(id,price,name) VALUES(%s,%s,%s)"""
    record_to_insert = (2,450,"Margerita",)
    cur.execute(sql,record_to_insert)
    connection.commit()

    sql ="""INSERT INTO veg_list(id,price,name) VALUES(%s,%s,%s)"""
    record_to_insert = (3,490,"Spinach Delight",)
    cur.execute(sql,record_to_insert)
    connection.commit()




#except (Exception, psycopg2.Error) as error :
 #   print ("Error while connecting to PostgreSQL", error)
#finally:
    #closing database connection.
 #   if(connection):
  #      cursor.close()
   #     connection.close()
    #    print("PostgreSQL connection is closed")



#app.config['SQLAlCHEMY_DATABASE_URI'] = 'postgresql://root:123@localhost/postgres'
#db=SQLAlchemy(app)

#class Example(db.Model):
 #   __tablename__ = 'user_details'
  #  id = db.Column('id',db.Unicode,primary_key=True)



#mysql = MySQL(app)
#app.config['MYSQL_USER'] = 'root'
#app.config['MYSQL_PASSWORD'] = ''
#app.config['MYSQL_HOST'] = 'localhost'
#app.config['MYSQL_DB'] ='pizzabot'
#app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
#app.config['MYSQL_DATABASE_URI'] = os.environ['DATABASE_URL']


@app.route("/")
def home():
    return render_template("index.html")


user_input = []
flag= ''
user_id=''
name =''
street =''
place =''
current_time =''
status=''
phone =''
veg_list = ''
nv_list =''
myresult = ''



@app.route("/get")
def get_bot_response():
    global flag;
    global user_id;
    global name;
    global street;
    global place;
    global current_time;
    global status;
    global phone;
    global veg_list;
 
    global myresult;
    global connection;
    global cur;

    check_order_status()

    userText = request.args.get('msg').lower()
    user_input=userText.split()


    for i in range(0,len(user_input)):

        if user_input[i] =='order':
            return user_details()
           
        if user_input [i] == 'status':
            flag='status'
            return str("Enter order id:")

        if user_input[i] == 'veg':
            return veg_list_category()

        if user_input[i] == 'non' or user_input[i] == 'non-veg' or user_input[i] == 'nonveg':
           return non_veg_list_category()

    if flag == '':
        return "Im still learning to communicate"

    if flag =='details':
        return split_user_details(userText)
        
    if flag == 'veg':
        return veg_after_ordering(flag,user_input)


    if flag =='nonveg':
        return veg_after_ordering(flag,user_input)
        
    if flag == 'status':
        return order_status_by_user(user_input)


    return str(chatbot.get_response(userText))


#Checking the order status defaultly when the bot is executed
def check_order_status():
    #-----------
    #Description 
    #-----------
    #This is used to check the order status defaultly when bot is executed

    #------
    #Return
    #------
    #This returns the status of the food 
    global connection;
    global cur;

    sql = "select id,time from user_details where status != 'Pizza Delivered'"
    cur.execute(sql)
    myresult =cur.fetchall()
    connection.commit()
    if is_empty(myresult):
        return 0
    current_time = datetime.now()
    print("##############")
    print(len(myresult))
    print(myresult)
    for i in range(0,len(myresult)):
        print(myresult[i])
        print(type(myresult[i]))
        # print(myresult[i])
        print(type(myresult[i][0]))
        order_time = myresult[i][1]
        rem_time = current_time-order_time
        time_diff =rem_time.seconds/60
        print(time_diff)
        print(type(time_diff))
        if time_diff <= 15:
            try:
                sql = "UPDATE user_details SET status = 'Preparation started' WHERE id = %s"
                cur.execute(sql,(myresult[i][0],))
                connection.commit()
            except Exception as ex:
                print(ex)            
            
        if time_diff >15 and time_diff <= 30:
            try:
                sql = "UPDATE user_details SET status = 'Pizza Cooking' WHERE id = %s"
                cur.execute(sql,(myresult[i][0],))
                connection.commit()
            except Exception as ex:
                print(ex)
            # cur=mysql.connection.cursor()
            # sql = "UPDATE user_details SET status = 'Pizza Cooking' WHERE id = %s"
            # cur.execute(sql,myresult[i]['id'])
            # mysql.connection.commit()
        if time_diff > 30 and time_diff <= 45:
            try:
                sql = "UPDATE user_details SET status = 'Cooking Finished' WHERE id = %s"
                cur.execute(sql,(myresult[i][0],))
                connection.commit()
            except Exception as ex:
                print(ex) 
            # cur=mysql.connection.cursor()
            # sql = "UPDATE user_details SET status = 'Cooking Finished' WHERE id = %s"
            # cur.execute(sql,myresult[i]['id'])
            # mysql.connection.commit()
        if time_diff > 45 and time_diff <=60:
            try:
                sql = "UPDATE user_details SET status = 'Out for Delivery' WHERE id = %s"
                cur.execute(sql,(myresult[i][0],))
                connection.commit()
            except Exception as ex:
                print(ex)
            # cur=mysql.connection.cursor()
            # sql = "UPDATE user_details SET status = 'Out for Delivery' WHERE id = %s"
            # cur.execute(sql,myresult[i]['id'])
            # mysql.connection.commit()
        if time_diff >60:
            try:
                sql = "UPDATE user_details SET status = 'Pizza Delivered' WHERE id = %s"
                cur.execute(sql,(myresult[i][0],))
                connection.commit()
            except Exception as ex:
                print(ex)
            # cur=mysql.connection.cursor()
            # sql = "UPDATE user_details SET status = 'Pizza Delivered' WHERE id = %s"
            # cur.execute(sql,myresult[i]['id'])
            # mysql.connection.commit()
    return 0

def  user_details():
    #-----------
    #Description 
    #-----------
    #This is used to set flag to details when the flag is set as order

    #------
    #Return
    #------
    #This returns the user details get list as string

    global flag;
    flag ='details'
    return 'Enter User Details in the format: Name Street City PhoneNumber'

def split_user_details(userText):
    #-----------
    #Description 
    #-----------
    #This is used to split user details when the flag is set as details
    #[generates order id for that user]

    #----------
    #Parameters
    #----------
    #The given user input is passen as parameter

    #------
    #Return
    #------
    #This returns the category list as string
    global user_id;
    global name;
    global street;
    global place;
    global phone;

    user_input=userText.split()
    name = user_input[0]
    street = user_input[1]
    place = user_input[2]
    phone = user_input[3]
    today = datetime.today()  
    year =today.year
    month =today.month    
    now= datetime.now()
    current_time = now.strftime("%H:%M:%S")
    time_split = current_time.split(':')
    user_id ='yoyo' + str(year) + str(month) + time_split[0] + time_split[1] 
    return 'Enter your category: Veg Non-Veg'

def veg_list_category():
    #-----------
    #Description 
    #-----------
    #This is used to show the category list of the veg pizzas from the database 
    #flag is set to veg


    #------
    #Return
    #------
    #This returns the category list as string
    global connection;
    global cur;
    global veg_list;
    global flag;
    flag = 'veg'
    sql ='Select name from veg_list'
    cur.execute(sql)
    connection.commit()
    myresult =cur.fetchall()
    print("##################")
    print(myresult)
    print(type(myresult))

    for i in range(0,len(myresult)):
        print(myresult[i][0])
        print(type(myresult[i][0]))
        veg_list += "Name: " + myresult[i][0] + ","
    return "Enter only the name of the pizza (One at a time ) :" + veg_list

def non_veg_list_category():
    #-----------
    #Description 
    #-----------
    #This is used to show the category list of the non veg pizzas from the database 
    #flag is set to nonveg


    #------
    #Return
    #------
    #This returns the category list as string

    global connection;
    global cur;
    global nv_list;
    global flag;
    flag='nonveg'
    sql ='Select name from non_veg'
    cur.execute(sql)
    connection.commit()
    myresult =cur.fetchall()
    for i in range(0,len(myresult)):
        nv_list += "Name: " + myresult[i][0] + ","
    return "Enter only the name of the pizza (one at a time):" + nv_list
            
def veg_after_ordering(variety,user_input):
    #push into db of the upcoming data as pizza item 
    #-----------
    #Description 
    #-----------
    #This is used to display the order id and details after ordering
    #Inserts the user details into the database

    #----------
    #Parameters
    #----------
    #The given user input, flag value  is passed as parameter

    #------
    #Return
    #------
    #This returns the details of ordering as string

    global user_id;
    global name;
    global street;
    global place;
    global phone;
    global user_id;
    global connection;
    global cur;
    global flag;

    current_time = datetime.now()
    status ='Order Received' 
    print(user_id+"-"+str(type(user_id)))

    sql ="""INSERT INTO user_details(id,name,street,place,category,food,status,time,phone) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    record_to_insert = (user_id,name,street,place,flag,user_input,status,current_time,phone,)
    cur.execute(sql,record_to_insert)
    connection.commit()
    myresult = "Your order id is : " + user_id + "    "+ '. ' + "Order on " + variety +" placed. " + "    " + 'To know about the status enter "status"!!!'
    flag = '' 
    return myresult


def order_status_by_user(user_input):
    #-----------
    #Description 
    #-----------
    #This is used to view the status of food ordered
    #[generates order id for that user]

    #----------
    #Parameters
    #----------
    #The given user input is passed as parameter

    #------
    #Return
    #------
    #This returns the status of the food 
    global connection;
    global cur;
    global flag;

    flag =''
    sql = 'select time from user_details where id=%s'
    cur.execute(sql,user_input)
    myresult =cur.fetchall()
    connection.commit()
    if is_empty(myresult):
        flag =''
        return "Invalid order ID"
    current_time = datetime.now()
    order_time = myresult[0][0]
    print(type(order_time))
    print(type(current_time))
    rem_time = current_time-order_time
    time_diff = rem_time.seconds/60
        
    if time_diff >= 0 and time_diff <= 15:
        sql = "UPDATE user_details SET status = 'Preparation started' WHERE id = %s"
        cur.execute(sql,user_input)
        connection.commit()
        return 'Preparation started'
    if time_diff >15 and time_diff <= 30:
        sql = "UPDATE user_details SET status = 'Pizza Cooking' WHERE id = %s "
        cur.execute(sql,user_input)
        connection.commit()
        return 'Pizza Cooking'
    if time_diff > 30 and time_diff <= 45: 
        sql = "UPDATE user_details SET status = 'Cooking Finished' WHERE id = %s"
        cur.execute(sql,user_input)
        connection.commit()
        return 'Cooking Finished'
    if time_diff > 45 and time_diff <=60:
        sql = "UPDATE user_details SET status = 'Out for Delivery' WHERE id = %s"
        cur.execute(sql,user_input)
        connection.commit()
        return 'Out for Delivery'
    if time_diff >60:
        sql = "UPDATE user_details SET status = 'Pizza Delivered' WHERE id = %s"
        cur.execute(sql,user_input)
        connection.commit()
        return 'Pizza Delivered'

def is_empty(any_structure):
    #-----------
    #Description 
    #-----------
    #This is used to check if a tuple is empty or not
    
    #----------
    #Parameters
    #----------
    #The tuple is passed as parameter

    #------
    #Return
    #------
    #This returns boolean
    if any_structure:
        return False
    else:
        return True

if __name__ == "__main__":
    # create_tables()
    app.run() 