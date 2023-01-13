from datetime import datetime


def default_12hs(now: datetime) -> str:
    return now.strftime("%I:%M:%S %p (%B %d, %Y)")


def default_24hs(now: datetime) -> str:
    return now.strftime("%H:%M:%S (%B %d, %Y)")


def iso8601(now: datetime) -> str:
    return now.isoformat()


def iso8601_without_microseconds(now: datetime) -> str:
    return now.replace(microsecond=0).isoformat()


FORMATTERS = {
    "FORMAT_DEFAULT": default_24hs,
    "FORMAT_DEFAULT_12HS": default_12hs,
    "FORMAT_DEFAULT_24HS": default_24hs,
    "FORMAT_ISO8601_WITH_MICROSECONDS": iso8601,
    "FORMAT_ISO8601_WITHOUT_MICROSECONDS": iso8601_without_microseconds,
}
