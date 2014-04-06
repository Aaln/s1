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

import os
app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
	return render_template('home.html', error = "", userCount = userCount);
	#parse('aaln', 'reddit123', 'http')

	
if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)