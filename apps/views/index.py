from flask import Blueprint

index = Blueprint("index", __name__)


@index.route("/")
def scp_index():
    return "Index"
