
from pydantic import BaseModel


class BaseDTO(BaseModel):

    @classmethod
    def from_model(cls, data):
        """Create an instance of the DTO from a dict or model-like object."""
        if data is None:
            return None

        if isinstance(data, dict):
            return cls(**data)

        field_names = getattr(cls, "model_fields", None)
        if field_names is not None:
            payload = {field: getattr(data, field) for field in field_names}
            return cls(**payload)

        payload = {field: getattr(data, field) for field in cls.__fields__}
        return cls(**payload)