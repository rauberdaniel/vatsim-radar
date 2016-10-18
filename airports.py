import json
import re

f = open('raw/airports.json', 'r')
j = json.load(f)
f.close()

airports = {}

airportPattern = '[A-Z]{4}'
airportRegex = re.compile(airportPattern)

for name, obj in j.items():
  if airportRegex.fullmatch(name):
    obj = obj[0]
    obj['id'] = obj.get('label')[0:4]
    obj['label'] = obj['label'][7:]
    airports[name] = obj

#print(airports)

f = open('airports.json', 'w')
f.write(json.dumps(airports))
f.close()
