from flask import request, Flask, jsonify
import json
from flask_sqlalchemy import SQLAlchemy
from APP.view import collection, block
from APP.view.auth import bp_auth
from APP.view.block import bp_block
from APP.view.collection import bp_collection
from APP.view.database import init_db

app = Flask(__name__)

app.register_blueprint(bp_auth)
app.register_blueprint(bp_block)
app.register_blueprint(bp_collection)
init_db()
app.run(debug=True)
