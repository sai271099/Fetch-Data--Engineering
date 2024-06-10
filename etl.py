from masking import mask_value
from db_operations import insert_messages
from sqs_operations import fetch_messages_from_sqs
import boto3

def main():
    sqs = boto3.client('sqs', region_name='us-east-1', endpoint_url='http://localhost:4566')
    queue_url = 'http://localhost:4566/000000000000/login-queue'

    all_messages = []
    total_message_count = 0

    while True:
        messages = fetch_messages_from_sqs(sqs, queue_url)
        if not messages:
            break
        all_messages.extend(messages)
        total_message_count += len(messages)

    print(f"Total messages fetched: {total_message_count}")

    if all_messages:
        insert_messages(all_messages, mask_value)
    else:
        print("No messages to process")

if __name__ == "__main__":
    main()
