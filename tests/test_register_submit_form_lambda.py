# Testing register_submit_Form_lambda
from src.register_submit_form_lambda import handler
def test_handler():
    assert handler({"email": "someone@example.com"}, None)

test_handler()