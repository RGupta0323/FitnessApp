# Displays home page
def handler(event, context):
    return {
            'statusCode': 200,
            'headers': {
                "Access-Control-Allow-Origin": "*",
            },
            'body': "This text is coming from Lambda!"
    }



