# PYthon file to contain helper functions for lambda functions
import boto3

def get_contents_s3_obj(bucket_name, object_key):
    contents = None
    try:
        s3 = boto3.client("s3")
        contents = s3.get_object(Bucket=bucket_name, Key=object_key)["Body"].read()

    except Exception as ex:
        raise ex

    return contents

def get_all_items_from_dynamodb_table(table_name):
    try:
        client = boto3.resource("dynamodb", region_name="us-east-1")
        table = client.Table(table_name)
        response = table.scan()
        return response["Items"]

    except Exception as ex:
        print("[lambda_utils.py get_all_items_from_dynamodb_table()] Exception occured: {}".format(ex))
        return ex