import os

import pytest
from src.homepage_lambda import handler

def test_homepagelambda():
    #print("test_homepagelambda; current working directory {}".format(os.getcwd()))
    #os.chdir("../src")
    result = handler(None, None)
    print(result)
    print(result["body"])
    assert result["body"]

print(test_homepagelambda())