import boto3
import botocore.config 
import json
import time
from datetime import datetime

def blog_generation_using_bedrock(topic):
      prompt ="""
            Generate a 200 words blog on the topic {topic}.

            """  
      body={
        "prompt":prompt,
        "max_gen_len":512,
        "temperature":0.5,
        "top_p":0.9
      } 
      # Initialize a boto3 client for the service
      try:
            bedrock =boto3.client(service_name="bedrock-runtime",region_name="us-east-1",
                                        config=botocore.config.Config(read_timeout=15000,connect_timeout=15,retries={'max_attempts':3}))
            response=bedrock.invoke_model(body=json.dumps(body),modelId="meta.llama3-70b-instruct-v1:0")
            response = json.loads(response.get('body').read())
            content = response['generation']
            print(content)
            return content
      except botocore.exceptions.NoCredentialsError:
            print("No AWS credentials found.")
            return ""
      
def write_to_s3(content, s3_key, s3_bucket):
      s3 = boto3.client('s3')
      try:
        s3.put_object(Bucket=s3_bucket, Key=s3_key, Body=content)
        print(f"Blog content has been written to S3: {s3_bucket}/{s3_key}")
      except Exception as e:
            print(f"Error writing to S3: {e}")

def lambda_handler(event, context):
   event = json.loads(event['body'])
   topic = event.get('topic')
   start_time = time.time()
   blog_content = blog_generation_using_bedrock(topic)
   print(f"Bedrock API call duration: {time.time() - start_time} seconds")
   
   if blog_content:
        current_time = datetime.now().strftime("%H%M%S")
        s3_key = f"blog_output/{current_time}.txt"
        s3_bucket = 'awsbedrockblogoutputs'
        start_time = time.time()
        write_to_s3(blog_content, s3_key, s3_bucket)
        print(f"S3 write operation duration: {time.time() - start_time} seconds")
   else :
        print("No blog generated")

   return {
            'statusCode': 200,
            'body': json.dumps('Blog generation has completed successfully')
        }


      