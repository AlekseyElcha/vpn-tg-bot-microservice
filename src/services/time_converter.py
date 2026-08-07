from datetime import datetime
from zoneinfo import ZoneInfo


def convert_unix_time_to_hr_time(unix_time: int) -> str:
    if unix_time > 9999999999:
        unix_time = unix_time // 1000

    raw_time = datetime.fromtimestamp(unix_time, tz=ZoneInfo("Europe/Moscow")).isoformat()

    dt_to_format = datetime.fromisoformat(raw_time)

    return dt_to_format.strftime("%d.%m.%Y %H:%M")
