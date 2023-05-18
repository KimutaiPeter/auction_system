from flask import render_template ,Flask,request,redirect,url_for
from flask_socketio import SocketIO
import threading
import pymysql
import json
from datetime import datetime,timedelta



app=Flask(__name__)
app.config['SECRET_KEY']='It is a secret'
socket=SocketIO(app)




connection= pymysql.connect(host='localhost',user='root',password='',database='bid_project')
cursor=connection.cursor()




@app.route('/')
def login_page():
    return render_template('Login.html')

@app.route('/register_page')
def register_page():
    return render_template('register.html')


@app.route('/controls')
def controls_page():

    if(True):
        cursor.execute("SELECT `product_id`, `product_name`, `winning_user_id`, `time_set_forward` FROM `product_table`;")
        result=cursor.fetchall()
        prep=[]
        for item in result:
            #prep[item[0]]={'id':item[0],'name':item[1]}
            prep.append({'id':item[0],'name':item[1]})
        print(prep)
        return render_template('control.html',data=prep)
    else:
        return render_template('Login.html')






@app.route('/new_long_term_item', methods=['POST','GET'])
def new_long_term_item():
    item_name=request.form['name']
    item_time=request.form['time']
    item_date=request.form['date']
    item_market_price=int(request.form['price'])

    insert_date_time="{} {}".format(item_date,item_time)
    print(insert_date_time)
    currently=datetime.now()
    now="{}-{}-{} {}:{}:{}".format(currently.year,currently.month,currently.day,currently.hour,currently.minute,currently.second)
    #query="INSERT INTO `product_table`( `product_name`, `winning_user_id`, `time_set_forward`) VALUES ('"+item_name+"',0,'"+insert_date_time+"');"
    query="INSERT INTO `product_table`( `product_name`, `product_market_price`, `product_type`, `winning_user_id`, `time_set_to_start`, `time_set_forward`) VALUES ('"+item_name+"',"+str(item_market_price)+",'passive',0,'"+now+"','"+insert_date_time+"');"
    indicate=cursor.execute(query)
    if(indicate>0):
        connection.commit()
        return redirect(url_for('controls_page'))
    else:
        return "Database error"







@app.route('/new_short_term_item', methods=['POST','GET'])
def new_short_term_item():
    item_name=request.form['name']
    item_time_extention_seconds=int(request.form['time_seconds'])
    item_time=request.form['time']
    item_date=request.form['date']
    item_market_price=request.form['price']
    now="{} {}".format(item_date,item_time)
    print(item_time,'is the new time')
    d=datetime.strptime('{} {}'.format(item_date,item_time),"%Y-%m-%d %H:%M")


    if(len(now)>0):
        currently=datetime.now()
        #do some math
        insert_date_time=currently+timedelta(seconds=60)
        insert_date_time=insert_date_time.strftime("%Y-%m-%d %H:%M:%S")
        now=currently.strftime("%Y-%m-%d %H:%M:%S")
        print(insert_date_time)
        #query="INSERT INTO `product_table`( `product_name`, `winning_user_id`, `time_set_forward`) VALUES ('"+item_name+"',0,'"+insert_date_time+"');"
        query="INSERT INTO `product_table`( `product_name`, `product_market_price`,`product_type`, `winning_user_id`, `time_set_to_start`, `time_set_forward`) VALUES ('"+item_name+"',"+str(item_market_price)+",'live',0,'"+now+"','"+insert_date_time+"');"
        indicate=cursor.execute(query)
        if(indicate>0):
            return redirect(url_for('controls_page'))
        else:
            return "Database error"
    else:
        return "Error in data, please check your data"


@app.route('/new_short_term_item_time_extention', methods=['POST','GET'])
def new_short_term_item_time_extention():
    item_id=request.form['id']
    item_time_extention_seconds=int(10)

    currently=datetime.now()
    if(currently.second+item_time_extention_seconds>59):
        #do some math
        insert_date_time="{}-{}-{} {}:{}:{}".format(currently.year,currently.month,currently.day,currently.hour,currently.minute+1,currently.second+item_time_extention_seconds-60)
        print(insert_date_time)
        query="UPDATE `product_table` SET `time_set_forward`='"+insert_date_time+"' WHERE `product_id`="+str(item_id)+";"
        indicate=cursor.execute(query)
        if(indicate>0):
            connection.commit()
            return redirect(url_for('controls_page'))
        else:
            return "Database error"
    else:
        insert_date_time="{}-{}-{} {}:{}:{}".format(currently.year,currently.month,currently.day,currently.hour,currently.minute,currently.second+item_time_extention_seconds)
        print(insert_date_time)
        query="UPDATE `product_table` SET `time_set_forward`='"+insert_date_time+"' WHERE `product_id`="+str(item_id)+";"
        indicate=cursor.execute(query)
        if(indicate>0):
            connection.commit()
            return redirect(url_for('controls_page'))
        else:
            return "Database error"




@app.route('/register_processing',methods=['POST','GET'])
def register_processing():
    user_name=request.form['user_name']
    password=request.form['password']

    indicate=cursor.execute("INSERT INTO `users_one`(`user_name`, `user_password`) VALUES ('"+user_name+"','"+password+"');")
    if(indicate>0):
        connection.commit()
        cursor.execute("SELECT `product_id`, `product_name`, `winning_user_id`, `time_set_forward` FROM `product_table`;")
        result=cursor.fetchall()
        prep=[]
        for item in result:
            #prep[item[0]]={'id':item[0],'name':item[1]}
            prep.append({'id':item[0],'name':item[1]})
        print(prep)
        return redirect(url_for('login_page'))
    else:
        return render_template('Login.html')



@app.route('/login',methods=['POST','GET'])
def login_processing():
    user_name=request.form['user_name']
    password=request.form['password']

    indicate=cursor.execute("SELECT * FROM `users_one` WHERE `user_name`='"+user_name+"' and `user_password`='"+password+"';")
    if(indicate>0):
        user_data=cursor.fetchall()
        print(user_data[0][0])
        cursor.execute("SELECT `product_id`, `product_name`,`product_type`,`time_set_to_start`, `winning_user_id`, `time_set_forward` FROM `product_table` where `time_set_forward`>NOW();")
        result=cursor.fetchall()
        prep1=[]
        prep2=[]
        for item in result:
            #prep[item[0]]={'id':item[0],'name':item[1]}
            if(item[2]=='live'):
                prep1.append({'id':item[0],'name':item[1],'time':item[2]})
            else:
                prep2.append({'id':item[0],'name':item[1],'time':item[2]})
        print(prep1)
        return render_template('home.html', live_data=prep1 , passive_data=prep2,user_id=user_data[0][0])
    else:
        return render_template('Login.html')



@app.route('/item_index',methods=['POST','GET'])
def item_index():
    id=request.form['Id']
    user_id=request.form['user_id']
    product_info=cursor.execute("SELECT `product_id`, `product_name`, `winning_user_id`,`product_type`, `time_set_forward`,`product_market_price`,`product_selling_price`,`time_set_to_start` FROM `product_table` where `product_id`="+id+" ;")
    if(product_info>0):
        product_info=cursor.fetchall()
        time=product_info[0][4]
        now=datetime.now()
        remaining_time=time-now
        time_set_to_start=product_info[0][7]
        now_and_start_time_difference=time_set_to_start-now
        if(now_and_start_time_difference.days<0):
            status='Started'
        else:
            status='starts at '+time_set_to_start.strftime("%H:%M:%S on %m/%d/%Y ")
        product_price=0
        if(product_info[0][6]>0):
            product_price=product_info[0][6]
        else:
            product_price=product_info[0][5]
        item_details={'id':product_info[0][0],'name':product_info[0][1],'status':status,'type':product_info[0][3],'price':product_price}
        print(remaining_time.days)
        if(remaining_time.days>=0):
            #Use sessions or something like that to handle the userid
            return render_template('index.html',user_id=user_id,time=remaining_time.seconds,days=remaining_time.days,item_details=item_details)
        else:
            return "This item has been sold"
    else:
        return render_template('home.html')

#sockets and things

@socket.on('connect')
def connect():
    print('Connected')



@socket.on('message')
def test_connect(message):
    print(message,request.sid)



@socket.on('live_bid')
def LiveBid(message):
    print(message,request.sid)
    print(message['user_id'])#Do some user check WHERE
    print(message['item_id'],message['offer_price']) #Do some item checking WHERE
    #if all is well log the bidding action and update the products bidder column and the bid closing time

    new_bid_data=message
    if(message['item_id']!=None):
        product_info=cursor.execute("SELECT `product_id`, `product_name`, `winning_user_id`,`product_type`, `time_set_forward`,`product_market_price`,`time_set_to_start` FROM `product_table` where `product_id`="+str(message['item_id'])+" ;")
        if(product_info>0):
            product_info=cursor.fetchall()

            #if the auction has not started send that user an error message that the bid has not Started
            if(product_info[0][6]>datetime.now()):
                print('The bid has not started, sending error message')
                socket.emit('error',"Im sorry the bid starts at "+product_info[0][6].strftime("%H:%M:%S on %m/%d/%Y "))

            #The bid has started request can proceed
            else:
                #if the type of item auction is live then update the expected time_seconds else just get the time_seconds
                if( product_info[0][3]=='live'):
                    insert_date_time=datetime.now()+timedelta(seconds=20)
                    query="UPDATE `product_table` SET `winning_user_id`='"+str(message['user_id'])+"' ,`time_set_forward`='"+insert_date_time.strftime("%Y-%m-%d %H:%M:%S")+"'  , `product_selling_price`="+str(message['offer_price'])+" WHERE `product_id`="+str(product_info[0][0])+";"
                    indicate=cursor.execute(query)
                    if(indicate>0):
                        connection.commit()
                        print('Item updated successfully to be at'+insert_date_time.strftime("%Y-%m-%d %H:%M:%S"))
                    else:
                        print("Database error")
                #else the bid is passive so just update the users table with the new winning user and their price
                else:
                    query="UPDATE `product_table` SET `winning_user_id`='"+str(message['user_id'])+"',`product_selling_price`="+str(message['offer_price'])+" WHERE `product_id`="+str(product_info[0][0])+";"
                    indicate=cursor.execute(query)
                    if(indicate>0):
                        connection.commit()
                        print('Item winning_user_id, \*currently at. updated successfully')
                    else:
                        print("Database error")

                #everything has been updated so now lets give the time and winning user and his offer price to every users_one
                updated_product_info=cursor.execute("SELECT `product_id`, `product_name`, `winning_user_id`,`product_type`, `time_set_forward`,`product_market_price`,`time_set_to_start` FROM `product_table` where `product_id`="+str(product_info[0][0])+" ;")
                if(updated_product_info>0):
                    updated_product_info=cursor.fetchall()
                    #Getting the time from the
                    time=updated_product_info[0][4]
                    now=datetime.now()
                    remaining_time=time-now


                    new_bid_data['time']=int(remaining_time.seconds)
                    new_bid_data['days']=int(remaining_time.days)
                    new_bid_data['user_id']=int(updated_product_info[0][2])
                    #new_bid_data['time']=None
                    #Notifying everyone of the all the users viewing this product who now has the bid
                    socket.emit('message',new_bid_data)#Use sessions and rooms next time




        else:
            print("The item is not in the database")


if(__name__ == '__main__'):
    socket.run(app,host='0.0.0.0',debug =True)
