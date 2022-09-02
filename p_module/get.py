import json


def config(name):
    with open('./settings/' + 'config.json', 'r') as b_cfg:
        json_file = json.load(b_cfg)
        return json_file[name]
