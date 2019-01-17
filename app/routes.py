import os
from PIL import Image
import sys
import json
import boto3
import botocore
from flask import render_template,request, redirect, url_for,  send_from_directory
from werkzeug.utils import secure_filename
from app import app
from util import * 

BUCKET = "swjkuploadimages"
ALLOWED_EXTENTIONS = set(['png','jpg'])

#HOME PAGE 
@app.route("/")
@app.route("/index")
def index():
    imageCollection = []
    emptyFolder(app.config["LOCALSTORE"]) 
    keys = getAllKeysInBucket(BUCKET) 
    s3 = boto3.resource("s3")
    for key in keys:
        detect_celebrity(BUCKET,key)
        try:
            s3.Bucket(BUCKET).download_file(key,os.path.join(app.config["LOCALSTORE"],key))	
            imageCollection.append(key)
        except botocore.exceptions.ClientError as e:
            dprint("The object does not exist")
    return render_template("index.html", title="HomePage", imageCollection=imageCollection)

#UPLOADING THUMBNAIL IMAGE TO S3
@app.route("/uploader", methods=['GET', 'POST'])
def uploader():    
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        localstore = os.path.join(app.config['LOCALSTORE'],filename)
        file.save(localstore)
        img = Image.open(localstore)
        img.thumbnail((200,200), Image.ANTIALIAS)
        img.save(localstore)
        s3 = boto3.client("s3")
        s3.upload_file(localstore,BUCKET,filename)
        os.remove(localstore)
        return render_template("submitted.html")

    return "file not succesfully uploaded"

#UPLOAD PAGE
@app.route("/upload")
def upload():
    return render_template("upload.html")

#SEND IMAGE FROM LOCAL STORAGE TO HTML
@app.route("/retrieve/<image>")
def send_image(image):
    return send_from_directory(app.config['LOCALSTORE'],image)  

#RETRIEVE CELEBRITY INFO WHEN ENLARGED
@app.route("/getcelebrity/<jsdata>")
def getCelebrityInfo(jsdata):
    celebrityNames = detect_celebrity(BUCKET, jsdata)
    data = [] 
    if celebrityNames:
        for celebrity in celebrityNames:
            data.append({ "name": celebrity})
    else:
            data =[{ "name": "No Name"}]
    return json.dumps(data)

#ERROR HANDLE IF SERVER CRASHES - CLEARING S3
@app.errorhandler(500)
def serverError(error):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(BUCKET)
    bucket.objects.all().delete()
    return redirect(url_for('index'))
