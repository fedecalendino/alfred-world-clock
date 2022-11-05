import os
import sys
from datetime import datetime

import pytz as tz
from pyflow import Workflow


DATE_FORMAT = os.getenv("DATE_FORMAT", "%d %B, %Y")
TIME_FORMAT = os.getenv("TIME_FORMAT", "%H%:%M:%S")


def main(workflow):
    timezones = map(
        lambda item: item[0][3:].replace("__", "/"),
        filter(
            lambda item: item[0].startswith("TZ_") and item[1] == "1",
            workflow.env.items(),
        ),
    )

    timezones = {
        timezone: datetime.utcnow()
        .replace(tzinfo=tz.utc)
        .astimezone(tz=tz.timezone(timezone))
        for timezone in timezones
    }

    timezones = list(
        sorted(
            timezones.items(),
            key=lambda item: item[1].isoformat(),
        )
    )

    for timezone, now in timezones:
        if timezone == "UTC":
            icon = "img/icons/utc.png"
        else:
            offset = now.utcoffset()
            offset_hours = round(offset.days * 24 + offset.seconds / 60 / 60)
            icon = f"img/icons/{offset_hours}.png"

        workflow.new_item(
            title=now.strftime(TIME_FORMAT),
            subtitle="{date} [{timezone}]".format(
                date=now.strftime(DATE_FORMAT),
                timezone=timezone.replace("/", ", ").replace("_", " "),
            ),
            arg=now.isoformat(),
            copytext=now.isoformat(),
            valid=True,
            uid=timezone,
        ).set_icon_file(
            path=icon,
        )


if __name__ == "__main__":
    wf = Workflow()
    wf.run(main)
    wf.send_feedback()
    sys.exit()
