import os
from src.lambda_utils import get_contents_s3_obj
import pytest

def test_lambda_utils():
    bucket_name = "fitness-app-dev-stack-fitnessappstaticwebfiles659-1c9bv2im68wv0"
    response = get_contents_s3_obj(bucket_name, "register.html")
    print(response)
    assert type(response) == bytes
    assert response != "" and response!=" "