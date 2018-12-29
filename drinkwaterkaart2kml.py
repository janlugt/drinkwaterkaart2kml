import json
import simplekml
import urllib2

response = urllib2.urlopen('https://drinkwaterkaart.nl/waar-kan-ik-gratis-water-tappen/')
html = response.read()
lines = html.splitlines()
locations_line = filter(lambda x:'wpgmaps_localize_marker_data' in x, lines)[0]
# Remove some javascript
locations_line = locations_line.replace('var wpgmaps_localize_marker_data = ', '')
# Remove semicolon
locations_line = locations_line[:-1]
locations = json.loads(locations_line).values()[0].values()
locations.sort(key=lambda x: x['desc'])

kml = simplekml.Kml(name = 'Drinking water locations')

for loc in locations:
  name = loc['desc'].split('</a>')[-1].strip()
  pnt = kml.newpoint(name='<![CDATA[%s]]>' % name)
  coords = loc['address'].split(',')
  pnt.coords = [(coords[1].strip(), coords[0].strip())]

kml.save('drinkwaterkaart.kml')
