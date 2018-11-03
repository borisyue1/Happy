from app import app
from flask import render_template, flash, redirect, request
import json
from scripts import faces

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

