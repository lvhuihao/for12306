import requests
import re
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9116'
r = requests.get(url, verify=False)  # 提取网页信息，不判断证书
pattern = u'([\u4e00-\u9fa5]+)\|([A-Z]+)'  # 正则表达式提取中文以及大写英文字母
result = re.findall(pattern, r.text)  # 进行所需要的信息的提取
station = dict(result)  # 把所获信息设置为一一对应（有点像是c++里的map）
station_name=list(station.keys())
station_cap=list(station.values())


def getStationCap(name):
    return station_cap[station_name.index(name)]

def getStationName(cap):
    return station_name[station_cap.index(cap)]

