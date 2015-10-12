import transat.setup.stt_helper_functions as stt
import os
import copy
import sys
"""

"""
object_template = """\
FILE  cylinder2.stl
  scale  1
  quickadd  0
  close_option  0
  thick  0
  PARTNAME  cylinder21
   close_option  0
   length  0
   area   0
   volume  0
   minimal_x  -4.993583
   maximal_x  4.993583
   minimal_y  0
   maximal_y  50
   minimal_z  -5
   maximal_z  5
   density      8000
   roughness      1e-08
   max_bmr_level   9
   enable_bmr   1
   obj_visible  1
   capacity     500
   conductivity  16.2
   heatsource   0
   critical_temp inf
   temp_model_choice 1
   temp_value 0
   conc_model_choice 1
   conc_value 0
   film_thickness 0
   surface_coverage 0
   porosity 0
   pore_size 0
   forchcoef 0
   contact_angle 90
   diffusion_coefficient 0
   viscosity -1
  ENDPARTNAME
ENDFILE
"""
object_template = [a + "\n" for a in object_template.rstrip().split('\n')]

class ImmersedSurfaces(object):
    def __init__(self, stt_data):
        self.objects = []
        if "FILE" in stt_data:
            if isinstance(stt_data['FILE'], list):
                for object in stt_data['FILE']:
                    self.objects.append( IST( "part_name", object) )
            else:
                self.objects.append( IST( "part_name", stt_data['FILE']) )


    def read_objects(self):
        raw_objects = stt.get_section("FILE", self.stt_file)
        for object in raw_objects:
            name = stt.get_attribute_value(object, "FILE")
            self.objects.append(IST(name, object))
        stt.remove_section("FILE", self.stt_file)

    def write(self, stt_file):
        data = [object.raw for object in self.objects]
        stt.write_section("FILE", data, stt_file)

    def get_names(self):
        return [obj.name for obj in self.objects]

    def add(self, names):
        if not isinstance(names, list):
            print "add IST take a list as input"
            sys.exit()

        for name in names:
            template = copy.deepcopy(object_template)
            template = stt.auto_parser(template)['FILE']
            ist = IST(name, template)
            ist.change_value('filename', name)
            self.objects.append(ist)

    def get(self, name):
        for obj in self.objects:
            if obj.name == name:
                return obj


class IST(object):
    def __init__(self, name, raw):
        self.name = name
        self.raw = raw

    def change_value(self, key, value):
        self.raw[key] = value

