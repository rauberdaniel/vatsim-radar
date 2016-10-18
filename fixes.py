import json
import re

f = open('raw/fixes.json', 'r')
j = json.load(f)
f.close()

fixesgj = {
  "type": "FeatureCollection",
  "features": []
}
fixes = {}

fixesPattern = '(I|J)[A-Z]{4}'
fixesRegex = re.compile(fixesPattern)

for name, arr in j.items():
  for fix in arr:
    if fixesRegex.fullmatch(fix.get('label')):
      fixes[fix.get('id')] = fix

for d, fix in fixes.items():
  fixesgj['features'].append({
    "type":"Feature",
    "geometry": {
      "type": "Point",
      "coordinates": [fix.get('lon'), fix.get('lat')]
    },
    "properties": {
      "name": fix.get('label')
    }
  })

f = open('raw/fixes.geojson', 'w')
f.write(json.dumps(fixesgj))
f.close()
