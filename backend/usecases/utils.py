import datetime

from dateutil.tz import gettz
from django.conf import settings

JST = gettz("Asia/Tokyo")
UTC = gettz("UTC")


def convert_datetime_timezone(data: dict) -> dict:
    for key, value in data.items():
        if isinstance(value, datetime.datetime):
            data[key] = convert_utc_to_jst(value)
        elif isinstance(value, dict):
            data[key] = convert_datetime_timezone(value)
    return data


def convert_utc_to_jst(dt_utc: datetime.datetime) -> datetime.datetime:
    dt_jst = dt_utc.astimezone(gettz(settings.TIME_ZONE))
    return dt_jst
