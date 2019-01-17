from flask import Flask
import os
app = Flask(__name__)
app.config["LOCALSTORE"] = os.path.join(os.path.dirname(os.path.realpath(__file__)),"vol1") 

from app import routes

