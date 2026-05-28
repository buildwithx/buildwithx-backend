from typing import Any
from bson import ObjectId

from pydantic_core import core_schema
from pydantic_core.core_schema import PlainValidatorFunctionSchema


class PyObjectId(str):
    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        _source_type,
        _handler,
    ) -> PlainValidatorFunctionSchema:
        return core_schema.no_info_plain_validator_function(
            cls.validate,
            serialization=core_schema.to_string_ser_schema(),
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls,
        _core_schema,
        handler,
    ) -> Any:
        return handler(core_schema.str_schema())

    @classmethod
    def validate(cls, value) -> str:
        if isinstance(value, ObjectId):
            return str(value)

        if isinstance(value, str):
            if not ObjectId.is_valid(value):
                raise ValueError("Invalid ObjectId")

            return value

        raise TypeError("ObjectId required")
