from rest_framework.exceptions import ValidationError, APIException
from rest_framework.views import exception_handler


class ValidationException(APIException):
    pass

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is None:
        return response

    if isinstance(exc, ValidationError):
        errors = response.data

        def get_first_error(data, field_name=None):
            if isinstance(data, dict):
                for key, value in data.items():
                    result = get_first_error(value, key)
                    if result:
                        return result

            elif isinstance(data, list):
                for value in data:
                    result = get_first_error(value, field_name)
                    if result:
                        return result

            else:
                message = str(data)

                if field_name:
                    return f"{field_name.capitalize()} : {message}"

                return message

            return None

        message = get_first_error(errors)

        if message:
            response.data = {"detail": message}

    return response