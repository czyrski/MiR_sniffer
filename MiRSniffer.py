from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty, DictProperty, ListProperty, NumericProperty
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.config import Config

from os import listdir
import requests
import json

# Window config
Config.set('graphics', 'width', '900')
Config.set('graphics', 'height', '500')

# Kivy files build
kv_path = './kv/'
for kv in listdir(kv_path):
    Builder.load_file(kv_path + kv)


# Class declarations
class MirSniffer(ScreenManager):
    pass


class MainScreen(Screen):
    index = NumericProperty(0)
    robots_dict = DictProperty({'MiR_S161': '10.173.175.117',
                                'MiR_S162': '10.173.175.121',
                                'MiR_S319': '10.173.175.120',
                                'MiR_S325': '10.173.175.119',
                                'MiR_S326': '10.173.175.116',
                                'MiR_S327': '10.173.175.118'
                                })
    status_robots = ListProperty(['', '', '', '', '', ''])
    buttons_color = ListProperty([[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1],
                                  [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]])

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        Clock.schedule_once(self.change_robot_status, -1)
        Clock.schedule_interval(self.change_robot_status, 20)  # MAIN SCREEN UPDATED EVERY xxSEC

    def change_robot_status(self, *args):
        self.index = 0
        for key in self.robots_dict.keys():
            try:
                url = f"http://{self.robots_dict.get(key)}/api/v2.0.0/status"

                headers = {
                    'Content-Type': "application/json",
                    'authorization': "Basic YWRtaW46OGM2OTc2ZTViNTQxMDQxNWJkZTkwOGJkNGRlZTE1ZGZiMTY3YTljODczZmM0YmI4YTgxZjZmMmFiNDQ4YTkxOA==",
                    'Cache-Control': "no-cache",
                    'Postman-Token': "bfcd7159-1d12-5b7f-468f-d5e096709cbd"
                }

                response = requests.request("GET", url, headers=headers, timeout=.5)
                text = json.loads(response.text)  # str to dict
                self.status_robots[self.index] = text.get("state_text")
                if text.get("state_text") == 'Error':
                    self.buttons_color[self.index] = [1, .2, .2, 1]
                elif text.get("state_text") == 'Pause':
                    self.buttons_color[self.index] = [.9, .7, .1, 1]
                elif text.get("state_text") == 'Ready':
                    self.buttons_color[self.index] = [1, 1, 1, 1]
                elif text.get("state_text") == 'EmergencyStop':
                    self.buttons_color[self.index] = [1, .2, .2, 1]
                elif text.get("state_text") == 'Executing':
                    self.buttons_color[self.index] = [1, 1, 1, 1]
            except:
                self.status_robots[self.index] = 'Not accessible!'
                self.buttons_color[self.index] = [1, .2, .2, 1]

            self.index += 1
            if self.index == 6:
                self.index = 0


class Mir161(Screen):
    robot_ip = StringProperty('10.173.175.117')
    robot_status = StringProperty('Not accessible.')
    battery_per = StringProperty('Not accessible.')
    battery_time = StringProperty('Not accessible.')
    error_description = StringProperty('Not accessible.')
    mission_text = StringProperty('Not accessible.')
    mission_id = StringProperty('Not accessible.')
    register = ListProperty(['LOW', 'LOW', 'LOW', 'LOW'])
    button_colors = ListProperty([[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]])

    def __init__(self, **kwargs):
        super(Mir161, self).__init__(**kwargs)
        Clock.schedule_once(self.change_robot_status, -1)
        Clock.schedule_interval(self.change_robot_status, 30)  # ROBOT PRIMARY PROPERTIES CHANGED EVERY 30SEC
        Clock.schedule_once(self.check_registers, -1)

    def change_robot_status(self, *args):
        try:
            url = f"http://{self.robot_ip}/api/v2.0.0/status"

            headers = {
                'Content-Type': "application/json",
                'authorization': "Basic YWRtaW46OGM2OTc2ZTViNTQxMDQxNWJkZTkwOGJkNGRlZTE1ZGZiMTY3YTljODczZmM0YmI4YTgxZjZmMmFiNDQ4YTkxOA==",
                'Cache-Control': "no-cache",
                'Postman-Token': "bfcd7159-1d12-5b7f-468f-d5e096709cbd"
            }

            response = requests.request("GET", url, headers=headers, timeout=.5)
            text = json.loads(response.text)  # str to dict
            self.robot_status = text.get("state_text")
            self.battery_per = str(text.get("battery_percentage"))
            self.battery_per = self.battery_per[:4]
            self.battery_time = str(text.get("battery_time_remaining"))
            # self.error_description = text['errors']['description']
            self.mission_text = text.get('mission_text')
            self.mission_id = str(text.get('mission_queue_id'))
        except:
            self.robot_status = 'Not accessible'
            self.battery_per = 'Not accessible'
            self.battery_time = 'Not accessible'
            self.error_description = 'Not accessible'
            self.mission_text = 'Not accessible'
            self.mission_id = 'Not accessible'

    def check_registers(self, *args):
        for i in range(101, 105):
            try:
                url = f"http://{self.robot_ip}/api/v2.0.0/registers/{i}"
                headers = {
                    'Content-Type': "application/json",
                    'authorization': "Basic YWRtaW46OGM2OTc2ZTViNTQxMDQxNWJkZTkwOGJkNGRlZTE1ZGZiMTY3YTljODczZmM0YmI4YTgxZjZmMmFiNDQ4YTkxOA==",
                    'Cache-Control': "no-cache",
                    'Postman-Token': "0db92846-36d7-ab5e-b336-1fafd9a409a3"
                }
                response = requests.request("GET", url, headers=headers, timeout=.5)
                text = json.loads(response.text)  # str to dict
                if text.get("value") == 1.0:
                    self.register[int(reg_number) - 101] = 'HIGH'
                elif text.get("value") == 0.0:
                    self.register[int(reg_number) - 101] = 'LOW'
            except:
                self.register[i - 101] = 'LOW'

    def set_register(self, reg_number):

        if self.register[int(reg_number) - 101] == 'LOW':
            reg_value = 1.0
        elif self.register[int(reg_number) - 101] == 'HIGH':
            reg_value = 0.0

        try:
            url = f"http://{self.robot_ip}/api/v2.0.0/registers/{reg_number}"
            data = {"value": reg_value, "label": "MiR Sniffer"}
            headers = {
                'Content-Type': "application/json",
                'authorization': "Basic YWRtaW46OGM2OTc2ZTViNTQxMDQxNWJkZTkwOGJkNGRlZTE1ZGZiMTY3YTljODczZmM0YmI4YTgxZjZmMmFiNDQ4YTkxOA==",
                'Cache-Control': "no-cache",
                'Postman-Token': "bfcd7159-1d12-5b7f-468f-d5e096709cbd"
            }
            response = requests.put(url, data=json.dumps(data), headers=headers, timeout=0.5)
            text = json.loads(response.text)  # str to dict
            # self.register[int(reg_number)-101] = str(text.get("value"))
            if text.get("value") == 1.0:
                self.register[int(reg_number) - 101] = 'HIGH'
            elif text.get("value") == 0.0:
                self.register[int(reg_number) - 101] = 'LOW'

        except:
            pass

    def change_button_color(self, reg_number):
        if self.register[int(reg_number) - 101] == 'HIGH':
            self.button_colors[int(reg_number) - 101] = [1, 1, 1, 1]
        elif self.register[int(reg_number) - 101] == 'LOW':
            self.button_colors[int(reg_number) - 101] = [0.3, 0.9, 0.1, 1]


class Mir162(Screen):
    robot_ip = StringProperty('10.173.175.121')
    robot_status = StringProperty('Not accessible.')
    battery_per = StringProperty('Not accessible.')
    battery_time = StringProperty('Not  accessible.')
    error_description = StringProperty('Not accessible.')
    mission_text = StringProperty('Not accessible.')
    mission_id = StringProperty('Not accessible.')
    register = ListProperty(['LOW', 'LOW', 'LOW', 'LOW'])
    button_colors = ListProperty([[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]])

    def __init__(self, **kwargs):
        super(Mir162, self).__init__(**kwargs)
        Clock.schedule_once(self.change_robot_status, -1)
        Clock.schedule_interval(self.change_robot_status, 30)

    def change_robot_status(self, *args):
        try:
            url = f"http://{self.robot_ip}/api/v2.0.0/status"

            headers = {
                'Content-Type': "application/json",
                'authorization': "Basic YWRtaW46OGM2OTc2ZTViNTQxMDQxNWJkZTkwOGJkNGRlZTE1ZGZiMTY3YTljODczZmM0YmI4YTgxZjZmMmFiNDQ4YTkxOA==",
                'Cache-Control': "no-cache",
                'Postman-Token': "bfcd7159-1d12-5b7f-468f-d5e096709cbd"
            }

            response = requests.request("GET", url, headers=headers, timeout=.5)
            text = json.loads(response.text)  # str to dict
            self.robot_status = text.get("state_text")
            self.battery_per = str(text.get("battery_percentage"))
            self.battery_per = self.battery_per[:4]
            self.battery_time = str(text.get("battery_time_remaining"))
            # self.error_description = text['errors']['description']
            self.mission_text = text.get('mission_text')
            self.mission_id = str(text.get('mission_queue_id'))
        except:
            self.robot_status = 'Not accessible'
            self.battery_per = 'Not accessible'
            self.battery_time = 'Not accessible'
            self.error_description = 'Not accessible'
            self.mission_text = 'Not accessible'
            self.mission_id = 'Not accessible'

    def check_registers(self, *args):
        for i in range(101, 105):
            try:
                url = f"http://{self.robot_ip}/api/v2.0.0/registers/{i}"
                headers = {
                    'Content-Type': "application/json",
                    'authorization': "Basic YWRtaW46OGM2OTc2ZTViNTQxMDQxNWJkZTkwOGJkNGRlZTE1ZGZiMTY3YTljODczZmM0YmI4YTgxZjZmMmFiNDQ4YTkxOA==",
                    'Cache-Control': "no-cache",
                    'Postman-Token': "0db92846-36d7-ab5e-b336-1fafd9a409a3"
                }
                response = requests.request("GET", url, headers=headers, timeout=.5)
                text = json.loads(response.text)  # str to dict
                if text.get("value") == 1.0:
                    self.register[int(reg_number) - 101] = 'HIGH'
                elif text.get("value") == 0.0:
                    self.register[int(reg_number) - 101] = 'LOW'
            except:
                self.register[i - 101] = 'LOW'

    def set_register(self, reg_number):

        if self.register[int(reg_number) - 101] == 'LOW':
            reg_value = 1.0
        elif self.register[int(reg_number) - 101] == 'HIGH':
            reg_value = 0.0

        try:
            url = f"http://{self.robot_ip}/api/v2.0.0/registers/{reg_number}"
            data = {"value": reg_value, "label": "MiR Sniffer"}
            headers = {
                'Content-Type': "application/json",
                'authorization': "Basic YWRtaW46OGM2OTc2ZTViNTQxMDQxNWJkZTkwOGJkNGRlZTE1ZGZiMTY3YTljODczZmM0YmI4YTgxZjZmMmFiNDQ4YTkxOA==",
                'Cache-Control': "no-cache",
                'Postman-Token': "bfcd7159-1d12-5b7f-468f-d5e096709cbd"
            }
            response = requests.put(url, data=json.dumps(data), headers=headers)
            text = json.loads(response.text)  # str to dict
            # self.register[int(reg_number)-101] = str(text.get("value"))
            if text.get("value") == 1.0:
                self.register[int(reg_number) - 101] = 'HIGH'
            elif text.get("value") == 0.0:
                self.register[int(reg_number) - 101] = 'LOW'

        except:
            pass

    def change_button_color(self, reg_number):
        if self.register[int(reg_number) - 101] == 'HIGH':
            self.button_colors[int(reg_number) - 101] = [1, 1, 1, 1]
        elif self.register[int(reg_number) - 101] == 'LOW':
            self.button_colors[int(reg_number) - 101] = [0.3, 0.9, 0.1, 1]


class Mir319(Screen):
    robot_ip = StringProperty('10.173.175.120')
    robot_status = StringProperty('Not accessible.')
    battery_per = StringProperty('Not accessible.')
    battery_time = StringProperty('Not accessible.')
    error_description = StringProperty('Not accessible.')
    mission_text = StringProperty('Not accessible.')
    mission_id = StringProperty('Not accessible.')
    register = ListProperty(['LOW', 'LOW', 'LOW', 'LOW'])
    button_colors = ListProperty([[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]])

    def __init__(self, **kwargs):
        super(Mir319, self).__init__(**kwargs)
        Clock.schedule_once(self.change_robot_status, -1)
        Clock.schedule_interval(self.change_robot_status, 30)

    def change_robot_status(self, *args):
        try:
            url = f"http://{self.robot_ip}/api/v2.0.0/status"

            headers = {
                'Content-Type': "application/json",
                'authorization': "Basic YWRtaW46OGM2OTc2ZTViNTQxMDQxNWJkZTkwOGJkNGRlZTE1ZGZiMTY3YTljODczZmM0YmI4YTgxZjZmMmFiNDQ4YTkxOA==",
                'Cache-Control': "no-cache",
                'Postman-Token': "bfcd7159-1d12-5b7f-468f-d5e096709cbd"
            }

            response = requests.request("GET", url, headers=headers, timeout=.5)
            text = json.loads(response.text)  # str to dict
            self.robot_status = text.get("state_text")
            self.battery_per = str(text.get("battery_percentage"))
            self.battery_per = self.battery_per[:4]
            self.battery_time = str(text.get("battery_time_remaining"))
            self.error_description = text['errors']['description']
            self.mission_text = text.get('mission_text')
            self.mission_id = str(text.get('mission_queue_id'))
        except:
            self.robot_status = 'Not accessible'
            self.battery_per = 'Not accessible'
            self.battery_time = 'Not accessible'
            self.error_description = 'Not accessible'
            self.mission_text = 'Not accessible'
            self.mission_id = 'Not accessible'

    def check_registers(self, *args):
        for i in range(101, 105):
            try:
                url = f"http://{self.robot_ip}/api/v2.0.0/registers/{i}"
                headers = {
                    'Content-Type': "application/json",
                    'authorization': "Basic YWRtaW46OGM2OTc2ZTViNTQxMDQxNWJkZTkwOGJkNGRlZTE1ZGZiMTY3YTljODczZmM0YmI4YTgxZjZmMmFiNDQ4YTkxOA==",
                    'Cache-Control': "no-cache",
                    'Postman-Token': "0db92846-36d7-ab5e-b336-1fafd9a409a3"
                }
                response = requests.request("GET", url, headers=headers, timeout=.5)
                text = json.loads(response.text)  # str to dict
                if text.get("value") == 1.0:
                    self.register[int(reg_number) - 101] = 'HIGH'
                elif text.get("value") == 0.0:
                    self.register[int(reg_number) - 101] = 'LOW'
            except:
                self.register[i - 101] = 'LOW'

    def set_register(self, reg_number):

        if self.register[int(reg_number) - 101] == 'LOW':
            reg_value = 1.0
        elif self.register[int(reg_number) - 101] == 'HIGH':
            reg_value = 0.0

        try:
            url = f"http://{self.robot_ip}/api/v2.0.0/registers/{reg_number}"
            data = {"value": reg_value, "label": "MiR Sniffer"}
            headers = {
                'Content-Type': "application/json",
                'authorization': "Basic YWRtaW46OGM2OTc2ZTViNTQxMDQxNWJkZTkwOGJkNGRlZTE1ZGZiMTY3YTljODczZmM0YmI4YTgxZjZmMmFiNDQ4YTkxOA==",
                'Cache-Control': "no-cache",
                'Postman-Token': "bfcd7159-1d12-5b7f-468f-d5e096709cbd"
            }
            response = requests.put(url, data=json.dumps(data), headers=headers)
            text = json.loads(response.text)  # str to dict
            # self.register[int(reg_number)-101] = str(text.get("value"))
            if text.get("value") == 1.0:
                self.register[int(reg_number) - 101] = 'HIGH'
            elif text.get("value") == 0.0:
                self.register[int(reg_number) - 101] = 'LOW'

        except:
            pass

    def change_button_color(self, reg_number):
        if self.register[int(reg_number) - 101] == 'HIGH':
            self.button_colors[int(reg_number) - 101] = [1, 1, 1, 1]
        elif self.register[int(reg_number) - 101] == 'LOW':
            self.button_colors[int(reg_number) - 101] = [0.3, 0.9, 0.1, 1]


class Mir325(Screen):
    robot_ip = StringProperty('10.173.175.119')
    robot_status = StringProperty('Not accessible.')
    battery_per = StringProperty('Not accessible.')
    battery_time = StringProperty('Not accessible.')
    error_description = StringProperty('Not accessible.')
    mission_text = StringProperty('Not accessible.')
    mission_id = StringProperty('Not accessible.')
    register = ListProperty(['LOW', 'LOW', 'LOW', 'LOW'])
    button_colors = ListProperty([[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]])

    def __init__(self, **kwargs):
        super(Mir325, self).__init__(**kwargs)
        Clock.schedule_once(self.change_robot_status, -1)
        Clock.schedule_interval(self.change_robot_status, 30)
        Clock.schedule_interval(self.check_registers, 30)

    def change_robot_status(self, *args):
        try:
            url = f"http://{self.robot_ip}/api/v2.0.0/status"

            headers = {
                'Content-Type': "application/json",
                'authorization': "Basic YWRtaW46OGM2OTc2ZTViNTQxMDQxNWJkZTkwOGJkNGRlZTE1ZGZiMTY3YTljODczZmM0YmI4YTgxZjZmMmFiNDQ4YTkxOA==",
                'Cache-Control': "no-cache",
                'Postman-Token': "bfcd7159-1d12-5b7f-468f-d5e096709cbd"
            }

            response = requests.request("GET", url, headers=headers, timeout=.5)
            text = json.loads(response.text)  # str to dict
            self.robot_status = text.get("state_text")
            self.battery_per = str(text.get("battery_percentage"))
            self.battery_per = self.battery_per[:4]
            self.battery_time = str(text.get("battery_time_remaining"))
            # self.error_description = text['errors'][0]['description']
            self.mission_text = text.get('mission_text')
            self.mission_id = str(text.get('mission_queue_id'))
        except:
            self.robot_status = 'Not accessible'
            self.battery_per = 'Not accessible'
            self.battery_time = 'Not accessible'
            self.error_description = 'Not accessible'
            self.mission_text = 'Not accessible'
            self.mission_id = 'Not accessible'

    def check_registers(self, *args):
        for i in range(101, 105):
            try:
                url = f"http://{self.robot_ip}/api/v2.0.0/registers/{i}"
                headers = {
                    'Content-Type': "application/json",
                    'authorization': "Basic YWRtaW46OGM2OTc2ZTViNTQxMDQxNWJkZTkwOGJkNGRlZTE1ZGZiMTY3YTljODczZmM0YmI4YTgxZjZmMmFiNDQ4YTkxOA==",
                    'Cache-Control': "no-cache",
                    'Postman-Token': "0db92846-36d7-ab5e-b336-1fafd9a409a3"
                }
                response = requests.request("GET", url, headers=headers, timeout=.5)
                text = json.loads(response.text)  # str to dict
                if text.get("value") == 1.0:
                    self.register[int(reg_number) - 101] = 'HIGH'
                elif text.get("value") == 0.0:
                    self.register[int(reg_number) - 101] = 'LOW'
            except:
                self.register[i - 101] = 'LOW'

    def set_register(self, reg_number):

        if self.register[int(reg_number) - 101] == 'LOW':
            reg_value = 1.0
        elif self.register[int(reg_number) - 101] == 'HIGH':
            reg_value = 0.0

        try:
            url = f"http://{self.robot_ip}/api/v2.0.0/registers/{reg_number}"
            data = {"value": reg_value, "label": "MiR Sniffer"}
            headers = {
                'Content-Type': "application/json",
                'authorization': "Basic YWRtaW46OGM2OTc2ZTViNTQxMDQxNWJkZTkwOGJkNGRlZTE1ZGZiMTY3YTljODczZmM0YmI4YTgxZjZmMmFiNDQ4YTkxOA==",
                'Cache-Control': "no-cache",
                'Postman-Token': "bfcd7159-1d12-5b7f-468f-d5e096709cbd"
            }
            response = requests.put(url, data=json.dumps(data), headers=headers)
            text = json.loads(response.text)  # str to dict
            # self.register[int(reg_number)-101] = str(text.get("value"))
            if text.get("value") == 1.0:
                self.register[int(reg_number) - 101] = 'HIGH'
            elif text.get("value") == 0.0:
                self.register[int(reg_number) - 101] = 'LOW'

        except:
            pass

    def change_button_color(self, reg_number):
        if self.register[int(reg_number) - 101] == 'HIGH':
            self.button_colors[int(reg_number) - 101] = [1, 1, 1, 1]
        elif self.register[int(reg_number) - 101] == 'LOW':
            self.button_colors[int(reg_number) - 101] = [0.3, 0.9, 0.1, 1]


class Mir326(Screen):
    robot_ip = StringProperty('10.173.175.116')
    robot_status = StringProperty('Not accessible.')
    battery_per = StringProperty('Not accessible.')
    battery_time = StringProperty('Not accessible.')
    error_description = StringProperty('Not accessible.')
    mission_text = StringProperty('Not accessible.')
    mission_id = StringProperty('Not accessible.')
    register = ListProperty(['LOW', 'LOW', 'LOW', 'LOW'])
    button_colors = ListProperty([[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]])

    def __init__(self, **kwargs):
        super(Mir326, self).__init__(**kwargs)
        Clock.schedule_once(self.change_robot_status, -1)
        Clock.schedule_interval(self.change_robot_status, 30)

    def change_robot_status(self, *args):
        try:
            url = f"http://{self.robot_ip}/api/v2.0.0/status"

            headers = {
                'Content-Type': "application/json",
                'authorization': "Basic YWRtaW46OGM2OTc2ZTViNTQxMDQxNWJkZTkwOGJkNGRlZTE1ZGZiMTY3YTljODczZmM0YmI4YTgxZjZmMmFiNDQ4YTkxOA==",
                'Cache-Control': "no-cache",
                'Postman-Token': "bfcd7159-1d12-5b7f-468f-d5e096709cbd"
            }

            response = requests.request("GET", url, headers=headers, timeout=.5)
            text = json.loads(response.text)  # str to dict
            self.robot_status = text.get("state_text")
            self.battery_per = str(text.get("battery_percentage"))
            self.battery_per = self.battery_per[:4]
            self.battery_time = str(text.get("battery_time_remaining"))
            # self.error_description = text['errors']['description']
            self.mission_text = text.get('mission_text')
            self.mission_id = str(text.get('mission_queue_id'))
        except:
            self.robot_status = 'Not accessible'
            self.battery_per = 'Not accessible'
            self.battery_time = 'Not accessible'
            self.error_description = 'Not accessible'
            self.mission_text = 'Not accessible'
            self.mission_id = 'Not accessible'

    def check_registers(self, *args):
        for i in range(101, 105):
            try:
                url = f"http://{self.robot_ip}/api/v2.0.0/registers/{i}"
                headers = {
                    'Content-Type': "application/json",
                    'authorization': "Basic YWRtaW46OGM2OTc2ZTViNTQxMDQxNWJkZTkwOGJkNGRlZTE1ZGZiMTY3YTljODczZmM0YmI4YTgxZjZmMmFiNDQ4YTkxOA==",
                    'Cache-Control': "no-cache",
                    'Postman-Token': "0db92846-36d7-ab5e-b336-1fafd9a409a3"
                }
                response = requests.request("GET", url, headers=headers, timeout=.5)
                text = json.loads(response.text)  # str to dict
                if text.get("value") == 1.0:
                    self.register[int(reg_number) - 101] = 'HIGH'
                elif text.get("value") == 0.0:
                    self.register[int(reg_number) - 101] = 'LOW'
            except:
                self.register[i - 101] = 'LOW'

    def set_register(self, reg_number):

        if self.register[int(reg_number) - 101] == 'LOW':
            reg_value = 1.0
        elif self.register[int(reg_number) - 101] == 'HIGH':
            reg_value = 0.0

        try:
            url = f"http://{self.robot_ip}/api/v2.0.0/registers/{reg_number}"
            data = {"value": reg_value, "label": "MiR Sniffer"}
            headers = {
                'Content-Type': "application/json",
                'authorization': "Basic YWRtaW46OGM2OTc2ZTViNTQxMDQxNWJkZTkwOGJkNGRlZTE1ZGZiMTY3YTljODczZmM0YmI4YTgxZjZmMmFiNDQ4YTkxOA==",
                'Cache-Control': "no-cache",
                'Postman-Token': "bfcd7159-1d12-5b7f-468f-d5e096709cbd"
            }
            response = requests.put(url, data=json.dumps(data), headers=headers)
            text = json.loads(response.text)  # str to dict
            # self.register[int(reg_number)-101] = str(text.get("value"))
            if text.get("value") == 1.0:
                self.register[int(reg_number) - 101] = 'HIGH'
            elif text.get("value") == 0.0:
                self.register[int(reg_number) - 101] = 'LOW'

        except:
            pass

    def change_button_color(self, reg_number):
        if self.register[int(reg_number) - 101] == 'HIGH':
            self.button_colors[int(reg_number) - 101] = [1, 1, 1, 1]
        elif self.register[int(reg_number) - 101] == 'LOW':
            self.button_colors[int(reg_number) - 101] = [0.3, 0.9, 0.1, 1]


class Mir327(Screen):
    robot_ip = StringProperty('10.173.175.118')
    robot_status = StringProperty('Not accessible.')
    battery_per = StringProperty('Not accessible.')
    battery_time = StringProperty('Not accessible.')
    error_description = StringProperty('Not accessible.')
    mission_text = StringProperty('Not accessible.')
    mission_id = StringProperty('Not accessible.')
    register = ListProperty(['LOW', 'LOW', 'LOW', 'LOW'])
    button_colors = ListProperty([[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]])

    def __init__(self, **kwargs):
        super(Mir327, self).__init__(**kwargs)
        Clock.schedule_once(self.change_robot_status, -1)
        Clock.schedule_interval(self.change_robot_status, 30)

    def change_robot_status(self, *args):
        try:
            url = f"http://{self.robot_ip}/api/v2.0.0/status"

            headers = {
                'Content-Type': "application/json",
                'authorization': "Basic YWRtaW46OGM2OTc2ZTViNTQxMDQxNWJkZTkwOGJkNGRlZTE1ZGZiMTY3YTljODczZmM0YmI4YTgxZjZmMmFiNDQ4YTkxOA==",
                'Cache-Control': "no-cache",
                'Postman-Token': "bfcd7159-1d12-5b7f-468f-d5e096709cbd"
            }

            response = requests.request("GET", url, headers=headers, timeout=.5)
            text = json.loads(response.text)  # str to dict
            self.robot_status = text.get("state_text")
            self.battery_per = str(text.get("battery_percentage"))
            self.battery_per = self.battery_per[:4]
            self.battery_time = str(text.get("battery_time_remaining"))
            # self.error_description = text['errors']['description']
            self.mission_text = text.get('mission_text')
            self.mission_id = str(text.get('mission_queue_id'))
        except:
            self.robot_status = 'Not accessible'
            self.battery_per = 'Not accessible'
            self.battery_time = 'Not accessible'
            self.error_description = 'Not accessible'
            self.mission_text = 'Not accessible'
            self.mission_id = 'Not accessible'

    def check_registers(self, *args):
        for i in range(101, 105):
            try:
                url = f"http://{self.robot_ip}/api/v2.0.0/registers/{i}"
                headers = {
                    'Content-Type': "application/json",
                    'authorization': "Basic YWRtaW46OGM2OTc2ZTViNTQxMDQxNWJkZTkwOGJkNGRlZTE1ZGZiMTY3YTljODczZmM0YmI4YTgxZjZmMmFiNDQ4YTkxOA==",
                    'Cache-Control': "no-cache",
                    'Postman-Token': "0db92846-36d7-ab5e-b336-1fafd9a409a3"
                }
                response = requests.request("GET", url, headers=headers, timeout=.5)
                text = json.loads(response.text)  # str to dict
                if text.get("value") == 1.0:
                    self.register[int(reg_number) - 101] = 'HIGH'
                elif text.get("value") == 0.0:
                    self.register[int(reg_number) - 101] = 'LOW'
            except:
                self.register[i - 101] = 'LOW'

    def set_register(self, reg_number):

        if self.register[int(reg_number) - 101] == 'LOW':
            reg_value = 1.0
        elif self.register[int(reg_number) - 101] == 'HIGH':
            reg_value = 0.0

        try:
            url = f"http://{self.robot_ip}/api/v2.0.0/registers/{reg_number}"
            data = {"value": reg_value, "label": "MiR Sniffer"}
            headers = {
                'Content-Type': "application/json",
                'authorization': "Basic YWRtaW46OGM2OTc2ZTViNTQxMDQxNWJkZTkwOGJkNGRlZTE1ZGZiMTY3YTljODczZmM0YmI4YTgxZjZmMmFiNDQ4YTkxOA==",
                'Cache-Control': "no-cache",
                'Postman-Token': "bfcd7159-1d12-5b7f-468f-d5e096709cbd"
            }
            response = requests.put(url, data=json.dumps(data), headers=headers)
            text = json.loads(response.text)  # str to dict
            # self.register[int(reg_number)-101] = str(text.get("value"))
            if text.get("value") == 1.0:
                self.register[int(reg_number) - 101] = 'HIGH'
            elif text.get("value") == 0.0:
                self.register[int(reg_number) - 101] = 'LOW'

        except:
            pass

    def change_button_color(self, reg_number):
        if self.register[int(reg_number) - 101] == 'HIGH':
            self.button_colors[int(reg_number) - 101] = [1, 1, 1, 1]
        elif self.register[int(reg_number) - 101] == 'LOW':
            self.button_colors[int(reg_number) - 101] = [0.3, 0.9, 0.1, 1]


class MainApp(App):
    def build(self):
        return MirSniffer()


# Main
if __name__ == '__main__':
    MainApp().run()
