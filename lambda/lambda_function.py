import json

def lambda_handler(event, context):
    # Log the event to CloudWatch
    print("Received event: " + json.dumps(event, indent=2))
    
    # Process the event
    for record in event['Records']:
        s3 = record['s3']
        bucket = s3['bucket']['name']
        key = s3['object']['key']
        
        print(f"Bucket: {bucket}")
        print(f"Key: {key}")
        

    return {
        'statusCode': 200,
        'body': json.dumps('Success')
    }

