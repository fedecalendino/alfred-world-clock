import os
import sys
from datetime import datetime

import pytz as tz
from workflow import Workflow


DATE_FORMAT = os.getenv("DATE_FORMAT", "%d %B, %Y")
TIME_FORMAT = os.getenv("TIME_FORMAT", "%H%:%M:%S")

TIMEZONES = os.getenv("TIMEZONES", "").split(",")


def main(workflow):
    now = datetime.utcnow()

    workflow.add_item(
        title=now.strftime(TIME_FORMAT),
        subtitle=f"{now.strftime(DATE_FORMAT)} [UTC]",
        arg=now.isoformat(),
        copytext=now.isoformat(),
        icon="img/icons/utc.png",
        valid=True,
    )

    for timezone in TIMEZONES:
        if not timezone:
            continue

        now = datetime.utcnow().replace(tzinfo=tz.utc).astimezone(tz.timezone(timezone))

        offset = now.utcoffset()
        offset_hours = round(offset.days * 24 + offset.seconds / 60 / 60)

        workflow.add_item(
            title=now.strftime(TIME_FORMAT),
            subtitle="{date} [{timezone}]".format(
                date=now.strftime(DATE_FORMAT),
                timezone=timezone.replace("/", ", ").replace("_", " "),
            ),
            arg=now.isoformat(),
            copytext=now.isoformat(),
            icon=f"img/icons/{offset_hours}.png",
            valid=True,
        )


if __name__ == "__main__":
    wf = Workflow()
    wf.run(main)
    wf.send_feedback()
    sys.exit()
