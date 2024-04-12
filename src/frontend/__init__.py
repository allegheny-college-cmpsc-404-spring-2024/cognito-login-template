from flask import Flask, Response, redirect, request, render_template

import requests

app: Flask = Flask(__name__)
app.debug = True

@app.route("/", methods = ["GET", "POST"])
def index():
  return render_template("layout.html")

@app.route("/login", methods = ["POST"])
def post_login():
  outcome = requests.post(
    "http://localhost:5000/api/v1/login",
    json = request.form
  )
  return Response(status = outcome.status_code)
