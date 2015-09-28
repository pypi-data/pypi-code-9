from cStringIO import StringIO
import xml.etree.cElementTree as ET
from LatLon import string2latlon


class Kml(object):
    route = None

    def __init__(self, route):
        self.route = route

    def kml(self, filename=None, route_name="Unnamed Route", route_description=""):
        kml = ET.Element("kml")
        doc = ET.SubElement(kml, "Document")

        ET.SubElement(doc, "name").text = route_name
        ET.SubElement(doc, "description").text = route_description

        style = ET.SubElement(doc, "Style", id="yellowLineGreenPoly")
        linestyle = ET.SubElement(style, "LineStyle")
        ET.SubElement(linestyle, "color").text = '7f00ffff'
        ET.SubElement(linestyle, "width").text = '4'
        polystyle = ET.SubElement(style, "PolyStyle")
        ET.SubElement(polystyle, "color").text = '7f00ff00'

        placemark = ET.SubElement(doc, "Placemark")
        ET.SubElement(placemark, "name").text = '%s Flightpath' % route_name
        ET.SubElement(placemark, "description").text = route_description
        ET.SubElement(placemark, "styleUrl").text = '#yellowLineGreenPoly'
        linestring = ET.SubElement(placemark, "LineString")
        ET.SubElement(linestring, "extrude").text = '1'
        ET.SubElement(linestring, "tessellate").text = '1'
        ET.SubElement(linestring, "altitudeMode").text = 'absolute'
        ET.SubElement(linestring, "coordinates").text = self._kmlcoordinates()

        tree = ET.ElementTree(kml)

        if filename:
            return tree.write(filename)

        x = StringIO()
        tree.write(x)
        return x.getvalue()

    def _kmlcoordinates(self):
        y = []
        for r in self.route:
            x = string2latlon(r[1], r[2], 'H% %d% %m% %S')
            x.name = r[0]
            y.append(",".join([str(x.lon),str(x.lat),str(r[3])]))
        return "\n".join(y)

if __name__ == '__main__':
    route = []
    route.append(("LSZI", "N 47 30 32.00", "E 007 57 00.00", 5000))
    route.append(("WIL 116.9", "N 47 10 41.90", "E 007 54 21.30", 5000))
    route.append(("Spiez", "N 46 40 41.99", "E 007 41 26.68", 5000))
    route.append(("Gemmipass", "N 46 23 53.93", "E 007 36 50.98", 5000))
    route.append(("Leuk", "N 46 19 11.36", "E 007 38 23.24", 5000))
    route.append(("Ayent", "N 46 16 37.75", "E 007 24 40.21", 5000))
    route.append(("Rawil Pass", "N 46 22 57.67", "E 007 26 38.70", 5000))
    route.append(("Sanetsch", "N 46 22 56.85", "E 007 16 29.00", 5000))
    route.append(("Sion W", "N 46 09 55.31", "E 007 12 30.64", 5000))
    route.append(("Gampel", "N 46 18 49.40", "E 007 45 24.34", 5000))
    route.append(("Kippel", "N 46 24 14.68", "E 007 46 07.78", 5000))
    route.append(("waypoint", "N 46 30 47.05", "E 008 01 52.54", 5000))
    route.append(("Grimsel", "N 46 33 47.66", "E 008 21 20.98", 5000))
    route.append(("Innetkirchen", "N 46 42 19.76", "E 008 13 53.12", 5000))
    route.append(("Trubschachen", "N 46 55 27.27", "E 007 50 35.57", 5000))
    route.append(("WIL 116.9", "N 47 10 41.90", "E 007 54 21.30", 5000))
    route.append(("LSZI", "N 47 30 32.00", "E 007 57 00.00", 5000))

    kml = Kml(route)
    kml.kml("/Users/tspycher/Desktop/blubbbbbb.kml")
