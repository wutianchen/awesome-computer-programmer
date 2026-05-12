# Calculate AWS Signature V4

Here is the relevant documentation: https://docs.aws.amazon.com/AmazonS3/latest/API/sig-v4-header-based-auth.html
But you do not have to do it yourself, if you are using aws SDK. for example, you can use aws_requests_auth package to sign aws request

```python
import requests
from aws_requests_auth.aws_auth import AWSRequestsAuth

auth = AWSRequestsAuth(aws_access_key='YOURKEY',
                       aws_secret_access_key='YOURSECRET',
                       aws_host='restapiid.execute-api.us-east-1.amazonaws.com',
                       aws_region='us-east-1',
                       aws_service='execute-api')

headers = {'params': 'ABC'}
response = requests.get('https://restapiid.execute-api.us-east-1.amazonaws.com/stage/resource_path',
                        auth=auth, headers=headers)
```
