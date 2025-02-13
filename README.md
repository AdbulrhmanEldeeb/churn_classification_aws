# AWS Lambda & SageMaker Inference API

## Project Overview
This project deploys an AWS Lambda function that invokes a SageMaker endpoint to make predictions on customer data. The function receives input via an API Gateway, processes the data, and returns a prediction indicating whether a customer is likely to exit.

## Features
- **AWS Lambda Function**: Handles HTTP POST requests and forwards data to the SageMaker model.
- **SageMaker Endpoint**: XGBoost model deployed to predict customer churn.
- **API Gateway**: Provides a REST API endpoint for inference.
- **Security Enhancements**: Validates input length and format, handles exceptions.

## API Usage
### **Endpoint URL**
```plaintext
https://gng8qcrjc6.execute-api.us-east-1.amazonaws.com/prod
```

### **Request Format**
Send a `POST` request with the following JSON payload:
```json
{
    "data": [670, 1, 38, 7, 0.0, 2, 1, 1, 77864.41, 1, 0, 0]
}
```

### **Response Format**
The response contains the predicted class label:
```json
{
    "result": "Will Exit"
}
```

### **cURL Example (Linux/macOS)**
```sh
curl -X POST "https://gng8qcrjc6.execute-api.us-east-1.amazonaws.com/prod" \
     -H "Content-Type: application/json" \
     -d '{"data":[670,1,38,7,0.0,2,1,1,77864.41,1,0,0]}'
```

### **PowerShell Example (Windows)**
```powershell
$headers = @{"Content-Type" = "application/json"}
$body = @{ "data" = @(670,1,38,7,0.0,2,1,1,77864.41,1,0,0) } | ConvertTo-Json -Depth 10
$response = Invoke-RestMethod -Uri "https://gng8qcrjc6.execute-api.us-east-1.amazonaws.com/prod" `
                              -Method Post `
                              -Headers $headers `
                              -Body $body
$response
```

## AWS Lambda Function
### **Code Implementation**
```python
import boto3
import json
from typing import Dict, Any
import os

# Initialize SageMaker client
runtime = boto3.client("sagemaker-runtime")
ENDPOINT_NAME = os.environ.get("ENDPOINT_NAME", "sagemaker-xgboost-2025-02-11-12-56-22-445")

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    try:
        inputs = event.get("data")
        if not isinstance(inputs, list) or len(inputs) != 12:
            return {"error": "Invalid input. Expected a list of 12 numerical values."}

        serialized_input = ",".join(map(str, inputs))
        response = runtime.invoke_endpoint(
            EndpointName=ENDPOINT_NAME,
            ContentType="text/csv",
            Body=serialized_input,
        )
        prediction = float(response["Body"].read().decode())
        class_label = "Will Exit" if round(prediction) == 1 else "Will Not Exit"
        return {"result": class_label}
    except Exception as e:
        return {"error": str(e)}
```


## Deployment Steps
1. **Create the SageMaker Endpoint**
   - Train and deploy an XGBoost model using AWS SageMaker, for this follow the notebook provided in notebooks dir
2. **Deploy AWS Lambda Function**
   - Upload the Python script to AWS Lambda.
   - Set the `ENDPOINT_NAME` environment variable.
3. **Configure API Gateway**
   - Create a new API Gateway with a POST method.
   - Connect it to the Lambda function.
4. **Test API Using cURL or Postman**
   - Send test requests to ensure predictions are accurate.

## Security Considerations
- Validate the input to ensure it contains exactly 12 numerical elements.
- Use environment variables instead of hardcoding sensitive values.
- Implement IAM policies with least privilege access to SageMaker.
- Implement logging and monitoring with AWS CloudWatch.

## Future Improvements
- Implement authentication using AWS IAM roles or API Gateway keys.
- Optimize response latency by fine-tuning the SageMaker model.
- Deploy a frontend interface for user-friendly interactions.

---
**Author**: Abdulrhman Eldeeb  
**Last Updated**: February 2025

