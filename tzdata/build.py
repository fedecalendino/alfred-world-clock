import csv

from data import emojis

with open("country.csv") as file:
    countries = dict(csv.reader(file))


with open('time_zone.csv') as file:
    db = csv.reader(file)

    found = set()

    for row in db:
        timezone, country_code = row[0], row[1]
        country_name = countries[country_code]
        country_flag = emojis[country_code]
        city_name = timezone.split("/")[-1].replace("_", " ")

        found.add((country_name, city_name, country_code, country_flag, timezone))

with open("timezones.checkboxes", "w+") as checkboxes:
    with open("timezones.homes", "w+") as homes:
        for item in sorted(found):
            country_name, city_name, country_code, country_flag, timezone = item

            checkbox = [
                "		<dict>",
                "			<key>config</key>",
                "			<dict>",
                "				<key>default</key>",
                f"				<{'false'}/>",
                "				<key>required</key>",
                "				<false/>",
                "				<key>text</key>",
                f"				<string>{country_flag} {country_name} / {city_name}</string>",
                "			</dict>",
                "			<key>description</key>",
                "			<string></string>",
                "			<key>label</key>",
                f"			<string></string>",
                "			<key>type</key>",
                "			<string>checkbox</string>",
                "			<key>variable</key>",
                f"			<string>TZ_{timezone.replace('/', '__')}</string>",
                "		</dict>",
                "",
            ]

            checkboxes.write("\n".join(checkbox))

            home = [
                "		<array>",
                f"		    <string>{country_flag} {country_name} / {city_name}</string>",
                f"           <string>TZ_{timezone.replace('/', '__')}</string>",
                "       </array>",
                "",
            ]

            homes.write("\n".join(home))
