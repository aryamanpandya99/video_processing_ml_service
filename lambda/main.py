import json


def handler(event, context):
    # Log the event to CloudWatch
    print("Received event: " + json.dumps(event, indent=2))

    try:
        for record in event["Records"]:
            s3 = record["s3"]
            bucket = s3["bucket"]["name"]
            key = s3["object"]["key"]

            print(f"Bucket: {bucket}")
            print(f"Key: {key}")
    except Exception as e:
        print(f"An error occurred: {e}")
        return {"statusCode": 500, "body": json.dumps("An error occurred")}

    return {"statusCode": 200, "body": json.dumps("Success")}
