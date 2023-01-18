# this is the lambda that gets triggered when the register form gets submitted
def handler(event, context):
    return {"statuscode": 200,  'headers': {
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "text/html"
        }, "body":event}