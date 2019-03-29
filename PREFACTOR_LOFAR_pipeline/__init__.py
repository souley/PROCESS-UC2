import json
import os
import subprocess
#from fabric import Connection
import requests

def give_name():
    jsonfile = give_config()
    name = list(jsonfile.keys())[0]
    return name

def give_version():
    return "0.1"

def give_config():
    json_config_file = os.path.join(os.path.dirname(__file__), "data", "config.json")
    with open(json_config_file) as json_data:
        return json.load(json_data)

def give_argument_names(required=False):
    jsonfile = give_config()
    name = list(jsonfile.keys())[0]
    required = jsonfile[name]["schema"]["required"]
    properties = set(jsonfile[name]["schema"]["properties"].keys())
    if required:
        return required
    else:
        return properties

def run_pipeline(observation, **kargs):
	# Start your pipeline here
#    print("===OBSERVATION: " + observation)
    url = '/jobs'
    headers = {
        'Content-Type': 'application/json',
    }
    data = {
        "input": {}
    }
#    print(kargs)
    for kw in kargs:
        if kw == "xenon_server_url":
            url = kargs[kw] + url
        elif kw == "api_key":
            headers["api-key"] = kargs[kw]
        elif kw == "workflow_name":
            data["name"] = kargs[kw]
        elif kw == "workflow_cwl":
            data["workflow"] = kargs[kw]
    res = requests.post(url, headers=headers, data=json.dumps(data))
    # Parse HttpResponse and return xenon-flow job id for later use
    # check content of res.data and retrieve res.data['id']???
#    print(res.content)
    res_data = json.loads(res.content.decode("utf8"))
#    print("===xenon job id: ", res_data["id"])
    res_val = "xenon-flow job id: " + res_data["id"]
    return res
#    return "Testing ..."
