from enum import StrEnum


class ResponseEnum(StrEnum):
    CREATE = "create success"
    UPDATE = "update success"
    DELETE = "delete success"
    UPLOAD = "upload success"
