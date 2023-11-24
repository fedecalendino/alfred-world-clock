import sys
from datetime import timedelta, datetime
from uuid import uuid4

import pytz as tz
from pyflow import Workflow

import data
import formatters
from main import *
import json

from json import JSONEncoder

#BASE_DIR = os.path.dirname(os.path.realpath(__file__))

def workflow_default(obj):
    if isinstance(obj, Workflow):
        return obj.__dict__
    else:
        pass
        #raise TypeError("Object of type {} is not JSON serializable".format(type(obj)))


def convert_to_datetime(arg):
    formats = ["%H:%M:%S", "%H:%M:%S %d-%m-%Y"]
    
    for format_str in formats:
        try:
            return datetime.strptime(arg, format_str)
        except ValueError:
            pass
    
    print("Invalid datetime format")
    return None

def get_home_(workflow):
    home_tz = workflow.env["HOME"][3:].replace("__", "/")

    # home_now = (
    #     datetime.utcnow()
    #     .replace(tzinfo=tz.utc)
    #     .astimezone(
    #         tz=tz.timezone(home_tz),
    #     )
    # )

    home_now = handleinput()

    #print(home_tz, home_now)

    return home_tz, home_now


def get_timezones_(workflow, home_tz):
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
        timezone: handleinput()
        .replace(tzinfo=tz.utc)
        .astimezone(tz=tz.timezone(timezone))
        for timezone in timezones
    }


def handleinput():
    if len(sys.argv) > 1:
        input_datetime = convert_to_datetime(sys.argv[1])
        if input_datetime:
            # If no date is provided, use today's date
            if len(sys.argv) == 2:
                input_datetime = datetime.now().replace(hour=input_datetime.hour, minute=input_datetime.minute, second=input_datetime.second)
            else:
                # If a date is provided, use that date
                input_datetime = input_datetime.replace(year=int(sys.argv[2].split('-')[2]), month=int(sys.argv[2].split('-')[1]), day=int(sys.argv[2].split('-')[0]))
            #print("Converted datetime:", input_datetime.strftime("%Y-%m-%d %H:%M:%S"))
    else:
        return datetime.now()
        #print("Please provide a datetime string as a command-line argument.")

    return input_datetime


def meet(workflow):

    home_tz, home_now = get_home_(workflow)
    timezones = get_timezones_(workflow, home_tz)
    formatter = get_formatter(workflow)

    # with open('workflow.json', 'w') as json_file:
    #     json.dump(workflow,json_file, sort_keys=False, indent=4, default=workflow_default)

    name_replacements = get_name_replacements(workflow)

    sorter = lambda pair: pair[1].isoformat()

    for timezone, now in sorted(timezones.items(), key=sorter):
        location = timezone.split("/")[-1].replace("_", " ")
        location = name_replacements.get(location, location)

        home_offset_str = get_home_offset_str(timezone, home_tz, now, home_now) + get_utc(timezone, now, home_tz)

        #print(home_tz, home_now, now)

        workflow.new_item(
            title=formatter(now),
            subtitle="{flag} {location} {home_offset}".format(
                flag=data.flags.get(timezone, "🌐"),
                location=location,
                home_offset=home_offset_str,
            ),
            arg=formatter(now) + get_utc(timezone, now, home_tz),
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
    #wf.save_env()
    wf.run(meet)
    wf.send_feedback()
    sys.exit()
