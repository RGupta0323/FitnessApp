# this is the lambda that gets triggered when the register form gets submitted
def handler(event, context):
    return {"statuscode": 200, "body":event}