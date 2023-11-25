import sys
from datetime import datetime, timedelta
from typing import List
from uuid import uuid4

from pyflow import Workflow
from pytimeparse.timeparse import timeparse

import data
import formatters
import helpers


# parse parameter to a set of valid time formats
def convert_to_time(time_arg: str) -> datetime:
    for format_str in ["%H:%M:%S", "%H:%M"]:
        try:
            time = datetime.strptime(time_arg, format_str)

            return datetime.utcnow().replace(
                hour=time.hour,
                minute=time.minute,
                second=time.second,
            )
        except ValueError:
            pass

    raise ValueError(f"'{time_arg}' should follow the formats 'HH:MM:SS' or 'HH:MM'")


# parse parameter to a set of valid date formats
def convert_to_date(date_arg: str) -> datetime:
    for format_str in ["%d/%m/%Y", "%Y-%m-%d"]:
        try:
            date = datetime.strptime(date_arg, format_str)

            return datetime.utcnow().replace(
                day=date.day,
                month=date.month,
                year=date.year,
            )
        except ValueError:
            pass

    raise ValueError(f"'{date_arg}' should follow the formats 'dd/mm/yyyy' or 'yyyy-mm-dd'")


# parse a positive or negative time offset to create a delta in seconds
def convert_to_delta(delta_arg: str) -> timedelta:
    try:
        return timedelta(
            seconds=timeparse(delta_arg),
        )
    except TypeError:
        raise ValueError("invalid time offset")


# parse arguments to find in which mode the workflow is running
def parse_args(args: List[str]) -> datetime:
    if len(args) > 2:
        raise ValueError("too many params, expected: [+offset] / [-offset] / [time] / [time date]")

    now = datetime.utcnow()

    # mode now: shows current time
    if len(args) == 0:
        return now

    # mode offset: shows current time +/- a time offset
    if args[0][0] in "+-":
        return now + convert_to_delta(args[0])

    # mode set: shows especific date and time
    time = convert_to_time(args[0])

    now = now.replace(
        hour=time.hour,
        minute=time.minute,
        second=time.second,
        microsecond=0,
    )

    if len(args) == 2:
        date = convert_to_date(args[1])

        now = now.replace(
            day=date.day,
            month=date.month,
            year=date.year,
        )

    return now


def main(workflow: Workflow):
    now = parse_args(workflow.args)

    home_tz, home_now = helpers.get_home(workflow)
    timezones = helpers.get_timezones(workflow, now, home_tz)
    formatter = helpers.get_formatter(workflow)
    name_replacements = helpers.get_name_replacements(workflow)

    for timezone, now in sorted(timezones.items(), key=lambda pair: pair[1].isoformat()):
        location = timezone.split("/")[-1].replace("_", " ")
        location = name_replacements.get(location, location)

        workflow.new_item(
            title=formatter(now),
            subtitle="{flag} {location} {home_offset}".format(
                flag=data.flags.get(timezone, "🌐"),
                location=location,
                home_offset=helpers.get_home_offset_str(
                    timezone=timezone,
                    home_tz=home_tz,
                    now=now,
                    home_now=home_now,
                ),
            ),
            arg=formatter(now),
            copytext=formatter(now),
            valid=True,
            uid=str(uuid4()),
        ).set_icon_file(
            path=helpers.get_icon(timezone, now, home_tz),
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
