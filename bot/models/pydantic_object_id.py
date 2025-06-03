from bson import ObjectId


class PyObjectId(ObjectId):
    """Pydantic wrapper so ObjectId serialises to str in JSON."""

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if isinstance(v, ObjectId):
            return v
        try:
            return ObjectId(str(v))
        except Exception as exc:
            raise ValueError("Not a valid ObjectId") from exc
