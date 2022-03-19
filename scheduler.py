
import subprocess
from datetime import date, datetime
import sys
import yaml

def parse_yaml(yaml_file):
    with open(yaml_file, "r") as f:
        try:
            parsed_yaml=yaml.safe_load(f)
            return parsed_yaml
        except yaml.YAMLError as exc:
            return exc

def odd_even(x):
    if x % 2 == 0:
        return True
    else:
        return False

def post(csv_file):
    subprocess.run(['docker exec fava bash -c "bean-extract /bean/config/ledger_importers/config.py /bean/data/scheduled/' + csv_file + ' >> /bean/data/inbox.beancount"'], shell=True)

def main(yaml_file):
    today = date.today()

    file = parse_yaml(yaml_file)
    for list in file.values():
        for dict_item in list:
            start_date = datetime.strptime(dict_item["start_date"], '%Y-%m-%d').date()
            frequency = dict_item["frequency"]
            csv_file = dict_item["csv_file"]
            if frequency == "monthly":
                if start_date.day is today.day:
                    post(csv_file)
            elif frequency == "fortnightly":
                if odd_even(start_date.isocalendar().week) == odd_even(today.isocalendar().week):
                    post(csv_file)
            elif frequency == "weekly":
                if start_date.weekday() is today.weekday():
                    post(csv_file)
            else:
                pass

if __name__ == "__main__":
    main(sys.argv[1])