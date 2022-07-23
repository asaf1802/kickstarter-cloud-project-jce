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





# GET PROJECTS TABLE - DynamoDB
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

if __name__ == '__main__':
    flaskrun(application)
