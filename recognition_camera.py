import boto3
import time
import csv
from picamera import PiCamera

directory = '/home/pi/4OI6_project/image' #directory to store photos taken 

#start the pi camera
P = PiCamera()
P.resolution = (800,600)
P.start_preview()

collectionId = '' #enter collection name here

#open credentials for AWS service
with open('new_user_credentials.csv','r') as input:
    next(input)
    reader = csv.reader(input)
    for line in reader:
        access_key_id = line[2]
        secret_access_key = line[3]

#initialize the rekognition client
client = boto3.client('rekognition',region_name='us-east-1',aws_access_key_id = access_key_id, aws_secret_access_key = secret_access_key)


while True:
    time.sleep(1)
    
    #store the photos taken in the corresponding directory
    current_time_milli = int(round(time.time() * 1000))
    image = '{}/photo_{}.jpg'.format(directory,current_time_milli)
    P.capture(image)
    print('photo captured: '+image)
    
    #print the response from the AWS rekognition
    with open(image, 'rb') as image:
        try:
            response = client.search_faces_by_image(
                CollectionId=collectionId, 
                Image={'Bytes': image.read()}, 
                MaxFaces=1, 
                FaceMatchThreshold=85, 
                QualityFilter='AUTO'
            )
            if response ['FaceMatches']:
                print('Recognized: ',response['FaceMatches'][0]['Face']['ExternalImageId'],'\nSimilarity: ',response['FaceMatches'][0]['Face']['Confidence'])
            else:
                print('No faces matched')
        except:
            print('No faces detected')
            
        time.sleep(1)



