import sys
from uuid import uuid4

from pyflow import Workflow

import data
import formatters
import helpers


def main(workflow: Workflow):
    home_tz, home_now = helpers.get_home(workflow)
    timezones = helpers.get_timezones(workflow, home_tz)
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
                home_offset=helpers.get_home_offset_str(timezone, home_tz, now, home_now),
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
