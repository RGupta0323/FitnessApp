import os
from src.lambda_utils import get_contents_s3_obj, get_all_items_from_dynamodb_table
import pytest

def test_lambda_utils():
    bucket_name = "fitness-app-dev-stack-fitnessappstaticwebfiles659-1c9bv2im68wv0"
    response = get_contents_s3_obj(bucket_name, "register.html")
    print(response)
    assert type(response) == bytes
    assert response != "" and response!=" "

def test_get_all_contents_from_dynamodb_table():
    table_name = "fitness-app-dev-stack-FitnessAppUserData5D9F0F31-YQPUN4XKQ00I"
    data = get_all_items_from_dynamodb_table(table_name)
    assert type(data) == list


#print(test_get_all_contents_from_dynamodb_table())