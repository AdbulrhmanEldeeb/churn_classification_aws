import boto3
import json
import logging
from typing import Dict, Any
import os 
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize SageMaker client securely
runtime = boto3.client("sagemaker-runtime")


ENDPOINT_NAME = os.environ.get("ENDPOINT_NAME")
if ENDPOINT_NAME is None:
    raise ValueError("Environment variable 'ENDPOINT_NAME' is not set.")


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    AWS Lambda function to send data to a SageMaker endpoint for inference.

    Args:
        event (dict): The input event containing 'data' key with a list of numerical values.
        context (Any): Lambda context object (not used).

    Returns:
        dict: JSON response with the predicted class label.
    """
    try:
        # Extract and validate input data
        inputs = event.get("data")

        if not isinstance(inputs, list):
            logger.warning("Invalid request: data is not a list")
            return {"error": "Invalid input format. 'data' must be a list of numbers."}

        if len(inputs) != 12:
            logger.warning(f"Invalid input length: expected 12, got {len(inputs)}")
            return {"error": f"Invalid input length. 'data' must contain exactly 12 elements. You provided {len(inputs)}."}

        # Ensure all elements are valid numbers
        if not all(isinstance(i, (int, float)) and not (i is None or i == float("inf") or i == float("-inf")) for i in inputs):
            logger.warning("Invalid request: data contains non-numeric or infinite values")
            return {"error": "Invalid input. 'data' must only contain finite numbers."}

        # Serialize input data
        serialized_input = ",".join(map(str, inputs))

        # Invoke SageMaker endpoint
        response = runtime.invoke_endpoint(
            EndpointName=ENDPOINT_NAME,
            ContentType="text/csv",
            Body=serialized_input,
        )

        # Read and decode the response
        prediction = float(response["Body"].read().decode())

        # Convert prediction to class label
        class_label = "Will Exit" if round(prediction) == 1 else "Will Not Exit"

        return {"result": class_label}

    except Exception as e:
        logger.error(f"Error processing request: {str(e)}", exc_info=True)
        return {"error": "Internal server error. Please try again later."}
