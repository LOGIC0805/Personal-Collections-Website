from flask import request, Flask, jsonify
from APP.view.auth import bp_auth
from APP.view.block import bp_block
from APP.view.start import bp_start
from APP.view.collection import bp_collection
from APP.view.database import init_db


class CustomFlask(Flask):

    jinja_options = Flask.jinja_options.copy()
    jinja_options.update(dict(
        variable_start_string='%%',  # Default is '{{', I'm changing this because Vue.js uses '{{' / '}}'
        variable_end_string='%%',
    ))
app = CustomFlask(__name__)
app.register_blueprint(bp_auth)
app.register_blueprint(bp_start)
app.register_blueprint(bp_block)
app.register_blueprint(bp_collection)
init_db()
app.run(debug=True)
