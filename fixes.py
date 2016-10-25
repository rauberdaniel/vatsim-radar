#!/usr/bin/env python3

import json
import re
from mapbox import Datasets

datasets = Datasets()
datasetID = 'ciuhdymvv00rf2zl7rzxve766'

f = open('raw/fixes.json', 'r')
j = json.load(f)
f.close()

startWithId = 2200

fixes = {}

for name, arr in j.items():
  for fix in arr:
    fixes[fix.get('id')] = fix


fixesgj = {
  "type": "FeatureCollection",
  "features": []
}
for d, fix in fixes.items():
  if(d<startWithId):
    continue
  id = str(fix.get('id'))
  feature = {
    "type": "Feature",
    "id": id,
    "geometry": {
      "type": "Point",
      "coordinates": [fix.get('lon'), fix.get('lat')]
    },
    "properties": {
      "name": fix.get('label'),
      "id": fix.get('id')
    }
  }
  #fixesgj['features'].append(feature)
  resp = datasets.update_feature(datasetID, id, feature)
  if resp.status_code != 200:
    print(resp.json())
    break
  else:
    print("%s %s" % (resp.status_code, id))

fi = open('raw/fixes.geojson', 'w')
fi.write(json.dumps(fixesgj))
fi.close()
