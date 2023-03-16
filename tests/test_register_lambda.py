import boto3, json
from src import register_lambda
def test_register_lambda():
    session = boto3.Session()
    client = session.client("lambda", region_name="us-east-1")
    client.invoke(
        FunctionName="FitnessApp_RegisterLambda",
        Payload=json.dumps({"fname":"test_name", "lname":"test_lname", "email":"someone@example.com", "password":"asdfjkl;"})
    )

def test_create_new_user():
    event = {"fname":"test_name", "lname":"test_lname", "email":"someone@example.com", "password":"asdfjkl;"}
    assert register_lambda.create_new_user(event) != None

def test_validate_new_user():
    event = {"fname":"test_name", "lname":"test_lname", "email":"someone@example.com", "password":"asdfjkl;"}
    response = register_lambda.validate_new_user(event["email"])
    assert response == True

#print(test_validate_new_user())