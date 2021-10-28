import bisect
import datetime
import json
import urllib.request

class DingDingRobot:
    def __init__(self, robot_id):
        self.url = "https://oapi.dingtalk.com/robot/send?access_token=" + robot_id
        self.headers = {'Content-Type': 'application/json'}
    
    def send(self, msg):
        data = {
            'msgtype': 'text',
            'text': {
                'content': msg
            }
        }
        json_data = json.dumps(data).encode('utf-8')
        request = urllib.request.Request(self.url, 
                                         headers=self.headers, 
                                         data=json_data)
        response = urllib.request.urlopen(request)
        return response

# if __name__ == '__main__':
#     now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
#     robot_id = '9b6d23422bf3aab35a20040a87cf08b402bed8ef3cc189c1137de13fa6bb0eaf'
#     robot = DingDingRobot(robot_id)
#     response = robot.send(f'测试行情 {now}')
