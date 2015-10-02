# Utility functions to read paraview files
# To make it work:
# export PYTHONPATH="/server/software/Paraview/ParaView-3.98.1-python/lib:$PYTHONPATH"
#export PYTHONPATH="/server/software/Paraview/ParaView-3.98.1-python/lib/site-packages:$PYTHONPATH"
#  LD_LIBRARY_PATH="/server/software/Paraview/ParaView-3.98.1-python/lib:$LD_LIBRARY_PATH"
import paraview.simple as pa
import numpy as np
import re
import glob as gl
import os


def OpenDataFile(filename):
    data = pa.OpenDataFile(filename)
    pa.UpdatePipeline()
    return data


def convert_to_unstructured(filter, convert_to_point=True):
    threshold = pa.Threshold(filter)
    threshold.Scalars = ['CELLS', 'BMR_I']
    threshold.ThresholdRange = [1.E-9, 1.0]
    dataset = pa.MergeBlocks(threshold)
    if convert_to_point:
        dataset = pa.CellDatatoPointData(dataset)

    return dataset


def rewrite_as_unstructured(filename_in, filename_out):
    data = pa.OpenDataFile(filename_in)
    unstructured = convert_to_unstructured(data)

    pa.UpdatePipeline()
    writer = pa.CreateWriter(filename_out, unstructured)
    writer.UpdatePipeline()


def read_only_certain_var(casename, directory, iteration, nblocks, variables, size_block_string=None,
                          blocklist=None):
    """ This returns a group datasets of all the blocks in blocklist containing only the variables in var
      Parameters:
        casename: project name 
	directory:         project directory (without RESULT)
	iteration:         iteration/timstep zeros will be added when necessary
	nblocks  :         number of blocks. This will load all the blocks from 1 
	                   to nblocks unless blocklist is  specified
	variables:         variables that you want to extract
	size_block_string: Number of digits in the block string. This needs to be specified
	                   only if you don't want to load all the blocks. Otherwise it will be 
			   computed from nblocks
	blocklist:         list of blocks to load. If you don't specify this, blocks 1,blocks are read
   """
    filelist = []
    if not blocklist:
        blocklist = range(1, nblocks + 1)

    for nb in blocklist:
        if not size_block_string:
            size_block_string = int(np.log10(nb) + 1)
        blockstring = str(nb).rjust(size_block_string, '0')
        itstring = str(iteration).rjust(7, '0')

        vtkName = directory + '/RESULT/' + casename + "." + blockstring + "." + itstring + ".vtr"
        reader = pa.XMLRectilinearGridReader(FileName=vtkName)
        reader.PointArrayStatus = variables
        reader.CellArrayStatus = []
        filelist.append(reader)
    datagroup = pa.GroupDatasets(Input=filelist)
    for file in filelist:
        pa.Delete(file)
    return datagroup


def massflow_avg(filter, weight, var, cell=True):
    """
  The function returns integrated variables over filter.
  Additional entries massflow and massflow_t_var are added
  which represent the integrated massflow as defined in weight 
  and integrated massflow*var
  Weight is a list of scalars that will be multiplied to get massflow

  Example usage:
    line is a PlotOverLine filter
    massflow_avg(line,["DEN","U"],"T")
    
   This will calculate a mass flow averaged temperature
   
  """
    var_list = ['massflow', 'massflow_t_' + var]
    names = []
    calc1 = pa.Calculator(filter)
    if cell:
        calc1.AttributeMode = "Cell Data"
    func = "1"
    for weight_var in weight:
        func = func+"*" + weight_var
    calc1.Function = func
    calc1.ResultArrayName = var_list[0]
    names.append(func)
    calc2 = pa.Calculator(calc1)
    if cell:
        calc2.AttributeMode = "Cell Data"
    func = func +"*" +var
    calc2.Function = func
    calc2.ResultArrayName = var_list[1]

    names.append(func)
    integrate = pa.IntegrateVariables(calc2)
    avg_dict = {}
    pa.UpdatePipeline()
    fetch = pa.servermanager.Fetch(integrate)
    for var, name in zip(var_list, names):
        avg_dict[name] = extract_data(integrate, var, fetch, cell=cell)[0]
    avg_dict['Area'] = extract_data(integrate, "Area", fetch, cell=True)[0]
    return avg_dict


def color_by_array(filter, var):
    """
   Render a filter colored by the variable
   name
  """
    dp = pa.GetDisplayProperties(filter)
    dp.ColorArrayName = var
    pa.Show(filter)
    pa.Render()


def extract_data(filter, var, fetch=None, cell=True):
    """
   Extract the data of variable var from filter
   Returns a numpy array
   """

    if fetch:
        data = fetch
    else:
        data = pa.servermanager.Fetch(filter)

    if cell:
        array = data.GetCellData().GetArray(var)
    else:
        array = data.GetPointData().GetArray(var)

    np_array = np.zeros(array.GetDataSize())
    for i in range(array.GetDataSize()):
        np_array[i] = array.GetValue(i)
    return np_array


def save_data_to_dict(filter, cell=False):
    """
  Extract all the data form a filter
  Returns a dictionary of numpy arrays
  """
    data_dict = {}
    pa.UpdatePipeline()
    data = pa.servermanager.Fetch(filter)
    for item, key in filter.PointData.iteritems():
        try:
            data_dict[item.strip()] = extract_data(filter, item, data, cell=cell)
        except:
            pass #print "could not read " + item
    return data_dict


def get_list_of_plot_over_line(filter, point_list):
    """
   creates a list of plot over lines on filter
   Input is a three dimensional list of points
   The first dimension is the line
   The second dimension is the point (1 or 2)
   The third dimension are the coordinate (x,y,z)
   """
    line_list = []
    for line in point_list:
        print line
        pol = pa.PlotOverLine(filter)
        pol.Source.Point1 = line[0]
        pol.Source.Point2 = line[1]

        line_list.append(pol)

    return line_list


def get_iteration(iteration=-1, folder="RESULT", file_ext="vtm"):
    """
    Returns the string of the last filename in a folder with a given extension
   """
    filelist = gl.glob(folder + "/*." + file_ext)
    filelist.sort(key=lambda filename: int(filename.split(".")[1]))

    if iteration == -1:
        return filelist[iteration]
    else:
        for filename in filelist:
            if int(filename.split(".")[1]) == iteration:
                return filename


def get_last_modified(folder="RESULT", file_ext="vtm"):
    """
    Returns the string of the filename that was last modified
    in a folder with a given extension
   """
    try:
        filelist = gl.glob(folder + "/*." + file_ext)
        filelist.sort(key=lambda filename: os.path.getmtime(filename))
        return filelist[-1]
    except:
        print "No results found in folder "+str(folder)+" with file extension "+str(file_ext)
        raise()


def get_all(folder="RESULT", file_ext="vtm"):
    filelist = gl.glob(folder + "/*." + file_ext)
    filelist.sort(key=lambda filename: os.path.getmtime(filename))
    return filelist


def contains_digits(d):
    """ returns True when a string d
       contains digits"""
    digits_re = re.compile('\d')
    return bool(digits_re.search(d))


class file_reader:
    def __init__(self, filename, comment='#'):
        """ Read the file and store its values in self.data
       Read the header and store it as dictionary
       in header_dict """

        self.filename = filename

        # Read file header
        file = open(self.filename)
        idx = 0
        # header_dict maps the string of the header
        # to the column index of the data
        self.header_dict = {}
        for line in file:
            # Simple parser: line has to contain a # and
            # and a digit. Should work
            # for most headers
            if comment in line and contains_digits(line):
                key = line.strip()
                self.header_dict[key] = idx
                idx = idx + 1
        file.close()

        # Read the data (everything that does not start with a #)
        self.data = np.genfromtxt(filename, comments=comment, invalid_raise=False)
        if not len(self.header_dict) == self.data.shape[1]:
            print("something went wrong in parsing the header")
            print("Each Header line should contain digits and start with a #")
            print("Found " + str(len(self.header_dict)) + " lines but data contains " +
                  str(self.data.shape[1]) + " columns")


    def get_column(self, column):
        """ Get a column from self.data based on
          column 
          If column is an integer return the column
          with the corresponding index directly
          Otherwise column is assumed to be regular expression
          that is used to find the index based on the header_dict
          Example usage:
              #You know the column index (10)

              get_column(10)

              #You know that the line you are looking for contains
              # "pressure" and  "x" and you want the last value
              get(".*pressure.*x.*")
      """

        # convert to index that starts at zero
        # If column is an int return the corresponding value directly
        if type(column) == int:
            return self.data[:, column]
        # Assume column is a regular expression
        else:
            pattern = re.compile(column)

            matches = []
            for key, item in self.header_dict.iteritems():
                if pattern.match(key):
                    matches.append([key, item])

            # Exactly one match found; return value
            if len(matches) == 1:
                return self.data[:, matches[0][1]]

            # Multiple matches found. show what was found
            elif len(matches) > 1:
                print("Found more than one match")
                for match in matches:
                    print(match[0])

            # Nothing found show available keys
            else:
                print("no match found")
                print("available keys")
                for key in self.header_dict.keys():
                    print(key)

    def get_value(self, column, timestep=-1):
        """ Convenience function to get a single
         value
     """
        if timestep > 0:
            timestep = timestep - 1
        return self.get_column(column)[timestep]


def get_variable(ext, phrase, folder):
    """ Function to determine the value assigned to variable in a file by finding
         the name of said variable and setting the parallel value to v.

         ext should be the extension of the file e.g "stt"

         phrase should be the text that preceeds the value in question e.g
         "xgravity ="
     """

    filelist = gl.glob(folder + "/*." + ext)
    filelist = filelist[0]
    with open(filelist, 'r') as f:
        lines = f.readlines()
        phrase = str(phrase)
        for line in lines:
            if line.startswith(phrase):
                line = re.sub(phrase, '', line)
                line = ' '.join(line.split())
                v[0] = (float(line)) / 2


def get_render(x, y, z, zoom):
    """ get_render() creates a basic paraview RenderView object based on domain geometry supplied
        in the form of x, y and z. This object can be appended to manually using the paraview 
        python framework.
    """
    try:

        RenderView1 = pa.GetRenderView()

        if zoom != None:
            z1 = x * zoom

        else:
            z1 = x * 4

        RenderView1.ViewSize = [1000, 1000]
        RenderView1.CameraFocalPoint = [x, y, z]
        RenderView1.CenterOfRotation = [x, y, z]
        RenderView1.CameraPosition = [x, y, z1]
        RenderView1.CameraParallelScale = x
        RenderView1.CenterAxesVisibility = 0

    except Exception, e:
        print str(e) + " problem in get_render"


def get_rep(vari, variable_table):
    """ get_rep() uses a simulation variable (vari) e.g "U" and pre-defined GetLookupTableForArray
        object (example variable_table in pa.paraview_image()) to create a basic 
        GeometryRepresentation object.
        
        This object can be appended to manually using the python framework. 
    """

    DataRepresentation1 = pa.Show()
    DataRepresentation1.ColorArrayName = (vari)
    DataRepresentation1.LookupTable = variable_table

    DataRepresentation1.CubeAxesColor = [0.0, 0.0, 0.0]
    DataRepresentation1.AmbientColor = [0.0, 0.0, 0.0]


def get_widget(vari, vmin, vmax):
    """ Creates the colour scale object and creates a widget object for the
         varible table called. 
     """
    try:
        vdiff = vmax - vmin
        variable_table = pa.GetLookupTableForArray(vari, 1, RGBPoints=[vmin, 0.278431, 0.278431, 0.858824,
                                                                       vmin + (0.143 * vdiff), 0.0, 0.0, 0.360784,
                                                                       vmin + (0.2857 * vdiff), 0.0, 1.0, 1.0,
                                                                       vmin + (0.4285 * vdiff), 0.0, 0.501961, 0.0,
                                                                       vmin + (0.5714 * vdiff), 1.0, 1.0, 0.0,
                                                                       vmin + (0.714257 * vdiff), 1.0, 0.380392, 0.0,
                                                                       vmin + (0.8571 * vdiff), 0.419608, 0.0, 0.0,
                                                                       vmax, 0.49, 0.0, 0.0]
                                                   , VectorMode='Magnitude', NanColor=[0.25, 0.0, 0.0],
                                                   ColorSpace='RGB')

        ScalarWidget = pa.CreateScalarBar(Title=vari, LabelFontSize=12, Enabled=1,
                                          LookupTable=variable_table, TitleFontSize=12)

        return [ScalarWidget, variable_table]

    except Exception, e:
        print str(e) + " [problem in pa.get_widget()]"


def get_range(data, vari):
    """get_range uses a filter and a variable string which, to get the range of the varible scale.

   """
    try:
        data_range = data.GetDataInformation().GetPointDataInformation().GetArrayInformation(vari).GetComponentRange(0)
        return data_range

    except Exception, e:
        print str(e) + " [problem in pa.get_range()]"


def get_bounds(data):
    """ get_domain produces a list of domain max min values
   """
    try:
        pa.UpdatePipeline()
        bounds = data.GetDataInformation().GetBounds()
        return bounds

    except Exception, e:
        print str(e) + " [problem in pa.get_bounds()]"


def get_domain(data):
    """ uses get_bounds() to get an array of max min domain values and calculates the length of each plane.
   """
    try:
        bounds = get_bounds(data)
        x = bounds[1] - bounds[0]
        y = bounds[3] - bounds[2]
        z = bounds[5] - bounds[4]
        return x, y, z

    except Exception, e:
        print str(e) + " [problem in pa.get_domain()]"


def get_center(ext, centerx, centery, centerz):
    """ get center finds a file of extension x, uses get_domain() to find the domain size and then
       works out the individual size of each plane and returns the center values of each plane.
   """
    try:

        data = get_last_modified("RESULT", ext)
        data = pa.OpenDataFile(data)
        pa.UpdatePipeline()
        [x, y, z] = get_domain(data)
        centerx = x / 2
        centery = y / 2
        centerz = z / 2

        return centerx, centery, centerz

    except Exception, e:
        print str(e) + " [problem in pa.get_center()]"


def get_state_center():
    """ get center finds a file of extension x, uses get_domain() to find the domain size and
        then works out the individual size of each plane and returns the center values of 
        each plane.
    """
    try:
        data = get_state_file()
        filter = get_state_data(data)
        pa.SetActiveSource(filter)
        pa.UpdatePipeline()
        [x, y, z] = get_domain(filter)
        centerx = x / 2
        centery = y / 2
        centerz = z / 2

        return centerx, centery, centerz

    except Exception, e:
        print str(e) + " [problem in pa.get_state_center()]"


def get_state_file(ext="pvsm"):
    """ Finds a State file in selected folder and activates it for rendering.
     """
    state_file = get_last_modified("RESULT", ext)
    data = pa.servermanager.LoadState(state_file)
    pa._DisableFirstRenderCameraReset()
    return data


def get_state_data(filter):
    """for using specific objects of a state file.
     """
    pa.SetActiveSource(filter)
    dic = pa.GetSources()
    objects = dic.items()
    filter = objects[0][1]
    return filter


def write_state_image(ext="pvsm"):
    """ Finds last state file and renders to image
     """

    filter = get_state_file(ext)
    pa.GetActiveSource()
    RenderView1 = pa.GetRenderView()
    pa.SetActiveView(RenderView1)
    pa.Render()
    pa.WriteImage("./state.png")


def get_slice_3D(data, x, y, z, normal="z"):
    """ where x,y,z are center coordinates.
    """
    pa.SetActiveSource(data)
    pa.UpdatePipeline()

    Slice1 = pa.Slice(data)
    Slice1.SliceOffsetValues = [0.0]
    Slice1.SliceType.Origin = [x, y, z]
    Slice1.SliceType.Normal = get_normal_vector(normal)

    return Slice1

def get_normal_vector(normal="z"):
    vec = []
    if normal == "x":
        #print "using x normal"
        vec = [-1, 0, 0]
    if normal == "y":
        #print "using y normal"
        vec = [0, -1, 0]
    if normal == "z":
        #print "using z normal"
        vec = [0, 0, -1]
    return vec

def inBounds(data, x, y, z):
    xmin, xmax, ymin, ymax, zmin, zmax = get_bounds(data)
    bounds = {'xmin':xmin, 'xmax': xmax, 'ymin': ymin, 'ymax':ymax, 'zmin':zmin, 'zmax':zmax}
    point = {'x': x, 'y': y, 'z': z}
    dx = 1e-10

    for key in point.keys():
        if point[key] < bounds[key+"min"]+dx:
            point[key] = bounds[key+"min"]+dx
        if point[key] > bounds[key+"max"]-dx:
            point[key] = bounds[key+"max"]-dx
    return point['x'], point['y'], point['z']

def get_plane(data, corners, normal):
    dirs = ['x', 'y', 'z']
    dirs.remove(normal)

    x = corners['xmin']
    y = corners['ymin']
    z = corners['zmin']
    x, y, z = inBounds(data, x, y, z)

    data = get_slice_3D(data, x, y, z, normal)
    if len(dirs)!= 2:
        sys.exit("Error in para_reader get_plane. Lenght of dirs array is "+str(len(dirs))+", should be 2.")
    points = {'x': x, 'y': y, 'z': z}
    for dir in dirs:
        points[dir] = corners[dir+'min']
        data = get_clip_3D(data, points['x'], points['y'], points['z'], dir, insideout=True)
        points[dir] = corners[dir+'max']
        data = get_clip_3D(data, points['x'], points['y'], points['z'], dir, insideout=False)
    return data

def get_clip_3D(filter, x, y, z, normal="z", insideout=False):
    clip1 = pa.Clip(Input=filter)
    clip1.ClipType = 'Plane'

    clip1.ClipType.Origin = [x, y, z]
    clip1.ClipType.Normal = get_normal_vector(normal)
    if insideout:
        clip1.InsideOut = 1
    return clip1

def get_custom_slice_3D(filter, x, y, z, a, b, c):
    pa.SetActiveSource(filter)
    pa.UpdatePipeline()
    Slice1 = pa.Slice()
    Slice1.SliceOffsetValues = [0.0]
    Slice1.SliceType.Origin = [x, y, z]
    Slice1.SliceType.Normal = [a, b, c]
    return Slice1


def get_slice_2D(ext):
    """get_slice uses get_domain() and get_center() to determine which plane the simultion is in
      and which normal to create a slice for the image. 
   """
    try:

        [x, y, z] = get_domain(data)

        [centerx, centery, centerz] = get_center(ext, centerx, centery, centerz)

        if x < 1e-04 or y < 1e-04 or z < 1e-04:

            Slice1 = pa.Slice()
            Slice1.SliceOffsetValues = [0.0]
            Slice1.SliceType.Origin = [centerx, centery, centerz]

            if z < 1e-04:
                print "simulation is in xy"

                Slice1.SliceType.Normal = [0, 0, -1]

            if y < 1e-04:
                print "simulation is in xz"

                Slice1.SliceType.Normal = [0, -1, 0]

            if x < 1e-04:
                print "simulation is in yz"

                Slice1.SliceType.Normal = [-1, 0, 0]

            return Slice1

        else:
            print "data is 3D"

    except Exception, e:
        print str(e) + " [problem in pa.get_slice()]"


def get_keys(filter):
    """ returns the keys in the variable dictionary for use in rendering multiple images.
   """
    try:

        keys = filter.GetPointDataInformation().keys()
        return keys

    except Exception, e:
        print str(e) + " [problem in pa.get_keys()]"


def get_items(filter):
    """ returns the keys in the variable dictionary for use in rendering multiple images.
   """
    try:

        items = filter.GetPointDataInformation().items()
        return items

    except Exception, e:
        print str(e) + " [problem in pa.get_items()]"


def paraview_image(filter, vari, ext, folder, dim="2d", x=None, y=None, z=None, zoom=None):
    """(filter,vari,ext,folder,dim="2d",x=None,y=None,z=None,zoom=None)
      """

    vari1 = 'POINT_DATA'
    v = [0]
    ScalarWidget = [0]
    variable_table = [0]
    data_range = [0]
    centerpoint = [0]
    centerx = [0]
    centery = [0]
    centerz = [0]

    pa.SetActiveSource(filter)
    pa.UpdatePipeline()

    # Find polar values of variable array
    try:
        data_range = get_range(filter, vari)
        vmin = data_range[0]
        vmax = data_range[1]
    except Exception, e:
        print str(e) + " [problem in pa.data_range()]"


    # Call get_widget() to define a scale object and construct appropriate scale widget:
    try:
        [ScalarWidget, variable_table] = get_widget(vari, vmin, vmax)
    except Exception, e:
        print str(e) + " [problem in pa.get_widget()]"


    # Create basic GeometryRepresentation and RenderView objects:
    try:
        get_rep(vari, variable_table)
    except Exception, e:
        print str(e) + " [problem in pa.get_rep()]"

    if dim == "3d":
        centerx = x
        centery = y
        centerz = z

    else:
        try:
            [centerx, centery, centerz] = get_center(ext, centerx, centery, centerz)
        except Exception, e:
            print str(e) + " [problem in pa.get_center()]"

    try:
        get_render(centerx, centery, centerz, zoom)
    except Exception, e:
        print str(e) + " [problem in pa.get_render()]"


    # Append GeometryRepresentation + ScalarWidget to RenderView object:

    pa.GetRenderView().Representations.append(ScalarWidget)

    # Write current RenderView object to file:

    picdir = folder + "/simulation_images/"
    vari = vari.replace(" ", "")
    if not os.path.exists(picdir):
        print "creating image directory"
        os.makedirs(picdir)

    writer = pa.WriteImage(os.path.join(picdir + vari + ".png"))

    #print "File" + " written to " + picdir

    pa.Delete(ScalarWidget)
    pa.Delete(writer)


def render_image_vtk(ext="vtm", folder=os.getcwd(), dim="2d", x=None, y=None, z=None, zoom=None):
    """ For 2D simulations, finds the most recently modified file of extension ext and
       renders image of each varible from a viewpoint determined by the size of the domain.
   """
    try:
        if ext == "vtm" or ext == "vtr":
            print "Rendering " + ext + "..."

            vtk = get_last_modified("RESULT", ext)
            filter = pa.OpenDataFile(vtk)
            varis = get_keys(filter)
            for vari in varis:
                paraview_image(filter, vari, ext, folder, dim, x, y, z, zoom)


    except Exception, e:
        print str(e) + ", problem with " + ext + " render_image_vtk(), cannot continue"

    pa.servermanager.Disconnect()


def get_line_plot(filter, (x1, y1, z1), (x2, y2, z2), cell=False):
    plot_over_line = pa.PlotOverLine(filter)
    plot_over_line.Source.Point1 = [x1, y1, z1]
    plot_over_line.Source.Point2 = [x2, y2, z2]

    if not cell:
        data = save_data_to_dict(plot_over_line, cell=False)
    else:
        data = save_data_to_dict(plot_over_line, cell=True)
    return data


def get_line_object(filter, (x1, y1, z1), (x2, y2, z2)):
    plot_over_line = pa.PlotOverLine(filter)
    plot_over_line.Source.Point1 = [x1, y1, z1]
    plot_over_line.Source.Point2 = [x2, y2, z2]

    return plot_over_line


def get_avg_over_line(plot_over_line_object, var, cell=False):
    avg_dict = massflow_avg(plot_over_line_object, [], var, cell=cell)
    var_list = ['massflow', 'massflow_t_' + var]
    for v in var_list:
        if not v in avg_dict:
            raise ("Incompatible arguments - API of massflow_avg() was probably changed")
    return avg_dict[var_list[1]] / avg_dict[var_list[0]]


def get_time_series(pvd, x, y, z):
    timesteps = pvd.TimestepValues
    ProbeLocation6 = pa.ProbeLocation(pvd, ProbeType="Fixed Radius Point Source")

    ProbeLocation6.ProbeType.Center = [x, y, z]
    var_arr = []
    for time in timesteps:
        pa.UpdatePipeline(time)
        var_arr.append(save_data_to_dict(ProbeLocation6))
    var_dict = {}
    for key_val in var_arr[0].keys():
        var_dict[key_val] = ([list(item[key_val]) for item in var_arr])
    return {'times': timesteps, 'vars': var_dict}


def get_iteration_string(niter):
    return str(niter).rjust(7, '0')


def get_time(vtm_file):
    try:
        timestep = vtm_file.split(".")[-2:-1][0].lstrip('0')
        cfl_file = os.path.join(os.path.dirname(vtm_file), 'cfl.dat')
        cfl = file_reader(cfl_file)
        index =np.where(cfl.get_column(0)==float(timestep))[0]
        return cfl.get_column(2)[index+1][0]
    except:
        return None


class para_reader:
    def __init__(self, datafile='RESULT/xy-catalytic_comb.0000001.vtm'):
        """
   Create a para_reader object
   The constructor automatically creates a Threshold which is 
   useful when working with 2D data. To be improved
   Members:
     self.datafile  = Name of the datafile
     self.input     = The input data file
     self.threshold = A threshold filter (range -1E6 to 1E6)
                      on pressure
   """
        self.datafile = datafile
        self.input = pa.OpenDataFile(datafile)
        pa.UpdatePipeline()
        self.threshold = pa.Threshold(self.input)
        self.threshold.ThresholdRange = [-1E6, 1E6]
        pa.UpdatePipeline()
        pa.Show(self.threshold)


import contextlib, cStringIO, sys


@contextlib.contextmanager
def quiet(devnull=False):
    '''
    Prevent print to stdout, but if there was an error then catch it and
    print the output before raising the error.
    Example:
    with quiet():
        res = noisy_function(a,b,c)
    => Nothing will be shown to stdout unless the function raises an exception
    If devnull is True, stdout is redirected to /dev/null and the output is lost forever
    (usefull if a lot of output is generated and we dont want to buffer it)
    '''

    #class DummyFile( object ):
    #    def write( self, x ): pass

    saved_stdout = sys.stdout
    if devnull:
        sys.stdout = open(os.devnull, 'w')
    else:
        sys.stdout = cStringIO.StringIO()
    try:
        yield
    except:
        if not devnull:
            saved_output = sys.stdout
            print saved_output.getvalue()
        sys.stdout = saved_stdout
        raise
    sys.stdout = saved_stdout
