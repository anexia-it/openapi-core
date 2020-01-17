"""OpenAPI core validation response shortcuts module"""
from openapi_core.validation.response.validators import ResponseValidator


def validate_response(validator, request, response):
    result = validator.validate(request, response)
    result.raise_for_errors()
    return result


def spec_validate_data(
        spec, request, response,
        request_factory=None,
        response_factory=None):
    if request_factory is not None:
        request = request_factory(request)
    if response_factory is not None:
        response = response_factory(response)

    validator = ResponseValidator(spec)
    result = validate_response(validator, request, response)

    return result.data
