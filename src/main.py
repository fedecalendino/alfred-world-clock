import sys
from datetime import datetime
from uuid import uuid4

import pytz as tz
from pyflow import Workflow

import data
import formatters


def get_home(workflow):
    home_tz = workflow.env["HOME"][3:].replace("__", "/")

    home_now = (
        datetime.utcnow()
        .replace(tzinfo=tz.utc)
        .astimezone(
            tz=tz.timezone(home_tz),
        )
    )

    return home_tz, home_now


def get_timezones(workflow, home_tz):
    timezones = set(
        map(
            lambda item: item[0][3:].replace("__", "/"),
            filter(
                lambda item: item[0].startswith("TZ_") and item[1] == "1",
                workflow.env.items(),
            ),
        )
    )

    timezones.add(home_tz)

    return {
        timezone: datetime.utcnow()
        .replace(tzinfo=tz.utc)
        .astimezone(tz=tz.timezone(timezone))
        for timezone in timezones
    }


def get_formatter(workflow):
    timestamp_format = workflow.env.get("TIMESTAMP_FORMAT", formatters.default)
    return formatters.FORMATTERS[timestamp_format]


def get_icon(timezone, now, home_tz):
    if timezone == home_tz:
        return "img/icons/home.png"

    if timezone == "UTC":
        return "img/icons/utc.png"

    utc_offset = now.utcoffset()
    utc_offset_hours = round(utc_offset.days * 24 + utc_offset.seconds / 60 / 60)
    return f"img/icons/{utc_offset_hours}.png"


def get_home_offset_str(timezone, home_tz, now, home_now) -> str:
    if timezone == home_tz:
        return ""

    now_tmp = now.replace(tzinfo=None)
    home_now_tmp = home_now.replace(tzinfo=None)

    if home_now_tmp > now_tmp:
        home_offset = home_now_tmp - now_tmp
        seconds = home_offset.seconds + 1
        text = "behind"
    else:
        home_offset = home_now_tmp - now_tmp
        seconds = 24 * 60 * 60 - home_offset.seconds + 1
        text = "ahead of"

    return "· [{hours:02}:{minutes:02} hs {text} home 🏠]".format(
        hours=seconds // 3600,
        minutes=(seconds % 3600) // 60,
        text=text,
    )


def main(workflow):
    home_tz, home_now = get_home(workflow)
    timezones = get_timezones(workflow, home_tz)
    formatter = get_formatter(workflow)

    sorter = lambda pair: pair[1].isoformat()

    for timezone, now in sorted(timezones.items(), key=sorter):
        location = timezone.replace("/", ", ").replace("_", " ")
        home_offset_str = get_home_offset_str(timezone, home_tz, now, home_now)

        workflow.new_item(
            title=formatter(now),
            subtitle="{flag} {location} {home_offset}".format(
                flag=data.flags.get(timezone, "🌐"),
                location=location,
                home_offset=home_offset_str,
            ),
            arg=formatter(now),
            copytext=formatter(now),
            valid=True,
            uid=str(uuid4()),
        ).set_icon_file(
            path=get_icon(timezone, now, home_tz),
        ).set_alt_mod(
            subtitle="Copy ISO format (with microseconds)",
            arg=formatters.iso8601(now),
        ).set_cmd_mod(
            subtitle="Copy ISO format (without microseconds)",
            arg=formatters.iso8601_without_microseconds(now),
        )


if __name__ == "__main__":
    wf = Workflow()
    wf.run(main)
    wf.send_feedback()
    sys.exit()
