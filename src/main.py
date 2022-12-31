import os
import sys
from uuid import uuid4
from datetime import datetime

import pytz as tz
from pyflow import Workflow

import data


DATE_FORMAT = os.getenv("DATE_FORMAT", "%d %B, %Y")
TIME_FORMAT = os.getenv("TIME_FORMAT", "%H%:%M:%S")


def main(workflow):
    home = workflow.env["HOME"]

    home_tz = home[3:].replace("__", "/")
    home_now = (
        datetime.utcnow()
        .replace(tzinfo=tz.utc)
        .astimezone(
            tz=tz.timezone(home_tz),
        )
    )

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

    timezones = {
        timezone: datetime.utcnow()
        .replace(tzinfo=tz.utc)
        .astimezone(tz=tz.timezone(timezone))
        for timezone in timezones
    }

    for timezone, now in sorted(
        timezones.items(), key=lambda pair: pair[1].isoformat()
    ):
        if timezone == home_tz:
            icon = "img/icons/home.png"
        elif timezone == "UTC":
            icon = "img/icons/utc.png"
        else:
            utc_offset = now.utcoffset()
            utc_offset_hours = round(
                utc_offset.days * 24 + utc_offset.seconds / 60 / 60
            )
            icon = f"img/icons/{utc_offset_hours}.png"

        location = timezone.replace("/", ", ").replace("_", " ")

        if timezone == home_tz:
            home_offset_str = ""
        else:
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

            home_offset_str = "· [{hours:02}:{minutes:02} hs {text} home 🏠]".format(
                hours=seconds // 3600,
                minutes=(seconds % 3600) // 60,
                text=text,
            )

        if workflow.env["INCLUDE_MICROSECONDS"] == "1":
            iso_time = now.isoformat()
        else:
            iso_time = now.replace(microsecond=0).isoformat()

        if workflow.env["DISPLAY_FORMAT_DEFAULT"] == "1":
            display_time = "{time} ({date})".format(
                time=now.strftime(TIME_FORMAT),
                date=now.strftime(DATE_FORMAT),
            )
        else:
            display_time = iso_time

        workflow.new_item(
            # title="{time} ({date})".format(
            #     time=now.strftime(TIME_FORMAT),
            #     date=now.strftime(DATE_FORMAT),
            # ),
            # title="{now}".format(now=iso_time),
            title=display_time,
            subtitle="{flag} {location} {home_offset}".format(
                flag=data.flags.get(timezone, "🌐"),
                location=location,
                home_offset=home_offset_str,
            ),
            arg=iso_time,
            copytext=iso_time,
            valid=True,
            uid=str(uuid4()),
        ).set_icon_file(
            path=icon,
        )


if __name__ == "__main__":
    wf = Workflow()
    wf.run(main)
    wf.send_feedback()
    sys.exit()
