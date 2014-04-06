from flask import Flask, request, redirect, render_template, Markup
import os
from urllib import urlopen, urlencode
import json
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import random
import redis
import sys


import pymongo 
from pymongo import MongoClient
mongoHQurl = urlencode('mongodb://aaron:reddit123@oceanic.mongohq.com:10024/starhub')
client = MongoClient(mongoHQurl)
users_collection = client.starhub.users

email_collection = client.starhub.emails

import os
app = Flask(__name__)

users = []
queue = []

userCountObj = users_collection.find_one({'counter': 1})
if userCountObj == None:
	users_collection.insert({'counter' : 1, 'count' : 0})
	userCountObj = users_collection.find_one({'counter': 1})
userCount = userCountObj['count']

redisCounter = 0

def userCheck(username, password):
	driver = webdriver.PhantomJS("phantomjs")
	loginUrl = urlencode("https://github.com/login")
	driver.get(loginUrl)
	print 'get'
	driver.execute_script("""
		var form_body = document.getElementsByClassName('auth-form-body')[0];
		var login_field = document.getElementById('login_field');
		var password_field = document.getElementById('password');
		var submit_button = form_body.children[4];

		login_field.value = '%s';
		password_field.value = '%s';
		submit_button.click();"""%(username, password ))

	print 'execute'
	time.sleep(.15)	
	try:
		source = Markup(driver.page_source)
		soup = BeautifulSoup(source)
		username = soup.findAll("a", { "class" : "name"})[0].contents
		print username
		return True
	except:
		return False
	#return source


@app.route('/', methods=['GET'])
def home():
	return render_template('home.html', error = "", userCount = userCount);
	#parse('aaln', 'reddit123', 'http')
@app.route('/signup', methods=['GET', 'POST'])
def signup():
	username = request.form['username']
	password = request.form['password']
	repo = request.form['repo']
	userObj = users_collection.find_one({'username' : username})
	if userObj != None:
		return render_template('home.html', error = "This user is already registered.", userCount = userCount)
	else:
		userStatus = userCheck(username, password)
		if userStatus == True:
			users_collection.insert({'username' : username, 'password' : password, 'repo' : repo})

			return render_template('home.html', error = "Success! Check your repo for constant starring as more people join.", userCount = userCount)
		else:
			return render_template('home.html', error = "Your username and/or password is incorrect.", userCount = userCount)

def initUser(username, password):
	allUsers = list(users_collection.find())
	chosenUsers = random.sample(allUsers, len(allUsers) / 2)
	

	r.publish





def parse(username, password, repo):
	driver = webdriver.PhantomJS("phantomjs")
	#js_script = "var form_body=document.getElementsByClassName('auth-form-body')[0];var login_field=document.getElementById('login_field');var password_field=document.getElementById('password');var submit_button=form_body.children[4];login_field.value='" + username + "';password_field.value='" + password + "';submit_button.click()"
	loginUrl = urlencode("https://github.com/login")

	driver.get(loginUrl)

	driver.execute_script("""
		var form_body = document.getElementsByClassName('auth-form-body')[0];
		var login_field = document.getElementById('login_field');
		var password_field = document.getElementById('password');
		var submit_button = form_body.children[4];

		login_field.value = '%s';
		password_field.value = '%s';
		submit_button.click();"""%(username, password ))
	
	time.sleep(1)
	driver.execute_script("""
		var metas = document.getElementsByTagName('meta');
		var csrf_token = "";
		for (var i = 0; i < metas.length; i++) {
			if (metas[i].getAttribute("name") === "csrf-token") {
		        csrf_token = metas[i].getAttribute("content");
		    }
		}

		var myRequest1 = new XMLHttpRequest();
		var url1 = "%s/star";
		
		myRequest1.open("POST", url1, true);
		myRequest1.setRequestHeader("X-CSRF-Token", csrf_token);
		myRequest1.send()

		var myRequest2 = new XMLHttpRequest();
		var url2 = "https://github.com/users/follow?target=ericz";
		
		myRequest2.open("POST", url2, true);
		myRequest2.setRequestHeader("X-CSRF-Token", csrf_token);
		myRequest2.send()

		//var sb = document.getElementsByClassName('star-button');
		//sb[1].click();

	""" % (repo))
	driver.quit
	#time.sleep(5)
	#
	source = Markup(driver.page_source)
	return source

	

	
if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT',5000))
    app.run(host='0.0.0.0', port=port)