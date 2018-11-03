from app import app
from flask import render_template, flash, redirect, request
import json
from .scripts.faces import get_emotions

@app.route('/')
@app.route('/index', methods=["GET"])
def index():
    return render_template("index.html")

@app.route('/new_entry', methods=["POST"])
def new_entry():
    return render_template("index.html")