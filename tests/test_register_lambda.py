import boto3, json
def register_lambda():
    session = boto3.Session()
    client = session.client("lambda", region_name="us-east-1")
    client.invoke(
        FunctionName="FitnessApp_RegisterLambda",
        Payload=json.dumps({"fname":"test_name", "lname":"test_lname", "email":"someone@example.com", "password":"asdfjkl;"})
    )

print(register_lambda())