#!flask/bin/python
import json
from flask import Flask, Response, request
from helloworld.flaskrun import flaskrun
from flask_cors import CORS
import boto3
import uuid



application = Flask(__name__)
CORS(application, resources={r"/*": {"origins": "*"}}) 


@application.route('/', methods=['GET'])
def get():
    return Response(json.dumps({'Output': 'Hello World'}), mimetype='application/json', status=200)

@application.route('/', methods=['POST'])
def post():
    return Response(json.dumps({'Output': 'Hello World'}), mimetype='application/json', status=200)
    
    
    
    


# Add Project - DynamoDB
@application.route('/addProject', methods=['POST'])
def addProject():
    data = request.data
    data_json = json.loads(data)
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('projects')
    project_id = str(uuid.uuid4())
    data_json['project_id'] = project_id
    table.put_item(Item=data_json)
    
    return Response(json.dumps({'Output': 'Save Succeed'}), mimetype='application/json', status=200)




if __name__ == '__main__':
    flaskrun(application)
