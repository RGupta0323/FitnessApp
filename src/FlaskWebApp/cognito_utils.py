# this python file contains a list of functions to be used for signing in, singing out and for a user to register using boto 3 & congito

def sign_up_user(client, ClientID, username, password):
    try:
        response = client.sign_up(ClientId=ClientID, Username=username, Password=password)
        return response

    except Exception as ex:
        print("Error has occured in sign_up_user functions in cognito_utils.py.")
        print("Exception: {} ".format(ex))


def list_users(client, UserPoolId):
    try:
        response = client.list_users(UserPoolId=UserPoolId)
        return response

    except Exception as ex:
        print("Error has occured in list_users() function in cognito_utils.py")
        print("Exception: {}".format(ex))

def create_user(client, UserPoolId, email):
    try:
        response = client.admin_create_user(
            UserPoolId=UserPoolId,
            Username=email,
            UserAttributes=[
                {"Name": "email", "Value": str(email)}
            ]
        )

        print(response)

        return response

    except Exception as ex:
        print("Error has occured when trying to create user in create_user() function in cognito_utils.py")
        print("Error: {}".format(ex))