import sys
from datetime import timedelta
from uuid import uuid4

from pyflow import Workflow

import data
import formatters
import helpers


def add_time(arg):
    if arg[0] == "-":
        is_negative = True
        arg = arg[1:]
    else:
        is_negative = False

    if len(arg) == 0 or (len(arg.strip()) == 1 and arg.startswith("+")):
        return 0

    if arg.endswith(":"):
        arg = arg[:-1]

    arg = arg.split(":")

    if len(arg) == 3:
        hr, minute, sec = arg
        total_seconds = int(hr) * 3600 + int(minute) * 60 + int(sec)
    elif len(arg) == 2:
        hr, minute = arg
        total_seconds = int(hr) * 3600 + int(minute) * 60
    elif len(arg) == 1:
        hr = arg[0]
        total_seconds = int(hr) * 3600

    if is_negative:
        total_seconds = -total_seconds

    return total_seconds


def main(workflow: Workflow):
    home_tz, home_now = helpers.get_home(workflow)
    timezones = helpers.get_timezones(workflow, home_tz)
    formatter = helpers.get_formatter(workflow)
    name_replacements = helpers.get_name_replacements(workflow)
    sorter = lambda pair: pair[1].isoformat()

    total_seconds = 0
    input = ""
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        input = " " + sys.argv[1]
        total_seconds = add_time(arg)

    for timezone, now in sorted(timezones.items(), key=sorter):
        location = timezone.split("/")[-1].replace("_", " ")
        location = name_replacements.get(location, location)

        home_offset_str = helpers.get_home_offset_str(timezone, home_tz, now, home_now) + helpers.get_utc_offset(now)
        now += timedelta(seconds=total_seconds)

        workflow.new_item(
            title=formatter(now) + input,
            subtitle="{flag} {location} {home_offset}".format(
                flag=data.flags.get(timezone, "🌐"),
                location=location,
                home_offset=home_offset_str,
            ),
            arg=formatter(now) + helpers.get_utc_offset(now),
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
