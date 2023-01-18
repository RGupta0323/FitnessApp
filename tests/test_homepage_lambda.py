import os
import pytest
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))
from src.homepage_lambda import handler


def test_homepagelambda():
    result = handler(None, None)
    print(result["body"])
    assert type(result["body"]) == str
    assert result["body"]


