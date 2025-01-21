

# AWS Lambda Blog Generator with API Gateway and S3 Integration

This project integrates an AWS Lambda function with API Gateway to create an HTTP endpoint for generating blogs using AWS Bedrock and saving them to an S3 bucket. The API Gateway serves as the entry point, forwarding requests to the Lambda function. The Lambda function processes the request, generates blog content, and saves it in an S3 bucket for storage.

### **Components:**

- **API Gateway Endpoint**: Exposes the Lambda function as an HTTP endpoint.
- **Lambda Function**: Handles the request, generates content, and writes it to S3.
- **S3 Bucket**: Stores the generated blog content.

---

### **Flow Overview**

1. **Client** (User/API consumer) sends an HTTP request with a `topic` to the API Gateway endpoint.
2. **API Gateway**:

   - Receives the request.
   - Forwards the payload to the Lambda function using Lambda Proxy Integration.
3. **Lambda Function**:

   - Parses the request.
   - Calls AWS Bedrock to generate a blog based on the topic.
   - Writes the generated blog to the specified S3 bucket.
   - Logs API call durations and outputs for monitoring.
   - Returns a success message to the API Gateway.
4. **API Gateway**:

   - Sends the response from Lambda back to the client.
5. **S3**:

   - Stores the blog as a text file in a designated folder (`blog_output/`).

---

### **API Gateway Integration**

1. In the **API Gateway Console**, create an HTTP API or REST API.
2. Configure a **POST method** that triggers the Lambda function.
3. Enable **Lambda Proxy Integration** to pass the request directly to the Lambda function.
4. Deploy the API to a stage (e.g., `dev` or `prod`).

---

### **Creating the Boto3 Layer for Lambda**

To use **Boto3** in Lambda, you will need to create a custom Lambda layer that contains the **Boto3** library.

#### **Step 1: Create the Boto3 Layer Directory**

```bash
mkdir boto3-layer
cd boto3-layer
mkdir python
cd python
```

#### **Step 2: Install Boto3 into the 'python' directory**

Install **Boto3** into the `python` directory using `pip`.

```bash
pip install boto3 -t .
```

#### **Step 3: Zip the content into a layer**

Zip the content of the `python` directory into a layer file.

```bash
cd ..
zip -r boto3-layer.zip python/
```

#### **Step 4: Create a Lambda Layer in AWS Console**

1. **Navigate** to **AWS Lambda Console** > **Layers** > **Create Layer**.
2. **Name** the layer (e.g., `Boto3-Layer`).
3. **Upload** the `boto3-layer.zip` file.
4. **Select** Python 3.x as the compatible runtime.
5. **Click** 'Create'.

---

### **IAM Permissions for Lambda Role**

Ensure the **IAM role** associated with the Lambda function has the necessary permissions to access **AWS Bedrock** and **S3**.

#### **1. Add Lambda Permissions to Role**

1. Go to the **IAM** console.
2. Search for and select the Lambda execution role (e.g., `awsappbedrock-role-0tedpw3a`).
3. Under the **Permissions** tab, click **Add permissions** → **Attach policies** or **Add inline policy**.
4. Attach the required policies.

---

### **Required IAM Policies**

#### **Bedrock Model Invoke Policy:**

```json
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
```

#### **S3 Access Policy:**

```json
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
```

---

### **API Request Example**

Below is an example of how the API request should look when calling the endpoint:

```json
{
    "body": "{"topic": "The future of AI in healthcare"}"
}
```

The API Gateway will forward this request to Lambda, where the **topic** will be extracted and passed to AWS Bedrock for blog generation.

---

### **S3 Storage Example**

The generated blog content will be stored in the **S3 bucket** `awsbedrockblogoutputs` under the path `blog_output/`.

Example of the generated file structure:

```
awsbedrockblogoutputs/
  ├── blog_output/
  │   └── 062138.txt
```

---

### **Testing the Lambda Function**

1. **Invoke the Lambda function manually** from the **Lambda Console** or through the **API Gateway**.
2. Use the **AWS CLI** to invoke the function:

```bash
aws lambda invoke --function-name <your-lambda-function-name> --payload file://test-event.json output.json
```

---

### **Conclusion**

This project demonstrates how to integrate AWS **Lambda**, **API Gateway**, **S3**, and **AWS Bedrock** to build a scalable blog generation service. The Lambda function processes incoming HTTP requests, uses Bedrock to generate content, and stores the result in an S3 bucket. By using an API Gateway, the service is exposed as an HTTP endpoint that can be accessed by clients or user


![1737442574675](image/Readme/1737442574675.png)

![1737442226477](image/Readme/1737442226477.png)


**Api request:**

![1737443030977](image/Readme/1737443030977.png)

S3 Storage :
![1737443137058](image/Readme/1737443137058.png)
