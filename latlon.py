#!/usr/bin/env python3

import json
import re
from mapbox import Datasets

datasets = Datasets()
datasetID = 'ciuoufm6l01ch2yp4nzm3tjtb'

for lat in range(-90, 100, 10):
  id = "lat%d" % (lat)
  feature = {
    "type": "Feature",
    "id": id,
    "geometry": {
      "type": "LineString",
      "coordinates": [[-180, lat], [180, lat]]
    },
    "properties": {
      "name": "%d" % lat,
      "id": id
    }
  }
  resp = datasets.update_feature(datasetID, id, feature)
  print(id)

for lon in range(-180, 190, 10):
  id = "lon%d" % (lon)
  feature = {
    "type": "Feature",
    "id": id,
    "geometry": {
      "type": "LineString",
      "coordinates": [[lon, -90], [lon, 90]]
    },
    "properties": {
      "name": "%d" % lon,
      "id": id
    }
  }
  resp = datasets.update_feature(datasetID, id, feature)
  print(id)
