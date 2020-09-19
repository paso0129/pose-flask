from flask import (
    Flask,
    render_template,
    request,
    make_response,
    jsonify,
)
from flask_cors import CORS

from pose import Pose, PoseList


app = Flask(__name__)
CORS(app)


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/req", methods=["POST"])
def create_entry():
    req = request.get_json()
    ret = PoseList.parse_obj(req)

    return make_response(jsonify(req), 200)
