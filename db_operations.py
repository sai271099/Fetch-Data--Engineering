import json
import psycopg2
from masking import mask_value, base64_encode

def create_table(cursor):
    with open('create_table.sql', 'r') as file:
        create_table_query = file.read()
    cursor.execute(create_table_query)

def insert_messages(messages, mask_value):
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()

    # Create table if not exists
    create_table(cursor)
    conn.commit()

    insert_query = """
    INSERT INTO user_logins (user_id, device_type, masked_ip, masked_device_id, locale, app_version, create_date)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    required_keys = {'user_id', 'device_type', 'ip', 'device_id', 'locale', 'app_version'}

    valid_messages_count = 0

    for message in messages:
        try:
            body = json.loads(message["Body"])
            
            # Decode base64 encoded fields if needed
            if "encoded_field" in body:
                body["encoded_field"] = base64_encode(body["encoded_field"], action="decode")
            
            # Validate required keys
            if not required_keys.issubset(body.keys()):
                missing_keys = required_keys - body.keys()
                print(f"Message is missing keys: {missing_keys} - Skipping this message: {message['Body']}")
                continue

            data = {
                'user_id': body['user_id'],
                'device_type': body['device_type'],
                'ip': body['ip'],
                'device_id': body['device_id'],
                'locale': body['locale'],
                'app_version': body['app_version'],
                'create_date': '2024-06-09'  # Use the current date or a relevant date
            }

            # Mask the PII fields
            data['masked_ip'] = mask_value(data['ip'])
            data['masked_device_id'] = mask_value(data['device_id'])

            # Insert data into table
            cursor.execute(insert_query, (
                data['user_id'], data['device_type'], data['masked_ip'], data['masked_device_id'], data['locale'], data['app_version'], data['create_date']
            ))

            valid_messages_count += 1
        
        except json.JSONDecodeError as e:
            print(f"JSONDecodeError: {e} in message: {message['Body']} - Skipping this message")
        except Exception as e:
            print(f"Error processing message: {e}")

    conn.commit()
    cursor.close()
    conn.close()

    print(f"{valid_messages_count} valid messages processed and inserted successfully")
