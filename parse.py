#!/usr/bin/env python3

import requests
import json
import sched, time
from datetime import datetime
import os

dataUrl = "http://info.vroute.net/vatsim-data.txt"
clientInfo = ["callsign","cid","realname","clienttype","frequency","latitude","longitude","altitude","groundspeed","planned_aircraft","planned_tascruise","planned_depairport","planned_altitude","planned_destairport","server","protrevision","rating","transponder","facilitytype","visualrange","planned_revision","planned_flighttype","planned_deptime","planned_actdeptime","planned_hrsenroute","planned_minenroute","planned_hrsfuel","planned_minfuel","planned_altairport","planned_remarks","planned_route","planned_depairport_lat","planned_depairport_lon","planned_destairport_lat","planned_destairport_lon","atis_message","time_last_atis_received","time_logon","heading","QNH_iHg","QNH_Mb"]

dir_path = os.path.dirname(os.path.realpath(__file__))

s = sched.scheduler()

def update():
  print('updating…')
  r = requests.get(dataUrl)

  print('received data. parsing…')
  data = r.text.split("\n")

  dt_string = data[0][13:36]
  dt = datetime.strptime(dt_string, "%d/%m/%Y %H:%M:%S %Z")
  timestamp = int(dt.timestamp())

  # find the clients
  clients = []
  index = data.index("!CLIENTS:") + 1
  while data[index] != ";":
    clientData = data[index].split(":")
    clientData.pop()
    if clientData[3] == "PILOT":
      clientData[5] = float(clientData[5]) if clientData[5] != "" else "" # latitude
      clientData[6] = float(clientData[6]) if clientData[6] != "" else "" # longitude
      clientData[7] = float(clientData[7]) if clientData[7] != "" else "" # altitude
      clientData[8] = float(clientData[8]) if clientData[8] != "" else "" # groundspeed
      clientData[38] = float(clientData[38]) if clientData[38] != "" else "" # heading
    zipped = zip(clientInfo, clientData)
    dic = {key: value for key, value in zipped}
    clients.append(dic)
    index = index+1

  atcs = [x for x in clients if x.get('clienttype') == 'ATC' and x.get('callsign')[-4:] != '_OBS' ]
  pilots = [x for x in clients if x.get('clienttype') == 'PILOT' ]

  print('parsed. writing…')
  jsonFile = open(dir_path + '/pilots.json', 'w')
  jsonFile.write(json.dumps({'timestamp': timestamp, 'data': pilots}, indent=2))
  jsonFile.close()

  jsonFile = open(dir_path + '/atc.json', 'w')
  jsonFile.write(json.dumps({'timestamp': timestamp, 'data': atcs}, indent=2))
  jsonFile.close()

  print('done.')
  s.enter(60, 1, update)


s.enter(1, 1, update)
s.run()
