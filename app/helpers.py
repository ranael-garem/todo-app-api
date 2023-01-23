from datetime import datetime, timezone


def utc_datetime():
    """Typically used as the default_factory in a pydantic.
    Field to have a datetime default to the current time at UTC"""
    return datetime.now(timezone.utc)
