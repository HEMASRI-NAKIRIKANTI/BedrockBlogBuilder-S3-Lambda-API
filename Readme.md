
This project integrates an AWS Lambda function with API Gateway to create an HTTP endpoint for generating blogs using AWS Bedrock and saving them to an S3 bucket. The API Gateway serves as the entry point, forwarding requests to the Lambda function.

- **API Gateway Endpoint**: Exposes the Lambda function as an HTTP endpoint.
- **Lambda Function**: Handles the request, generates content, and writes it to S3.
- **S3 Bucket**: Stores the generated blog content.

### **Flow Overview**

1. **Client** (User/API consumer) sends an HTTP request with a `topic` to the API Gateway endpoint.
2. **API Gateway** :

* Receives the request.
* Forwards the payload to the Lambda function using Lambda Proxy Integration.

  3.**Lambda Function** :

* Parses the request.
* Calls AWS Bedrock to generate a blog based on the topic.
* Writes the generated blog to the specified S3 bucket.
* Logs API call durations and outputs for monitoring.
* Returns a success message to the API Gateway.

 4.**API Gateway** :

* Sends the response from Lambda back to the client

 5.**S3** :

* Stores the blog as a text file in a designated folder (`blog_output/`).

##### Integration with Lambda

```plaintext
### API Gateway Integration
1. In the API Gateway console, create an HTTP API or REST API.
2. Configure a **POST method** that triggers the Lambda function.
3. Enable **Lambda Proxy Integration** to pass the request directly to the Lambda function.
4. Deploy the API to a stage (e.g., `dev` or `prod`).
```


# Step 1: Create the Boto3 Layer Directory

mkdir boto3-layer
cd boto3-layer
mkdir python
cd python

# Step 2: Install Boto3 into the 'python' directory

pip install boto3 -t .

# Step 3: Zip the content into a layer

cd ..
zip -r boto3-layer.zip python/

# Step 4: Create a Lambda Layer in AWS Console

(Manual step: Go to AWS Lambda Console)

Navigate to Lambda -> Layers -> Create Layer

Name it `Boto3-Layer`

Upload the `boto3-layer.zip` file you created

Select Python 3.x as the compatible runtime

Click 'Create'


Ensure the IAM role associated with the Lambda function has the necessary
Add the below policies for the lambda  - AWS Service: lambda

* Go to the **IAM** console.
* Search for and select the role (`awsappbedrock-role-0tedpw3a`).
* Under the **Permissions** tab, click **Add permissions** → **Attach policies** or  **Add inline policy** .
* You can Give whatever name you want

![1737442574675](image/Readme/1737442574675.png)

![1737442226477](image/Readme/1737442226477.png)

**Bedrock model Invoke Policy :**

{
	"Version": "2012-10-17",
	"Statement": [
		{
			"Effect": "Allow",
			"Action": [
				"bedrock:InvokeModel"
			],
			"Resource": "arn:aws:bedrock:us-east-1::foundation-model/meta.llama3-70b-instruct-v1:0"
		}
	]
}

**S3 Policy**

{
	"Version": "2012-10-17",
	"Statement": [
		{
			"Effect": "Allow",
			"Action": "s3:PutObject",
			"Resource": "arn:aws:s3:::awsbedrockblogoutputs/*"
		}
	]
}

**Api request:**

![1737443030977](image/Readme/1737443030977.png)

S3 Storage :
![1737443137058](image/Readme/1737443137058.png)
