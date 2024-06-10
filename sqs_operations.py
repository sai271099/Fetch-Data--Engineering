
import boto3

def fetch_messages_from_sqs(sqs, queue_url):
    response = sqs.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=10,  
        WaitTimeSeconds=5
    )
    return response.get('Messages', [])
