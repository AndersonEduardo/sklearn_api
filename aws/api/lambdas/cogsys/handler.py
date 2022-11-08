import json
import boto3
import os
import pickle

# import numpy  # nao funciona importar na lambda
# import pandas # nao funciona importar na lambda
import sklearn

s3 = boto3.resource("s3")
BUCKET_NAME = "api-linhas-de-cuidado"


def lambda_handler(event, context):

    print('#######################')
    print('event:\n', event)
    print('#######################')

    # event_body = event["body"]

    review_text = event.get('review_text')

    if review_text is None:

        return {"statusCode": 400, "body": "body cannot be empty"}


    # Load in the data from the event body
    # req_body = json.loads(event_body)

    # Check to see if review_text is in the body
    # if "review_text" in req_body:

    #     review_text = req_body["review_text"]

    # else:

    #     return {"statusCode": 400, "body": "review_text must have a value"}

    # Download the model file from s3
    # FIXME:: CACHE MUST BE INVALIDATED IF A NEW MODEL IS UPLOADED!
    local_model_path = "/tmp/review_model.pkl"
    s3_file_name = "review_model.pkl"

    if not os.path.exists(local_model_path):

        s3.Bucket(BUCKET_NAME).download_file(s3_file_name, local_model_path)

    # Load model to memory
    with open(local_model_path, "rb") as f:

        model = pickle.load(f)

    # make a prediction
    pred = model.predict([review_text])

    return {"statusCode": 200, "body": json.dumps(str(pred))}