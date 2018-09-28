import requests
import json

# Dict of current robots

mir_list = []
mir_dict = {'MiR_S161': '10.173.175.117',
            'MiR_S162': '10.173.175.121',
            'MiR_S319': '10.173.175.120',
            'MiR_S325': '10.173.175.119',
            'MiR_S326': '10.173.175.116',
            'MiR_S327': '10.173.175.118'
            }


# Class definitions

class MiR():
    """Defining a robot class"""

    status = 'Not accessible!'

    def __init__(self, name, ip):
        self.name = name
        self.ip = ip

    def status_check(self):
        url = f"http://{self.ip}/api/v2.0.0/status"

        headers = {
            'Content-Type': "application/json",
            'authorization': "Basic YWRtaW46OGM2OTc2ZTViNTQxMDQxNWJkZTkwOGJkNGRlZTE1ZGZiMTY3YTljODczZmM0YmI4YTgxZjZmMmFiNDQ4YTkxOA==",
            'Cache-Control': "no-cache",
            'Postman-Token': "bfcd7159-1d12-5b7f-468f-d5e096709cbd"
        }

        response = requests.request("GET", url, headers=headers, timeout=2)
        text = json.loads(response.text)  # str to dict
        return (text.get("state_text"))


# Functions definitions

def creating_robots_list(mir_list: object, mir_dict: object) -> object:
    """Creating list of robots. Called once"""
    for key in mir_dict.keys():
        robot = MiR(key, mir_dict.get(key))
        mir_list.append(robot)


def get_actual_status():
    """Status check and overwrite"""
    for mir in mir_list:
        try:
            mir.status_check()
        except:
            mir.status = 'Not accessible!'


# Main

creating_robots_list(mir_list, mir_dict)
get_actual_status()
