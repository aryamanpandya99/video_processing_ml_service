"""
This module implements the lambda function triggered by successful image uploads
in s3
"""

import json


def handler(event, context):
    """
    Lambda trigger (s3 upload) handler
    """
    print("Received event: " + json.dumps(event, indent=2))
    print(f"Context: {context}")
    try:
        for record in event["Records"]:
            container = record["s3"]
            bucket = container["bucket"]["name"]
            key = container["object"]["key"]

            print(f"Bucket: {bucket}")
            print(f"Key: {key}")
    except Exception as exc:
        print(f"An error occurred: {exc}")
        return {"statusCode": 500, "body": json.dumps("An error occurred")}

    return {"statusCode": 200, "body": json.dumps("Success")}
