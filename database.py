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
#import requests


engine = create_engine('sqlite:///my.db', connect_args={'check_same_thread': False}, echo=True)
Base = declarative_base()
For_data = sessionmaker(autocommit=False, autoflush=False,bind=engine)
for_data = For_data()

class Users(Base):
	__tablename__ = 'Users'
	UserID = Column(Integer, primary_key=True,autoincrement=True)
	Username = Column(String(80))
	Email = Column(String(120))
	First_name = Column(String(120))
	Last_name = Column(String(120))
	Password = Column(String(80))
	Phone = Column(Integer, autoincrement = False)
	Prop = Column(String(50))


class Ad(Base):
	__tablename__ = 'Ad'
	AdID = Column(Integer, primary_key=True,autoincrement=True)
	UserID = Column(Integer, ForeignKey("Users.UserID", ondelete='CASCADE'), nullable = False) 
	#user_name = relationship("Users", backref='Username')
	
	Type = Column(String(15))
	Area = Column(String(10))
	Purpose = Column(String(15))
	Price = Column(Float)
	Size = Column(Float)
	Description = Column(String(300))
	Image=Column(String(80))
	User = relationship("Users", backref="Ad")

def encryption(p):
	pwd = pbkdf2_sha256.encrypt(p, rounds=20000, salt_size= 16)
	return pwd 

def verification(p1,pw):
	return pbkdf2_sha256.verify(p1,pw)	 
	

Base.metadata.create_all(engine,checkfirst=True)

jack = Users(UserID = 1, Username = u'jack_sm', Email = u'jack_sm@gmail.com',First_name=u'Jack',Last_name=u'Smith', Password = encryption('heyyy'), Phone = u'6985555555', Prop = u'User')
james = Users(UserID = 2, Username = u'james_john',Email = u'james_j@gmail.com',First_name=u'James',Last_name=u'John', Password= encryption('heyyy'), Phone = u'6981111111', Prop = u'User')
oliver = Users(UserID = 3, Username = u'oliver_brwn',Email = u'oliver_b@gmail.com',First_name=u'Oliver',Last_name=u'Brown', Password= encryption('heyyy'), Phone = u'6982222222', Prop = u'User')
lewis = Users(UserID = 4, Username = u'lewis_j',Email = u'lewis_j@gmail.com',First_name=u'Lewis',Last_name=u'Jones', Password= encryption('heyyy'), Phone = u'6983333333', Prop = u'Admin') 
logan = Users(UserID = 5, Username = u'logan_ml',Email = u'logan_m@gmail.com',First_name=u'Logan',Last_name=u'Miller', Password= encryption('heyyy'), Phone = u'6984444444', Prop = u'User')
harry = Users(UserID = 6, Username = u'harry_dv',Email = u'harry_d@gmail.com',First_name=u'Harry',Last_name=u'Davis', Password= encryption('heyyy'), Phone = u'6986666666', Prop = u'Admin')



jack1 = Ad(AdID = 1, User = jack, Type = u'Land', Area = u'Athens-East', Purpose = u'Buy', Price =  250000, Size = 1020, Description = 'Within urban plan: No, Facade: Yes, Facade length: 60 meters, Corner: Yes, Road type: Asphalt road, Investment: No, Agricultural use: No',Image=u'oikopedo4.jpg' )
james1 = Ad(AdID = 2, User= james, Type = u'House', Area = u'Center', Purpose = u'Rent', Price =  2500, Size = 150, Description = 'Bedrooms: 3, Air condition: Yes, Fireplace: Yes, Secure door: Yes, Double glass: Yes, Window screens: Yes',Image=u'2.jpg')
harry1 = Ad(AdID = 3, User = harry, Type = u'House', Area = u'Athens-South', Purpose = u'Buy', Price =  65000, Size = 1000, Description = '2 Living rooms, 1 Kitchens, 2 WC, Floors type: Wood, Attic: Yes, Fireplace: Yes, Playroom: Yes, Secure door: Yes, Elevator: Yes, Furnished: Yes, Internal staircase: Yes, Frames type: Aluminium, Double glass: Yes, Window screens: Yes',Image=u'3.jpg')
logan1 = Ad(AdID = 4, User = logan, Type = u'Land', Area = u'Athens-East', Purpose = u'Rent', Price =  420000, Size = 1000, Description = 'Within urban plan: No, Facade: No, Corner: No, Residential zone, Investment: No, Agricultural use: No ',Image=u'oikopedo3.jpg')
oliver1 = Ad(AdID = 5, User = oliver, Type = u'Professional Space', Area = u'Center', Purpose = u'Rent', Price = 320, Size = 50, Description = '1 WC, Air condition: Yes, Furred ceiling: No, Structured cabling: Yes, Equipped: No, Painted: No, UnderFloor: No',Image=u'epag1.jpg')
oliver2 = Ad(AdID = 6, User = oliver, Type = u'Professional Space', Area = u'Center', Purpose = u'Buy', Price = 295000 , Size = 270, Description = 'Floors type: Industrial, Air condition: Yes, Furred ceiling: No, Structured cabling: Yes, Internal staircase: No, Equipped: No, Current: Three phase, Painted: Yes, UnderFloor: No ',Image=u'epag2.jpg' )
lewis1 = Ad(AdID = 7, User = lewis, Type = u'House', Area = u'Athens-North', Purpose = u'Rent', Price = 550 , Size = 148, Description = '1 Kitchens, Air condition: No, Attic: No, Fireplace: No, Playroom: No, Secure door: No, Elevator: Yes, Furnished: No, Internal staircase: No, Double glass: No, Window screens: No, Painted: No, UnderFloor: No', Image=u'spiti3.jpg') 
lewis2 = Ad(AdID = 8, User = lewis, Type = u'Professional Space', Area = u'Athens-East', Purpose = u'Buy', Price = 89000 , Size = 35, Description = '1 Living rooms, 1 Kitchens, Double glass: Yes, Garden: Yes, Road type: Asphalt road ', Image = 'epag3.JPG')
logan2 = Ad(AdID = 9, User = logan, Type = u'Land', Area = u'Athens-South', Purpose = u'Buy', Price = 250000 , Size = 528, Description = ' Slope: Plane, Coverage ratio: 40, Within urban plan: Yes, Facade length: 14 meters, Residential zone, Road type: Asphalt road, Distance from sea (m): 250 meters ', Image = 'oikopedo1.jpg')
harry2 = Ad(AdID = 10, User = harry, Type = u'Land', Area = u'Athens-North', Purpose = u'Buy', Price = 300000 , Size = 417, Description = ' View: No, Slope: Plane, Orientation: East meridian, Coverage ratio: 40 Extra, Within urban plan: Yes, Facade: Yes, Facade length: 20 meters, Corner: Yes, Residential zone, Road type: Asphalt road, Investment: Yes, Agricultural use: No ', Image = 'oikopedo2.jpg')
jack2 = Ad(AdID = 11, User = harry, Type = u'House', Area = u'Center', Purpose = u'Rent', Price = 1200 , Size = 95, Description = 'Air condition: Yes, Attic: No, Fireplace: No, Playroom: No, Secure door: No, Elevator: No, Furnished: Yes, Double glass: Yes, Window screens: No, Painted: Yes, UnderFloor: No, Garden: No, Balcony: No, Awning: No ', Image = 'spiti2.jpg')


try:
	for_data.add_all([jack, james, oliver, lewis, logan, harry])
	for_data.commit()
except exc.SQLAlchemyError:
	pass

try:
	for_data.add_all([jack1, james1, harry1, logan1, oliver1, oliver2, lewis2, logan2, harry2, jack2])
	for_data.commit()
except exc.SQLAlchemyError:
	pass











