from datetime import datetime


def default(now: datetime) -> str:
    return now.strftime("%H%:%M:%S (%B %d, %Y)")


def iso8601(now: datetime) -> str:
    return now.isoformat()


def iso8601_without_microseconds(now: datetime) -> str:
    return now.replace(microsecond=0).isoformat()


FORMATTERS = {
    "FORMAT_DEFAULT": default,
    "FORMAT_ISO8601_WITH_MICROSECONDS": iso8601,
    "FORMAT_ISO8601_WITHOUT_MICROSECONDS": iso8601_without_microseconds,
}
