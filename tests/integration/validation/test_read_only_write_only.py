import json

import pytest
from openapi_spec_validator import openapi_v30_spec_validator

from openapi_core.shortcuts import create_spec
from openapi_core.testing import MockRequest
from openapi_core.testing import MockResponse
from openapi_core.unmarshalling.schemas.exceptions import InvalidSchemaValue
from openapi_core.validation.request.validators import RequestValidator
from openapi_core.validation.response.validators import ResponseValidator


@pytest.fixture
def response_validator(spec):
    return ResponseValidator(spec)


@pytest.fixture
def request_validator(spec):
    return RequestValidator(spec)


@pytest.fixture(scope="class")
def spec(factory):
    spec_dict = factory.spec_from_file("data/v3.0/read_only_write_only.yaml")
    return create_spec(spec_dict, spec_validator=openapi_v30_spec_validator)


class TestReadOnly:
    def test_write_a_read_only_property(self, request_validator):
        data = json.dumps(
            {
                "id": 10,
                "name": "Pedro",
            }
        )

        request = MockRequest(
            host_url="", method="POST", path="/users", data=data
        )

        result = request_validator.validate(request)

        assert type(result.errors[0]) == InvalidSchemaValue
        assert result.body is None

    def test_read_only_property_response(self, response_validator):
        data = json.dumps(
            {
                "id": 10,
                "name": "Pedro",
            }
        )

        request = MockRequest(host_url="", method="POST", path="/users")

        response = MockResponse(data)

        result = response_validator.validate(request, response)

        assert not result.errors
        assert result.data == {
            "id": 10,
            "name": "Pedro",
        }


class TestWriteOnly:
    def test_write_only_property(self, request_validator):
        data = json.dumps(
            {
                "name": "Pedro",
                "hidden": False,
            }
        )

        request = MockRequest(
            host_url="", method="POST", path="/users", data=data
        )

        result = request_validator.validate(request)

        assert not result.errors
        assert result.body == {
            "name": "Pedro",
            "hidden": False,
        }

    def test_read_a_write_only_property(self, response_validator):
        data = json.dumps(
            {
                "id": 10,
                "name": "Pedro",
                "hidden": True,
            }
        )

        request = MockRequest(host_url="", method="POST", path="/users")
        response = MockResponse(data)

        result = response_validator.validate(request, response)

        assert type(result.errors[0]) == InvalidSchemaValue
        assert result.data is None
