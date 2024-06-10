# ETL Pipeline for Masking PII and Storing in PostgreSQL

## Overview

This project implements an ETL (Extract, Transform, Load) pipeline to read JSON data from an AWS SQS Queue using Localstack, mask sensitive information (PII fields) such as `device_id` and `ip`, and write the transformed data to a PostgreSQL database. Docker is utilized to set up Localstack and PostgreSQL locally, ensuring an isolated and consistent development environment.

## Prerequisites

- Docker and Docker Compose installed
- Python 
- pgAdmin or any PostgreSQL client for database management


## Setup and Execution Steps

### 1. Start Docker Containers

Start Localstack and PostgreSQL containers using Docker Compose:

```sh
docker-compose up -d

### 2. Verify SQS and PostgreSQL Setup

Open a new terminal and use the following command to interact with Localstack:

```sh
awslocal sqs create-queue --queue-name login-queue


### 3. Run the Main ETL Script

Execute the main script to fetch messages from the SQS queue, mask PII, and insert the transformed data into PostgreSQL:

```sh
python etl.py

### 4. Verify Data Insertion in PostgreSQL

#### Using pgAdmin

1. **Open pgAdmin:**
   - Launch pgAdmin and connect to the PostgreSQL server.

2. **Create a Server Connection:**
   - Host: `localhost`
   - Port: `5432`
   - Username: `postgres`
   - Password: `postgres`

3. **Run SQL Query:**
   - Navigate to the `user_logins` table and execute the following query to verify the inserted data:

```sql
SELECT * FROM user_logins;



## Files and Their Roles

- **`create_table.sql`**: SQL script to create the `user_logins` table in PostgreSQL.
- **`docker-compose.yml`**: Docker Compose file to set up Localstack and PostgreSQL.
- **`etl.py`**: Main script to coordinate the ETL process.
- **`masking.py`**: Contains the function to hash, encode, and decode strings.
- **`db_operations.py`**: Contains functions to create the table and insert messages into the database.
- **`sqs_operations.py`**: Contains the function to fetch messages from the SQS queue.
- **`requirements.txt`**: Lists the required Python packages.

