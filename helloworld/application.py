#!flask/bin/python
import json
from flask import Flask, Response, request
from helloworld.flaskrun import flaskrun
from flask_cors import CORS # availble get records from dynamodb by conditions 
import boto3 # AWS library for python  
import uuid # generates ID in UUID format
from boto3.dynamodb.conditions import Key # availble get records from dynamodb by conditions 
from boto3.dynamodb.conditions import Attr
import simplejson as json # use decimel values in json


application = Flask(__name__)
CORS(application, resources={r"/*": {"origins": "*"}}) 


@application.route('/', methods=['GET'])
def get():
    return Response(json.dumps({'Output': 'Hello World'}), mimetype='application/json', status=200)

@application.route('/', methods=['POST'])
def post():
    return Response(json.dumps({'Output': 'Hello World'}), mimetype='application/json', status=200)
    
    
    
    


# ADD NEW PROJECT - DynamoDB
@application.route('/addProject', methods=['POST'])
def addProject():
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('projects')
    data = request.data
    data_json = json.loads(data)
    project_id = str(uuid.uuid4())
    data_json['project_id'] = project_id
    table.put_item(Item=data_json)
    
    return Response(json.dumps({'Output': 'Save Succeed'}), mimetype='application/json', status=200)





# GET PROJECTS BY USER ID - DynamoDB
@application.route('/getProjects', methods=['POST'])
def getProjects():
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('projects')

    data = request.data
    data_json = json.loads(data)
    user_id = data_json['user_id']
    print(user_id)
    
    response = table.scan(FilterExpression = Attr('user_id').eq(user_id))
    projects = response['Items']
    print(projects)
    return Response(json.dumps(projects), mimetype='application/json', status=200)  

# curl -i -X POST -H "Content-Type: application/json" -d '{"user_id": "5rtTKC7sE2hRIXdfOca6CQNqFgR2"}' http://localhost:8000/getProjects



# DELETE PROJECT BY PROJECT ID - DynamoDB
@application.route('/deleteProject', methods=['POST'])
def deleteProject():
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('projects')
    
    data = request.data
    data_json = json.loads(data)
    project_id = data_json['project_id']

    response = table.delete_item(
        Key={
            'project_id': project_id,
        }
    )

    return Response(json.dumps({'Output': 'Delete Succeed'}), mimetype='application/json', status=200)
# curl -i -X POST -H "Content-Type: application/json" -d '{"project_id": "b38e5046-33f3-4f0f-a7c8-76fb9427947c"}' http://localhost:8000/deleteProject



# UPLOAD IMAGE TO S3 AND REKOGNITION MODERATION ANALYSIS
@application.route('/uploadImage', methods=['POST'])
def uploadImage():
    s3 = boto3.resource('s3', region_name='us-east-1')
    bucket = 'kickstarter-cloud-project-assets'
    
    image_file = request.files['image']
    image_id = str(uuid.uuid4())
    image_full_name  = "%s.jpg" %  image_id
    s3.Bucket(bucket).upload_fileobj(image_file, image_full_name, ExtraArgs={'ACL': 'public-read', 'ContentType': 'image/jpeg'}) 
    image_url = 'https://kickstarter-cloud-project-assets.s3.amazonaws.com/'+ image_full_name
    
    rekognition = boto3.client("rekognition", region_name = 'us-east-1')
    image_url = 'https://kickstarter-cloud-project-assets.s3.amazonaws.com/'
    response = rekognition.detect_moderation_labels(
    Image={
        'S3Object': {
            'Bucket': bucket,
            'Name': image_full_name,
        }
    }
    )
    
    print(response)
    
    moderationLabels = response['ModerationLabels']
    res = [{"image_url":image_url, "moderationLabels": moderationLabels} ]

    return Response(json.dumps(res), mimetype='application/json', status=200)
# curl -i -X POST -H "Content-Type: application/json" -d '{"project_id": "b38e5046-33f3-4f0f-a7c8-76fb9427947c"}' http://localhost:8000/uploadImage

if __name__ == '__main__':
    flaskrun(application)
