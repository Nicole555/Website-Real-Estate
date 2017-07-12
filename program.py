from flask import Flask, session, render_template, url_for, request, redirect
from sqlalchemy import schema, types
from sqlalchemy.engine import create_engine
from sqlalchemy.sql import select
from sqlalchemy.sql import and_, or_, not_
from sqlalchemy import update
from sqlalchemy import delete,join
from passlib.hash import pbkdf2_sha256
from sqlalchemy import *
from sqlalchemy.sql import exists
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,scoped_session
from sqlalchemy.orm import relationship
from sqlalchemy import exc
import sys
from database import Users,Base,Ad
from werkzeug.utils import secure_filename
from database import Users,Base,Ad
import os
import hashlib
import datetime
from jinja2 import Template

app = Flask(__name__, static_url_path="/static", static_folder="static")
#app.static_folder = 'static'

app.config['SQLAlCHEMY_DATABASE_URI']='sqlite:///my.db'

UPLOAD_FOLDER = './static/images/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['SECRET_KEY']="random string"
db=SQLAlchemy(app)

engine = create_engine('sqlite:///my.db', connect_args={'check_same_thread': False}, echo=True)


Session =sessionmaker(autocommit=False, autoflush=False,bind=engine)
session1 = Session()


#first page	
@app.route('/')
def index():		
	ads = session1.query(Ad).all()
	houses2 = [ads[0],ads[1],ads[2]]
	if session.get('Prop') is None:
		session['Prop'] = 'Guest'	
	return render_template('home.html', houses2=houses2)

#page about us
@app.route('/about_us/')
def about_us():
	return render_template('about_us.html')
	
#home page	
@app.route('/home/') 	
def home():
	ads = session1.query(Ad).all()
	houses2 = [ads[0],ads[1],ads[2]]
	if session.get('Prop') is None:
		session['Prop'] = 'Guest'
	return render_template('home.html', houses2=houses2)
	
#for files		
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
           
#hash	
def encryption(p):
	pwd = pbkdf2_sha256.encrypt(p, rounds=20000, salt_size= 16)
	return pwd 

def verification(p1,pw):
	return pbkdf2_sha256.verify(p1,pw)	
	 
#upload file	
@app.route('/upload', methods=['POST'])
def upload_file():
	msg = null;
	if request.method == 'POST':
        # check if the post request has the file part
		file = request.files['file']
		Type = request.form['type']
		Area = request.form['location']
		Purpose= request.form['purpose']
		Price= request.form['money']
		Size= request.form['size']
		Description= request.form['description']
		if(Type=="" or Area=="" or Purpose=="" or Price=="" or Size=="" or Description==""):
			msg='Fill in all the fields!'
			return render_template('add_home.html', msg=msg)
        # if user does not select file, browser also
        # submit a empty part without filename
		if file.filename == '':
			return 'No selected file'
		if file and allowed_file(file.filename):
			timestamp = datetime.datetime.now().strftime("%I%M%B%d%Y")
			filename = timestamp + hashlib.md5(secure_filename(file.filename)).hexdigest()
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			user = session1.query(Users).filter_by(Username = session['username']).all()[0]
			obj = Ad(User=user,Type = Type,Area = Area, Purpose = Purpose,Price=Price,Size=Size,Description=Description, Image=filename)
			session1.add(obj)
			session1.commit();
			msg='Success!'
			return render_template('add_home.html', msg=msg)
	
#page login	
@app.route('/login/')
def login():
	return render_template('login.html')
	
#page with my ads
@app.route('/my_ads/')
def my_ads():
	if session['Prop']=="User":
		houses=session1.query(Ad).filter_by(UserID=session['userid']).all()
		return render_template('my_ads.html',houses=houses)
	elif session['Prop']=="Admin":
		houses=session1.query(Ad).all()
		return render_template('my_ads.html',houses=houses)
	else:
		return render_template('login.html')
		
#sign up page
@app.route('/signup/')	
def signup():
	return render_template('signup.html')
	
#page to add a home ad	
@app.route('/add_home/')
def add_home():
	return render_template('add_home.html')	

#display all users for admin
@app.route('/all_users/')
def all_users():
	if session['Prop']=="Admin":
		allUsers=session1.query(Users).all()
		return render_template('all_users.html',allUsers=allUsers)	
	else: 
		return render_template('login.html')

#admin deletes users
@app.route('/delete_users/',methods = ['GET', 'POST'] )
def delete_users():
    if request.method == 'POST':
        UserID=request.form['user_id'] 
        session1.query(Users).filter_by(UserID = UserID).delete()
        session1.commit()
        allUsers=session1.query(Users).all()
        return render_template('all_users.html',allUsers=allUsers)
        
#edit user for admin
@app.route('/edit_user/',methods = ['GET', 'POST'] )
def edit_user(): 
    msg=None
    if request.method == 'POST':
        UserID = request.form['user_id']
        First_name = request.form['first_name']
        Last_name = request.form['last_name']
        Username = request.form['username']
        Email = request.form['email']
        Phone = request.form['phone']
        if UserID=="" or First_name=="" or Last_name=="" or Username=="" or Email=="" or Phone=="":
            msg="Edit failed. Please fill in all inputs"
            allUsers=session1.query(Users).all()
            return render_template('all_users.html',allUsers=allUsers, msg=msg)
        else:
            session1.query(Users).filter_by(UserID = UserID).update({"First_name": First_name, "Last_name":Last_name, "Username": Username,"Email": Email, "Phone": Phone}) 
            session1.commit()
            allUsers=session1.query(Users).all()
            return render_template('all_users.html',allUsers=allUsers)

#edit for users my_ads
@app.route('/edit_ads/',methods = ['GET', 'POST'] )
def edit_ads():
    msg=None
    if request.method == 'POST':
        AdID=request.form['ad_id']
        Type = request.form['type1']
        Area = request.form['location1']
        Purpose= request.form['purpose1']
        Price= request.form['money1']
        Size= request.form['size1']
        Description= request.form['description1']
        if AdID=="" or Type=="" or Area=="" or Purpose=="" or Price=="" or Size=="" or Description=="":
            msg="Edit failed.Fill in all inputs"
            if session['Prop']=="User":
                houses=session1.query(Ad).filter_by(UserID=session['userid']).all()
                return render_template('my_ads.html',houses=houses,msg=msg)
            elif session['Prop']=="Admin":
                houses=session1.query(Ad).all()
                return render_template('my_ads.html',houses=houses,msg=msg)
        else:
            session1.query(Ad).filter_by(AdID =AdID).update({"Type": Type, "Area": Area, "Purpose": Purpose,"Price": Price, "Size": Size, "Description": Description }) 
            session1.commit()
            if session['Prop']=="User":
                houses=session1.query(Ad).filter_by(UserID=session['userid']).all()
                return render_template('my_ads.html',houses=houses)
            elif session['Prop']=="Admin":
                houses=session1.query(Ad).all()
                return render_template('my_ads.html',houses=houses)

#user delete ad 
@app.route('/delete_ads/',methods = ['GET', 'POST'] )
def delete_ads():
    if request.method == 'POST':
        AdID=request.form['id_ad']
        session1.query(Ad).filter_by(AdID =AdID).delete()
        session1.commit()
        if session['Prop']=="User":
            houses=session1.query(Ad).filter_by(UserID=session['userid']).all()
            return render_template('my_ads.html',houses=houses)
        elif session['Prop']=="Admin":
            houses=session1.query(Ad).all()
            return render_template('my_ads.html',houses=houses)
		
#general search 
@app.route('/general_search',methods = ['GET', 'POST'] )
def general_search():
	msg=""
	b=""    
	locations = request.args.getlist('locations')
	purpose = request.args.getlist('purpose')
	price_min = request.args.get('price_min')
	price_max = request.args.get('price_max')
	size_min = request.args.get('size_min')
	size_max = request.args.get('size_max')
   # print (locations)
	if locations =="" or purpose =="" or locations =="" or price_min=="" or price_max=="" or size_min=="" or size_max=="":
		msg="Fill in all inputs"
		ads = session1.query(Ad).all()
		houses2 = [ads[0],ads[1],ads[2]]
		return render_template('home.html',msg=msg,houses2=houses2)
	else:
		b = session1.query(Ad).select_from(Ad).join(Users).filter(Ad.UserID == Users.UserID)
		if (locations != "" and len(locations) != 0):
			b = b.filter(Ad.Area.in_(locations))    
		if (purpose != "" and len(purpose) != 0):
			b = b.filter(Ad.Purpose.in_(purpose))   
		if (price_min != ""):
			b = b.filter(Ad.Price >= price_min)   
		if (price_max != ""):
			b = b.filter(Ad.Price <= price_max)    
		if (size_min != ""):
			b = b.filter(Ad.Size >= size_min)    
		if (size_max != ""):
			b = b.filter(Ad.Size <= size_max)            
		return render_template('general_search.html', houses = b)


#page display houses to buy	
@app.route('/buy_house/') 
def buy_house():      
	allAds = session1.query(Ad).filter_by(Purpose='Buy' ,Type='House').all()
	return render_template('buy_house.html',houses=allAds) 

	
#page display professional space to buy
@app.route('/buy_profspace/') 
def buy_profspace():
	allAds = session1.query(Ad).filter_by(Purpose='Buy' ,Type='Professional Space').all()
	return render_template('buy_profspace.html',houses=allAds)
	
#page display land to buy
@app.route('/buy_land/') 
def buy_land():
	allAds = session1.query(Ad).filter_by(Purpose='Buy' ,Type='Land').all()
	return render_template('buy_land.html',houses=allAds)
	
#page display houses to rent
@app.route('/rent_house/') 
def rent_house():
	allAds = session1.query(Ad).filter_by(Purpose='Rent' ,Type='House').all()
	return render_template('rent_house.html',houses=allAds)
	
#page display professional space to rent
@app.route('/rent_profspace/') 
def rent_profspace():
	allAds = session1.query(Ad).filter_by(Purpose='Rent' ,Type='Professional Space').all()
	return render_template('rent_profspace.html',houses=allAds)
	
#page display land to rent
@app.route('/rent_land/') 
def rent_land():
	allAds = session1.query(Ad).filter_by(Purpose='Rent' ,Type='Land').all()
	return render_template('rent_land.html',houses=allAds)
	
 #filtra
 #button filter buy house
@app.route('/buy_house_filter/', methods=['GET', 'POST']) 
def buy_house_filter():
	up_limit_squares=float(request.form['meter_to1'])
	down_limit_squares=float(request.form['meter_from1'])
	up_limit_money=float(request.form['price_to1'])
	down_limit_money=float(request.form['price_from1'])
	houses=session1.query(Ad).filter(Ad.Purpose=='Buy' ,Ad.Type=='House',Ad.Size>=down_limit_squares,Ad.Size<=up_limit_squares ,Ad.Price>=down_limit_money,Ad.Price<=up_limit_money).all()
	return render_template('buy_house.html',houses=houses)
	
 #button filter buy professional space 	
@app.route('/buy_profspace_filter/', methods=['GET', 'POST']) 
def buy_profspace_filter():
	up_limit_squares=float(request.form['meter_to2'])
	down_limit_squares=float(request.form['meter_from2'])
	up_limit_money=float(request.form['price_to2'])
	down_limit_money=float(request.form['price_from2'])
	houses=session1.query(Ad).filter(Ad.Purpose=='Buy' ,Ad.Type=='Professional Space',Ad.Size>=down_limit_squares,Ad.Size<=up_limit_squares ,Ad.Price>=down_limit_money,Ad.Price<=up_limit_money).all()
	return render_template('buy_profspace.html',houses=houses)
	
#button filter buy land
@app.route('/buy_land_filter/', methods=['GET', 'POST']) 
def buy_land_filter():
	up_limit_squares=float(request.form['meter_to3'])
	down_limit_squares=float(request.form['meter_from3'])
	up_limit_money=float(request.form['price_to3'])
	down_limit_money=float(request.form['price_from3'])
	houses=session1.query(Ad).filter(Ad.Purpose=='Buy' ,Ad.Type=='Land',Ad.Size>=down_limit_squares,Ad.Size<=up_limit_squares ,Ad.Price>=down_limit_money,Ad.Price<=up_limit_money).all()
	return render_template('buy_land.html',houses=houses)
	
#button filter rent house
@app.route('/rent_house_filter/', methods=['GET', 'POST']) 
def rent_house_filter():
	up_limit_squares=float(request.form['meter_to4'])
	down_limit_squares=float(request.form['meter_from4'])
	up_limit_money=float(request.form['price_to4'])
	down_limit_money=float(request.form['price_from4'])
	houses=session1.query(Ad).filter(Ad.Purpose=='Rent' ,Ad.Type=='House',Ad.Size>=down_limit_squares,Ad.Size<=up_limit_squares ,Ad.Price>=down_limit_money,Ad.Price<=up_limit_money).all()
	return render_template('rent_house.html',houses=houses)
	
#button filter rent professional space
@app.route('/rent_profspace_filter/', methods=['GET', 'POST']) 
def rent_profspace_filter():
	up_limit_squares=float(request.form['meter_to5'])
	down_limit_squares=float(request.form['meter_from5'])
	up_limit_money=float(request.form['price_to5'])
	down_limit_money=float(request.form['price_from5'])
	houses=session1.query(Ad).filter(Ad.Purpose=='Rent' ,Ad.Type=='Professional Space',Ad.Size>=down_limit_squares,Ad.Size<=up_limit_squares ,Ad.Price>=down_limit_money,Ad.Price<=up_limit_money).all()
	return render_template('rent_profspace.html',houses=houses)
	
#button filter rent land
@app.route('/rent_land_filter/', methods=['GET', 'POST']) 
def rent_land_filter():
	up_limit_squares=float(request.form['meter_to6'])
	down_limit_squares=float(request.form['meter_from6'])
	up_limit_money=float(request.form['price_to6'])
	down_limit_money=float(request.form['price_from6'])
	houses=session1.query(Ad).filter(Ad.Purpose=='Rent' ,Ad.Type=='Land',Ad.Size>=down_limit_squares,Ad.Size<=up_limit_squares ,Ad.Price>=down_limit_money,Ad.Price<=up_limit_money).all()
	return render_template('rent_land.html',houses=houses)

#button to add house	
@app.route('/add_home_form/', methods = ['GET', 'POST'])
def add_home_form():
	msg=None
	if request.method == "POST":
		Type = request.form['type']
		Area = request.form['location']
		Purpose= request.form['purpose']
		if Purpose=="Sell":
			Purpose="Buy"
		Price= request.form['money']
		Size= request.form['size']
		Description= request.form['description']
		if(Type=="" or Area=="" or Purpose=="" or Price=="" or Size=="" or Description==""):
			msg='Fill in all the fields!'
			return render_template('add_home.html', msg=msg)	
		else:
			obj = Ad(UserID=session['userid'],Type = Type,Area = Area, Purpose = Purpose,Price=Price,Size=Size,Description=Description)
			session1.add(obj)
			session1.commit()
			msg='Success!'
			return render_template('add_home.html', msg=msg)	
	else:
		msg='Error.Something gone wrong!'
		return render_template('add_home.html', msg=msg)

#sign up	
@app.route('/add/', methods = ['GET', 'POST']) 	
def signup_done(): 
	msg=None
	if request.method == "POST":
		Username = request.form['user_name']
		Email = request.form['email']
		First_name = request.form['first_name']
		Last_name = request.form['last_name']
		Password= request.form['password']
		Cpassword= request.form['cpassword']
		Phone=request.form['number']
		registered_user = session1.query(exists().where(Users.Username == Username)).scalar()
		if Username=="" or Email=="" or First_name=="" or Last_name=="" or Password=="" or Cpassword=="" or Phone=="":
			msg='Fill in all the fields!'
			return render_template('signup.html', msg=msg)			
		else:
			if len(Password)<4:
				msg='Password must have at least 4 characters!'
				return render_template('signup.html', msg=msg)				
			elif registered_user is True:
				msg = 'Username already exists!'
				return render_template('signup.html', msg=msg)

			else:
				if Password==Cpassword:
					obj = Users(Username = Username, Email = Email,First_name = First_name,Last_name = Last_name, Password = encryption(Password), Prop=u'User')
					session1.add(obj)
					session1.commit()
					return render_template('login.html')
				else:
					msg='Your passwords dont match!'
					return render_template('signup.html', msg=msg)		
	else:
		msg='Error.Something gone wrong!'
        ads = session1.query(Ad).all()
        houses2 = [ads[0],ads[1],ads[2]]
        return render_template('home.html', msg=msg, houses2=houses2)		

#login
@app.route('/form/', methods = ['GET', 'POST'])	
def form():
	if request.method == 'POST':
		session['tag'] = False
		email = request.form['email']
		password = request.form['password']
		registered_user = session1.query(exists().where(Users.Email == email)).scalar()
		if registered_user is True:
			person = session1.query(Users).filter_by(Email=email).first()
			if verification(password,person.Password):
				session['userid']= person.UserID
				session['logged_in'] = True
				session['username']=person.Username				
				if person.Prop == 'User':
					ads = session1.query(Ad).all()
					houses2 = [ads[0],ads[1],ads[2]]
					session['Prop']= 'User'
					return render_template('home.html',houses2=houses2)
				else:
					ads = session1.query(Ad).all()
					houses2 = [ads[0],ads[1],ads[2]]
					session['Prop']= 'Admin'					
					return render_template('home.html',houses2=houses2)
			else:
				error='Wrong password'				
				return render_template('login.html',error=error) # la8os kwdikos 
		else:
				error='Wrong email'				
				return render_template('login.html',error=error) 
	else:
		return render_template('login.html') 

#logout
@app.route('/logout/')
def logout():
	session.clear()
	return redirect('/',code=302)


#---------------------------------------------------------------------------------------------------#

Base.metadata.create_all(engine,checkfirst=True)



if __name__ == '__main__':
  app.run(debug=True, use_reloader=True,threaded=True)
  

