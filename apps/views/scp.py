from flask import Blueprint

scp = Blueprint("scp", __name__)


@scp.route("/")
def scp_index():
    return "Hahahaha"
