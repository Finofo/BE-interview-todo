from datetime import datetime, UTC


def datetime_now() -> datetime:
    return datetime.now(UTC)
