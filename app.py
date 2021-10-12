from flask import Flask
# create a new Flask instance called app
# Variables with underscores before and after them are called magic methods in Python
app = Flask(__name__)

# ________________________________________________________________________________________________________________________________________________________________________________________
# Create first route. define the starting point, also known as the root
# Whenever you make a route in Flask, you put the code you want in that specific route below @app.route()
@app.route('/')
def hello_world():
    return 'Hello world'
