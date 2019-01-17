import os
from PIL import Image
import sys
import json
import boto3
import botocore
from flask import render_template,request, redirect, url_for,  send_from_directory

def emptyFolder(folder):
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)

def detect_expression(bucket,key,max_labels,min_confidence=70, region="us-east-1"):
    rekognition = boto3.client("rekognition", region)
    response = rekognition.detect_faces(Image={"S3Object": { "Bucket":bucket, "Name":key}}, MaxLabels=max_labels, MinConfidence=min_confidence,)
    return response['Labels'] 

def detect_celebrity(bucket, key, region="us-east-1"):
    rekognition = boto3.client("rekognition", region)
    response = rekognition.recognize_celebrities(Image={"S3Object": { "Bucket": bucket, "Name":key}}) 
    celebrityNames = []
    for celebrity in response['CelebrityFaces']:
        print ('Name: ' + celebrity['Name'])
        celebrityNames.append(celebrity['Name'])
        print ('Id: ' + celebrity['Id'])
        print ('Position:')
        print ('   Left: ' + '{:.2f}'.format(celebrity['Face']['BoundingBox']['Height']))
        print ('   Top: ' + '{:.2f}'.format(celebrity['Face']['BoundingBox']['Top']))
        print ('Info')
        for url in celebrity['Urls']:
            print ('   ' + url)
    return celebrityNames  

def get_celebrity_info(celebrityId, region="us-east-1"):
    client = boto3.client("rekognition", region)
    response = client.get_celebrity_info(Id=celebrityId)
    print (response['Name'])  
    print ('Further information (if available):')
    for url in response['Urls']:
        print (url) 
    

def getAllKeysInBucket(bucket):
    s3 = boto3.resource("s3")	
    bucket = s3.Bucket(bucket)
    keys = []
    for obj in bucket.objects.all():
    	keys.append(obj.key)
    return keys  
