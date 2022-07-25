import os
import sys
from datetime import datetime

import pytz as tz
from pyflow import Workflow


DATE_FORMAT = os.getenv("DATE_FORMAT", "%d %B, %Y")
TIME_FORMAT = os.getenv("TIME_FORMAT", "%H%:%M:%S")

TIMEZONES = os.getenv("TIMEZONES", "").split(",")


def main(workflow):
    now = datetime.utcnow()

    workflow.new_item(
        title=now.strftime(TIME_FORMAT),
        subtitle=f"{now.strftime(DATE_FORMAT)} [UTC]",
        arg=now.isoformat(),
        copytext=now.isoformat(),
        valid=True,
    ).set_icon_file(
        path="img/icons/utc.png",
    )

    for timezone in TIMEZONES:
        if not timezone:
            continue

        now = datetime.utcnow().replace(tzinfo=tz.utc).astimezone(tz.timezone(timezone))

        offset = now.utcoffset()
        offset_hours = round(offset.days * 24 + offset.seconds / 60 / 60)

        workflow.new_item(
            title=now.strftime(TIME_FORMAT),
            subtitle="{date} [{timezone}]".format(
                date=now.strftime(DATE_FORMAT),
                timezone=timezone.replace("/", ", ").replace("_", " "),
            ),
            arg=now.isoformat(),
            copytext=now.isoformat(),
            valid=True,
        ).set_icon_file(
            path=f"img/icons/{offset_hours}.png",
        )


if __name__ == "__main__":
    wf = Workflow()
    wf.run(main)
    wf.send_feedback()
    sys.exit()
