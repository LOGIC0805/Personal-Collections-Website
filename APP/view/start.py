from flask import Flask, render_template, request, jsonify, session, Blueprint
from bson import json_util
import uuid

from APP.view.database import db_session
from APP.view.model import Block, CollectionBlock

bp_start = Blueprint("start", __name__)

@bp_start.route("/", methods=["POST",'GET'])
def hello():
    return render_template('login.html')

@bp_start.route("/login", methods=["POST",'GET'])
def login():
    return render_template('login.html')

@bp_start.route("/register", methods=["POST",'GET'])
def register():
    return render_template('register.html')

@bp_start.route("/forget", methods=["POST",'GET'])
def forget():
    return render_template('forget.html')

@bp_start.route("/personal", methods=["POST",'GET'])
def personal():
    return render_template('personal.html')

@bp_start.route("/square", methods=["POST",'GET'])
def square():
    return render_template('square.html')

@bp_start.route("/add", methods=["POST",'GET'])
def add():
    return render_template('add.html')