import boto3 
#bedrock-agentcore,  strands-agents

session = boto3.Session(
    aws_access_key_id='YOUR_ACCESS_KEY_ID',
    aws_secret_access_key='YOUR_SECRET_ACCESS_KEY',
    region_name='us-east-1'
)
# create client
s3_client = session.client('s3')
lambda_client = session.client('lambda')
iam=  session.client('iam') # add IAM client for Lambda role management
logs =  session.client('logs') # CloudWatch Logs client for monitoring

bedrock_agent =  session.client('bedrock-agent')



# setting up the lambda function
