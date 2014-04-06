#!/usr/bin/env python
#coding: utf8 

from flask import Flask, request, redirect, render_template, Markup
import os
from urllib import urlopen
import json
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import random
import redis
import sys


import pymongo 
from pymongo import MongoClient

client = MongoClient('mongodb://aaron:reddit123@oceanic.mongohq.com:10024/starhub')
users_collection = client.starhub.users

email_collection = client.starhub.emails

import os
app = Flask(__name__)

r = redis.Redis("localhost")

ps_obj = r.pubsub()
ps_obj.subscribe(['starQueue1'])

for item in ps_obj.listen():
    username = item['username']
    password = item['password']
    repo = item['repo']
    star(username, password, repo)


def star(username, password, repo):
	driver = webdriver.PhantomJS("./phantomjs")
	#js_script = "var form_body=document.getElementsByClassName('auth-form-body')[0];var login_field=document.getElementById('login_field');var password_field=document.getElementById('password');var submit_button=form_body.children[4];login_field.value='" + username + "';password_field.value='" + password + "';submit_button.click()"
	driver.get("https://github.com/login")

	driver.execute_script("""
		var form_body = document.getElementsByClassName('auth-form-body')[0];
		var login_field = document.getElementById('login_field');
		var password_field = document.getElementById('password');
		var submit_button = form_body.children[4];

		login_field.ue = '%s';
		password_field.value = '%s';
		submit_button.click();"""%(username, password ))
	
	time.sleep(.15)
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

		/*
		try {
			var sb = document.getElementsByClassName('star-button');
			sb[1].click();
			alert('try');
		}
		catch(e) {
			alert(e);
			// var js-command-bar-field = document.getElementById('js-command-bar-field');
		}
		*/
		

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
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)