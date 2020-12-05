import csv
import boto3
import json

#open credentials for AWS service
with open('new_user_credentials.csv','r') as input:
    next(input)
    reader = csv.reader(input)
    for line in reader:
        access_key_id = line[2]
        secret_access_key = line[3]

#initialize S3 and rekognition client
s3_client = boto3.client(
    's3',
    region_name='us-east-1',
    aws_access_key_id=access_key_id,
    aws_secret_access_key=secret_access_key,
)

reko_client=boto3.client(
    'rekognition',
    region_name='us-east-1',
    aws_access_key_id=access_key_id,
    aws_secret_access_key=secret_access_key,
)

collectionId='facecollection321' #enter collection name here
bucket = 'facebucket321' #enter S3 bucket name here

#if any, delete existing collection
list_response=reko_client.list_collections(MaxResults=2)
if collectionId in list_response['CollectionIds']:
    reko_client.delete_collection(CollectionId=collectionId)

reko_client.create_collection(CollectionId=collectionId)

all_objects = s3_client.list_objects(Bucket=bucket)

#for each object in S3, store in the collection
for content in all_objects['Contents']:
    image = content['Key']
    imageName = content['Key'].split('.')[0]
    index_response=reko_client.index_faces(
        CollectionId=collectionId,
        Image={'S3Object':{'Bucket':bucket,'Name':image}},
        ExternalImageId=imageName,
        MaxFaces=1,
        QualityFilter="AUTO",
        DetectionAttributes=['ALL']
    )
    print('FaceId: ',index_response['FaceRecords'][0]['Face']['ExternalImageId'])