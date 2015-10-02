from transat.simulation import Simulation
from subprocess import call
import os, sys
import time
import json, requests
import math

"""
  Coupling with 1D codes

  This class contains the functions to stop, resotre, and run the coupled simulation and stand alone simulation
  for either 3D or 1D code.
  It contains functions to modify the domain and geometry in 3D and 1D code.
  It contains functions to carry out post-process procedure for either code.
"""


class Coupling(object):
    def __init__(self):
        pass


class Olga1D(Coupling):
    def __init__(self, url):
        super(Olga1D, self).__init__()
        self.url = url

    def simulate(self, till):
        self.setup()
        self.start()
        simu_time = 0
        while simu_time < till:
            time.sleep(1)
            simu_time = self.get('TIME')
            print "simu time " + str(simu_time)
        self.pause()
        return True


    def setup(self):
        params = dict(action='setup')
        resp = requests.get(url=self.url, params=params)
        data = json.loads(resp.text)
        print data

    def start(self):
        params = dict(action='start')
        resp = requests.get(url=self.url, params=params)
        data = json.loads(resp.text)
        print data


    def pause(self):
        params = dict(action='pause')
        resp = requests.get(url=self.url, params=params)
        data = json.loads(resp.text)
        print data

    def get(self, varname, location='None'):
        params = dict(action='get', varname=varname, location=location)
        resp = requests.get(url=self.url, params=params)
        data = json.loads(resp.text)
        return data[varname]

    # mass flow rate of oil GLTHL
    # mass flow rate of water in film GLWT
    def get_velocities(self, location, n):
        velocities = {}
        r = 0.254 / 2
        A = math.pi * pow(r, 2)
        velocities['oil'] = self.get('GLTHL', location)[n] / ( self.get('ROHL', location)[n] * A )
        velocities['water'] = self.get('GLWT', location)[n] / ( self.get('ROWT', location)[n] * A )
        return velocities

    # oil: VISHL
    # water : VISWT
    def get_viscosities(self, location, n):
        viscosities = {}
        viscosities['oil'] = self.get('VISHL', location)[n]
        viscosities['water'] = self.get('VISWT', location)[n]
        return viscosities

    # oil : ROHL
    # water : ROWT
    def get_densities(self, location, n):
        densities = {}
        densities['oil'] = self.get('ROHL', location)[n]
        densities['water'] = self.get('ROWT', location)[n]
        return densities

    def get_pressure(self, location, n):
        return 1  # self.get('bla',location)[n]


class Cathare1D(Simulation):
    def __init__(self, name, filename):
        super(Cathare1D, self).__init__(name)
        self._cathare_input_file = filename

    def execute(self, cmd):
        print cmd
        print self.load_path('local')
        return call(cmd, cwd=self.load_path('local'), shell=True)

    def open_file(self, filename, mode='r'):
        return open(os.path.join(self.load_path('local'), filename), mode)

    def change_configuration(self, item, value):
        self.execute("mv Configuration.txt Configuration.txt.bak")
        fo = self.open_file("Configuration.txt", "a")
        for line in self.open_file("Configuration.txt" + ".bak"):
            if item in line:
                line = item + " " + str(value) + "\n"
            fo.write(line)
        fo.close();
        self.execute("rm Configuration.txt.bak")

    ##Generate a plot for the given file.
    # @param self is the object pointer.
    # @param filename is a file created by cathare post process procedure
    def generate_cathare_plot(self, filename):
        import numpy as np
        import matplotlib.pyplot as plt

        datafile = os.path.join(self.load_path('local'), filename)
        filecontent = np.loadtxt(datafile)
        x = filecontent[:, 0]
        y = filecontent[:, 1]

        lines = []
        for line in self.open_file(filename, "r"):
            lines.append(line)
        xlabel = lines[1].replace("# set xlabel ", "")
        ylabel = lines[2].replace("# set ylabel ", "")
        title = lines[3].replace("# set label 1 ", "")
        plt.rcParams['lines.linewidth'] = 3
        plt.rcParams['font.size'] = 20
        plt.rc('xtick', labelsize=15)
        plt.rc('ytick', labelsize=15)
        plt.figure(figsize=(15, 10))
        plt.plot(x, y, c='r')
        plt.xlabel(unicode(xlabel), fontsize=15)
        plt.ylabel(unicode(ylabel, errors='ignore'), fontsize=15)
        plt.title(unicode(title), fontsize=15)
        plt.grid("on")
        filename = datafile.replace(".evol", "")
        plt.tight_layout()
        plt.savefig(filename + ".png")

        ##Check if the item which a user wants to add already exists.

    # @param self     is the object pointer.
    # @param filename is the name of the file to be checked.
    # @param item     is the item to be checked.
    # @return True when item exists, False otherwise.
    def item_existence(self, filename, item):
        for line in self.open_file(filename):
            if item in line:
                print "The item '" + item + "' you want to add already exists. If you don't interrupt me, I will continue without changing anything in " + filename
                from time import sleep

                sleep(5)
                return True
        return False

    ##Insert one or several lines into a file.
    # @param self      is the object pointer.
    # @param filename  is the file to be used.
    # @param new_lines is the new lines to be inserted.
    # @param trigger   is the sign to insert. New_lines will be inserted before the line contains trigger.   
    def insert_line_to_cathare_file(self, filename, new_lines, trigger):
        self.execute("mv " + filename + " " + filename + ".bak")
        fo = self.open_file(filename, "a")
        for line in self.open_file(filename + ".bak"):
            if trigger in line:
                for new_line in new_lines:
                    fo.write(new_line + "\n")
            fo.write(line)
        fo.close();
        self.execute("rm " + filename + ".bak")


    ##Add a water injection point to an element.
    # @param self      is the object pointer.
    # @param order     is the order number of the new injection point.
    # @param element   is the element which the new injection is attached to.
    # @param position  is the location of the new injection point on that element.
    # @param elevation is the elevation of the new injection point compared to the element(between 0.0 and 1.0).
    # @param area      is the cross section area of the new injection point.
    def add_injection_point(self, order, element, position, elevation, area):
        import os, sys

        if not os.path.isfile(os.path.join(self.load_path('local'), self._cathare_input_file)):
            ss = self._cathare_input_file + " does not exist! Please check the name of the CATHARE input file!"
            sys.exit(ss)

        if not self.item_existence(self._cathare_input_file, "INJECT" + str(order)):
            new_lines = []
            new_lines.append("IP" + str(order) + " = " + "SCALAR " + element + " " + str(position) + ";")
            new_lines.append(
                "INJECT" + str(order) + " = PIQREV AXIAL " + element + " EXTERNAL IP" + str(order) + "\n ELEV " + str(
                    elevation) + " SECT " + str(area) + " PERPENDI ;")
            self.insert_line_to_cathare_file(self._cathare_input_file, new_lines, "END DATA")

    ##Initialize a new injection point.
    # @param self        is the object pointer.
    # @param order       is the order number of the injection point to be initialized.
    # @param totflow     is the initial mass flow rate via this injection point.
    # @param temperature is the initial temperature of the fluid through this injection point.
    def init_injection_point(self, order, totflow, temperature):
        if not os.path.isfile(os.path.join(self.load_path('local'), self._cathare_input_file)):
            ss = self._cathare_input_file + " does not exist! Please check the name of the CATHARE input file!"
            sys.exit(ss)

        if not self.item_existence(self._cathare_input_file, "ENABLE INJECT" + str(order)):
            new_lines = []
            new_lines.append("WRITE " + str(totflow) + " TOTFLOW INJECT" + str(order) + ";")
            new_lines.append("WRITE " + str(temperature) + " TLIQEXT INJECT" + str(order) + ";")
            new_lines.append("WRITE 1.0D-5 OVERHEAT " + "INJECT" + str(order) + ";")
            new_lines.append("WRITE 1.0D-5 ALFAEXT " + "INJECT" + str(order) + ";")
            new_lines.append("ENABLE INJECT" + str(order) + ";")
            self.insert_line_to_cathare_file(self._cathare_input_file, new_lines, "GOPERM")


    ##Write a file containing mass flux and temperature colleted from TransAT for injection points.
    # @param self        is the object pointer.
    # @param massflux    is the massflux collected from TransAT.
    # @param temperature is the temperature collected from TransAT
    def injection_to_1D(self, massflux, temperature):
        if not len(massflux) == len(temperature):
            import sys

            sys.exit("ERROR: The number of mass flux doesn't match with that of temperature!")
        fo = self.open_file("INJECTION.txt", "w")
        fo.close()
        fo = self.open_file("INJECTION.txt", "a")
        for index in range(len(massflux)):
            fo.write(str(massflux[index]) + "\t" + str(temperature[index]) + "\n")
        fo.close

    ##Run CATHARE solver for a coupled simulation by using ICoCo.
    # @param self is the object pointer.
    def run_cathare_controller(self):
        fo = self.open_file("run.sh", "w")
        fo.close()
        fo = self.open_file("run.sh", "a")
        fo.write("#!/bin/sh" + "\n\n")
        fo.write("make -f $v25_3/ICoCo/Makefile_gad fullclean " + "\n\n")
        fo.write("DATAFILE=" + self._cathare_input_file + " make -f $v25_3/ICoCo/Makefile_gad" + "\n\n")
        fo.write("./superv" + "\n")
        fo.close()
        self.execute("chmod 777 run.sh")
        if self.execute("./run.sh") != 0:
            sys.exit("ERROR: Cathare solver is stopped due to some error.")

    ##Run CATHARE solver by using ICoCo starting from a state restored from a previous simulation.
    # @param self is the object pointer.
    def restore_cathare(self, restore_label, restore_method):
        fo = self.open_file("run.sh", "w")
        fo.close()
        fo = self.open_file("run.sh", "a")
        fo.write("#!/bin/sh" + "\n\n")
        fo.write("make -f $v25_3/ICoCo/Makefile_gad fullclean " + "\n\n")
        fo.write("DATAFILE=" + self._cathare_input_file + " make -f $v25_3/ICoCo/Makefile_gad" + "\n\n")
        fo.write("./superv" + "\n")
        fo.close()


    ##Run CATHARE stand alone simulation.
    # @param self is the object pointer.
    def run_cathare_alone(self):
        if not os.path.isfile(self._cathare_input_file):
            ss = "The filename " + self._cathare_input_file + " does not exist! Please check your input file!"
            sys.exit(ss)
        else:
            if self.execute("./read.unix " + self._cathare_input_file) != 0:
                sys.exit("ERROR: Reading is interupted. Please check reader.out and your input data file.")
            else:
                ff = self._cathare_input_file.replace(".dat", "")
                filename = self.load_path('local') + "PILOT_" + ff + ".f"
                if os.path.isfile(filename):
                    try:
                        os.remove(filename)
                    except OSError:
                        pass
                if self.execute("./cathar.unix " + ff + ".list") != 0:
                    sys.exit(
                        "ERROR: Unable to start CATHARE solver or abnormal stop of calculation. Please check the output file " + ff + ".list")

    ##Create a post process input file or add line into it.
    # @param self     is the object pointer.
    # @param method decides the post process extrats data for time evolution or a spatial profile("CHRONO" or "PHOTO" ). 
    # @param name     is the name of the output file of post process.
    # @param element  is the element which the user wants to check.
    # @param variable is the variable which the user wants to check.
    # @param mark     is time instance for "PHOTO" method and position for "CHRONO" method.
    def create_cathare_postpro_file(self, method, name, element, variable, mark):
        ss = []
        if method == "PHOTO":
            ss.append(name + " = " + method + " " + element + " " + variable + " " + str(mark) + ";")
        elif method == "CHRONO":
            ss.append(name + " = " + method + " " + element + " " + variable + " " + "ELEV " + str(mark) + ";")
        else:
            sys.exit("ERROR: method name is not correct!")

        filename = "postpro.dat"
        if not os.path.isfile(os.path.join(self.load_path('local'), filename)):
            fo = self.open_file(filename, "a")
            fo.write("GNUPLOT ALL;\n")
            fo.write("READ RESULT 21;\n")
            fo.write(ss[0] + "\n")
            fo.write("END ;\n")
            fo.close()
        else:
            if not self.item_existence(filename, name + " = "):
                self.insert_line_to_cathare_file(filename, ss, "END")

    ##Run CATHARE post process procedure.
    # @param self is the object pointer.
    def run_cathare_post_process(self):
        self.execute("./postpro.unix postpro.dat")

    ##Obtain the spatial profile for a variable along an element at a time instance or
    # obtain the time evolution for a variable at a location on an element.
    # @param self     is the object pointer.
    # @param method   is the method to present data. "PHOTO" for spatial profile; "CHRONO" for time evolution.
    # @param element  is the element which the user wants to check.
    # @param variable is the variable which the user wants to check.
    # @param mark     is time instance for "PHOTO" method and position for "CHRONO" method.
    def get_cathare_global(self, method, element, variable, mark):
        filename = os.path.join(self.load_path('local'), "postpro.dat")
        if os.path.isfile(filename):
            self.execute("mv postpro.dat postpro.dat.backup")
        self.create_cathare_postpro_file(method, "PROF", element, variable, mark)
        self.run_cathare_post_process()
        title = element + "_" + variable + "_" + str(mark) + "_" + method + ".evol"
        self.execute("mv PROF.evol " + title)
        self.generate_cathare_plot(title)
        self.execute("mv postpro.dat.backup postpro.dat")

    ##Obtain the local value for a variable at a location on an element at a time instance.
    # @param self     is the object pointer.
    # @param element  is the element which the user wants to check.
    # @param variable is the variable which the user wants to check.
    # @param tim      is the time which the user wants to check. 
    def get_cathare_local(self, element, variable, location, time):
        filename = os.path.join(self.load_path('local'), "postpro.dat")
        if os.path.isfile(filename):
            self.execute("mv postpro.dat postpro.dat.backup")
        self.create_cathare_postpro_file("PHOTO", "PROF", element, variable, time)
        self.run_cathare_post_process()

        import numpy as py

        datafile = os.path.join(self.load_path('local'), "PROF.evol")
        filecontent = py.loadtxt(datafile)
        x = filecontent[:, 0]
        y = filecontent[:, 1]

        self.execute("rm PROF.evol")
        self.execute("mv postpro.dat.backup postpro.dat")

        index = 0
        for index in range(len(x)):
            if location == x[index]:
                return y[index]
            elif location < x[index]:
                break
            else:
                pass

        if index == 0:
            result = y[0] + (location - x[0]) * (y[1] - y[0]) / (x[1] - x[0])
        else:
            result = y[index] + (location - x[index]) * (y[index - 1] - y[index]) / (x[index - 1] - x[index])
        return result


"""

private:
  std::string _1D_code_name                   //!< The name of the 1D code which is conntected to TransAT.
  std::vector<std::string> _coupling_boundary_id                    //!< The id of the coupling boundary
public:

  /**
   *brief This function tells TransAT which code is connected to which boundary
   *param boundary_id  is a number identifying a coupling boundary
   *param 1D_code_name is the name of the 1D code connected to the corresponding boundary
   **/
  void select_1D(std::string boundary_id, std::string 1D_code_name);

   /**
    *brief This function changes the domain in TransAT via modifying the TransAT input file.
    *param filename is the name of the TransAT input file. Here it is .stt file.
    *param new_domain is the new domain(including three dimensions, each dimension has two limits).
   **/
   void modify_transat_domain(std::string filename, std::vector<std::vector <double> > new_domain);

   /**
    *brief This function changes the geometry in CATHARE via modifying the CATHARE input file.
    *param filename is the name the CATHARE input file.
    *param name is the name of the element whose geometry is to be changed.
   **/
   void modify_cathare_geometry(std::string filename, std::string name);

   /**
    *brief This function changes the boundary conditions in TransAT via modifying the TransAT input file.
    *param filename is the name of the TransAT input file. Here it is .bc file.
   **/
   void modify_transat_boundaries(std::string filename);

   /**
    *brief This function changes the boundary conditions in CATHARE via modifying the CATHARE input file.
    *param filename is the name the CATHARE input file.
    *param name is the name of the boundary object whose setting is to be changed.
   **/
   void modify_cathare_boundaries(std::string filename, std::string name);

   /**
    *brief This function changes the boundary conditions in TransAT via modifying the TransAT input file.
    *param filename is the name of the TransAT input file. Here it is transat_mb.inp file.
   **/
   void modify_transat_control_parameters(std::string filename);

  /**
   *brief This function activates/de-activates the turbulence model in TransAT based on action.
   *param action is yes to activate and no to de-activate.
  **/
  void activate_transat_turbulence_model(bool action);

  /**
   *brief This function activates/de-activates the multiphase model in TransAT based on action.
   *param action is yes to activate and no to de-activate.
  **/
  void activate_transat_multiphase_model(bool action);

  /**
   *brief This function activates/de-activates the drift model in TransAT based on action.
   *param action is yes to activate and no to de-activate.
  **/
  void activate_transat_drift_model(bool action);

  /**
   *brief This function activates/de-activates the axisymmetry model in TransAT based on action.
   *param action is yes to activate and no to de-activate.
  **/
  void activate_transat_axisymmetry(bool action);

  /**
   *brief This function modifies the phase properties in TransAT.
   *param nphases is the number of phases in this simulation.
  **/
  void modify_transat_phase_properites(double nphases);

  /**
   *brief This function generates the files needed for simulation based on input files.
   *param filename1 is the name of the .stt file.
   *param filename2 is transat_mb.inp.
  **/
  void prepare_transat_simulation(std::string filename1, std::string filename2);

  void stop_transat();
  void stop_cathare();

  void run_transat_coupled();

  /**
   *brief The function starts CATHARE solver for a coupled simulation.
   *param cathare_input_file is the input data file for CATHARE.
  **/
  void run_cathare_coupled(std::string cathare_input_file);

  void run_transat_alone();

  /**
   *brief The function starts CATHARE solver for a CATHARE stand alone simulation.
   *param cathare_input_file is the input data file for CATHARE.
  **/
  void run_cathare_alone(std::string cathare_input_file);

  void restore_transat();
  void restore_cathare();

  /**
   *brief The function writes a line into "postpro.dat" for time evolution of a particular variable.
   *param method   is the method of post process, either "PHOTO" for spatial profile or "CHORONO" for time evolution.
   *param name     is the name of the output file generated by the post-process procedure, which will be in the form of "name.evol".
   *param variable is the name of the variable of which the user wants to extract information.
   *param element  is the name of the object where the user wants to check.
   *param mark     is the position or the time where the user wants to check.
  **/
  void create_cathare_postpro_file(std::string method, std::string name, std::string variable, std::string element, double mark);

  void post_process_transat();
  void post_process_cathare();

  /**
   *brief The function creates the configuration file for TransAT's controller and provides the essential information.
   *param 1D_pipe_diameter is the pipe diameter specified in 1D code.
   *param time_stepping_tolerance is used to check if two codes have synchronized.
   *param pressure_coupling_tolerance is the the tolerance used to decide whether the coupling constran has reached.
   *param mass_flux_tolerance is the constrain for mass flux.
   *param velocity_tolerance is the constrain for velocity.
  **/
  void configuration_for_transat( double 1D_pipe_diameter, double time_stepping_tolerance, double pressure_coupling_tolerance, double mass_flux_tolerance, double velocity_tolerance);


  void configuration_for_olga();

  /**
   *brief The function creates the configuration file for CATHARE's coupling controller and provides the essential information.
   *param element is name of the element where coupling interface is located. Currently it is one of the boundary objects in CATHARE.
   *param RADCHEMI is to specify whether radiochemical component is activated. True for simulation with tracer.
   *param time_stepping_tolerance is time tolerance to determine whether CATHARE has reached the same time in TransAT.
   *param tmax is maximum time for the simulation.
   *param filename_T is name of TransAT output file.
   *param filename_C is name of CATHARE output file.
   *param DENL is density of liquid phase in TransAT. (not necessary when RADCHEMI is true)
   *param DENG is density of gas phase in TransAT.(not necessary when RADCHEMI is true)
   *param restore is to determine whether the simulations needs a restart. True when simulation needs to restart.
   *param restore_label is number of the restored data file. It is also required for the saving procedure.
   *param restore_method is to specify the data file is saved and/or restored from memory or disk.
  **/
  void configuration_for_cathare(std::string element, bool RADCHEMI, double time_stepping_tolerance, double tmax, std::string filename_T, std::string filename_C, double DENL, double DENG, bool restore, int restore_label, std::string restore_method);
}

"""
