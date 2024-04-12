from flask import Flask, Response, redirect, request, render_template

import json

from .aws_login import AWSLogin
from dotenv import load_dotenv
from cognitojwt import jwt_sync

app: Flask = Flask(__name__)
app.debug = True

@app.route("/v1/login", methods = ["POST"])
def post_app_login():
  data = request.json
  login = AWSLogin(data["username"], data["password"])
  login.do_login()
  
  return Response(status = 200)

@app.route("/v1/login/verify", methods = ["POST"])
def post_app_login_verify():
  pass
  return Response(status = 200)
