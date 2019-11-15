# coding=utf-8
import getStation
import urllib
import json
import requests
from prettytable import PrettyTable
from operator import itemgetter

def getTrains(fromStation,toStation,date):
    ##需要测试提取的数据是否正确
    ##增加对二等座和无座是有有票买的检查判断
    # fromStation="广州"
    # toStation="北京"
    # date="2019-11-20"
    fromStationCap=getStation.getStationCap(fromStation)
    toStationCap=getStation.getStationCap(toStation)
    url=("https://kyfw.12306.cn/otn/leftTicket/query?"
         "leftTicketDTO.train_date={0}&"
         "leftTicketDTO.from_station={1}"
         "&leftTicketDTO.to_station={2}"
         "&purpose_codes=ADULT").format(date,fromStationCap,toStationCap)
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko)"
                      " Chrome/58.0.3029.110 Safari/537.36"
    }
    # print(url)

    r2 = requests.get(
        "https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc&fs=%E5%B9%BF%E5%B7%9E,GZQ&ts=%E5%8D%97%E5%A4%B4,NOQ&date=2019-10-19&flag=N,N,Y")#获取一个cookies
    r=requests.get(url,headers=headers,cookies=r2.cookies)
    raw_trains=r.json()["data"]["result"]
    # print(r.json()["data"]["result"])
    # raw_trains=r.json()["data"]["result"]
    # print(raw_trains)

    pt = PrettyTable()
    pt._set_field_names('车次 车站 时间 历时 商务座 一等座 二等座 动卧 软卧 硬卧 硬座 无座'.split())
    #到站时间 经历时间 二等座 无座
    # dataIndex={"车次":4,"出发站":5,"终止站":6,"出发时间":9,"到站时间":10,"经历时间":11,"二等座":,"无座"}
    trains = []
    # print("出发站" + "\t" + "终止站" + "\t" + "出发时间" + "\t" + "到站时间" + "\t" + "经历时间" + "\t" + "二等座" + "\t" + "无座")
    for raw_train in raw_trains:
        data_list=raw_train.split("|")
        # print(len(data_list))
        from_station_code = data_list[6]
        to_station_code = data_list[7]
        from_station_name = getStation.getStationName(from_station_code)
        to_station_name = getStation.getStationName(to_station_code)
        start_time = data_list[8]
        arrive_time = data_list[9]
        time_duration = data_list[10]
        business_seat = data_list[32] or '--'
        first_class_seat = data_list[31] or '--'
        second_class_seat = data_list[30] or '--'
        pneumatic_sleep = data_list[33] or '--'
        soft_sleep = data_list[23] or '--'
        hard_sleep = data_list[28] or '--'
        hard_seat = data_list[29] or '--'
        no_seat = data_list[26] or '--'
        if  fromStation not in from_station_name or  toStation not in to_station_name:
            continue

        # print(from_station_name+"\t"+to_station_name+"\t"+start_time+"\t"+arrive_time+"\t"+time_duration+"\t"+second_class_seat+"\t"+no_seat)


        eachTrain = {}
        eachTrain["from_station_name"]=from_station_name
        eachTrain["to_station_name"]=to_station_name
        eachTrain["start_time"]=start_time
        eachTrain["arrive_time"]=arrive_time
        eachTrain["time_duration"]=time_duration
        eachTrain["second_class_seat"]=second_class_seat
        eachTrain["no_seat"]=no_seat
        print(eachTrain)
        trains.append(eachTrain)
    return trains

def arrangeTrains():
    firstTrains = getTrains("虎门", "广州", "2019-11-17")
    secondTrains = getTrains("广州", "容桂", "2019-11-17")
    print("虎门"+"\t"+"广州"+"\t\t"+"广州"+"\t"+"南头")
    allTrains=[]
    for index in range(len(firstTrains)):
        temp=(1,index,firstTrains[index]["arrive_time"])
        allTrains.append(temp)
    for index in range(len(secondTrains)):
        temp=(2,index,secondTrains[index]["start_time"])
        allTrains.append(temp)
    allTrains.sort(key=itemgetter(2))
    for item in allTrains:
        if item[0]==1:
            startTime=firstTrains[item[1]]["start_time"]
            arriveTime=firstTrains[item[1]]["arrive_time"]
            print(startTime+"\t"+arriveTime)
        if item[0]==2:
            startTime=secondTrains[item[1]]["start_time"]
            arriveTime=secondTrains[item[1]]["arrive_time"]
            print("\t\t\t\t"+startTime+"\t"+arriveTime)

arrangeTrains()
