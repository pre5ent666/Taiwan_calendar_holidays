import json
import urllib.request
import datetime
import os
import sys

def save_calendar_json_from_url(year):
    url_address = f'https://cdn.jsdelivr.net/gh/ruyut/TaiwanCalendar/data/{year}.json'
    try:
        with urllib.request.urlopen(url_address) as url:
            data = json.loads(url.read())
    except urllib.error.HTTPError as he:
        print(f"ERROR: Failed to get data from the url {url_address}, please make sure that the {year} calendar is avaliable.")
        sys.exit(1)

    if not os.path.exists("./json"):
        os.mkdir("./json")
    json_data =  json.dumps(data, indent=4, ensure_ascii=False)
    with open(f"./json/calendar_{year}.json", "w", encoding='utf8') as outfile:
        outfile.write(json_data)


def isholiday(dt_str):
    try:
        dt = datetime.datetime.strptime(dt_str, '%Y%m%d')
    except ValueError as ve:
        print(f"ERROR: {ve}")
        sys.exit(1)

    y = dt.year
    file_path = f"./json/calendar_{y}.json"

    if not os.path.exists(file_path):
        save_calendar_json_from_url(year=y)
    
    data = open(file_path, "r")
    holiday_calendar = json.load(data)
    date_info = list(filter(lambda x:x["date"]==dt_str, holiday_calendar))
    return date_info[0]["isHoliday"]


if __name__ == "__main__":
    dt_str = "20240113"
    print(isholiday(dt_str))