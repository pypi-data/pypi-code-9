"""Support to read the .mxp file format used by Stratagenes qPCR machines.


read_mxp(filename) is the basic function you need, returns
a DataFrame containing the amplification curves (40 cycles, <=96 wells...)
    with the following columns:
    Well: 0..96
    Well Key A1..H12
    Assay - the assay in this well - exported as 'Dye' by MxPro
    Well Name - the name the user assigned
    Fluorescence - the raw measurement at this cyle/well
    Temperature - temperature at this cycle/well
    Cycle - 0..40

Currently only tested for 96 well plates on Mx3000P and Mx3005P machines.


"""
import pandas as pd
import olefile
import numpy as np

def read_mxp(filename):
    """Read an MXP file and return a dataframe with the annotated amplification curves"""
    ole = olefile.OleFileIO(filename)
    fileformat = discover_fileformat(ole)
    #print 'fileformat', fileformat
    well_names, assay_names = np.array(extract_well_names_and_assay_names(ole, fileformat))
    well_numbers = np.array(xrange(0, 97))
    #empty wells that were not read, and are not in the amplification curve file...
    ok_wells = (well_names != '') | (assay_names != '')
    well_names = well_names[ok_wells]
    assay_names = assay_names[ok_wells]
    well_numbers = well_numbers[ok_wells]

    amplification_data = extract_amplification_curves(ole, fileformat, len(assay_names))

    #melting_data = extract_melting_curves(ole)
        
    cycle_count = len(amplification_data[0][0])
    well_count = sum(ok_wells)
    amp_data = {'Well': [], 'Well Key': [], 'Assay': [], 'Well Name': [], 'Fluorescence': [], 'Temperature': [], 'Cycle': []}
    for ii in xrange(0, well_count):
        amp_data['Cycle'].extend(list(xrange(1, cycle_count + 1)))
        amp_data['Well'].extend([well_numbers[ii]] * cycle_count)
        amp_data['Well Key'].extend([well_no_to_code(well_numbers[ii] + 1)] * cycle_count)
        amp_data['Assay'].extend([assay_names[ii]] * cycle_count)
        amp_data['Well Name'].extend([well_names[ii]] * cycle_count)
        amp_data['Fluorescence'].extend(amplification_data[0][ii])
        amp_data['Temperature'].extend(amplification_data[1][ii])
    return pd.DataFrame(amp_data)

def well_no_to_code(well_no):
    """1 -> A1, 2 -> A2, 96 -> H12"""
    well_no = well_no -1
    first = well_no / 12
    second = well_no % 12
    return chr(ord('A') + first) + str(second + 1)

def code_to_well_no(code):
    """A1 -> 1, H12 -> 96"""
    if len(code) not in (2, 3):
        raise ValueError("Invalid code")
    first = ord(code[0]) - ord('A')
    second = int(code[1:])
    return 12 * first + second

def discover_fileformat(ole):
  path = 'Storage2/Stream2'
  with ole.openstream(path) as op:
      x = op.read()
  if  ord(x[0xf32]) != 0:
      return 0
  else:
      return 1
     
def extract_well_names_and_assay_names(ole, fileformat):
    """Read well and assay names from an MXP file"""
    if isinstance(ole, olefile.OleFileIO):
        path = 'Storage0/Stream0'
        with ole.openstream(path) as op:
            d = op.read()
    else:
        path = os.path.join(ole, 'Storage0_Stream0')
        with open(path, 'rb') as op:
            d = op.read()
    parts = d.split('\xf0\xe7i\xa5') 
    if fileformat == 1:
        well_parts = [parts[x] for x in xrange(2, len(parts), 12)]
        assay_parts = [parts[x] for x in xrange(9, len(parts), 12)]
        fileformat = 1
    elif fileformat == 0:
        well_parts = [parts[x] for x in xrange(2, len(parts), 11)]
        assay_parts = [parts[x] for x in xrange(8, len(parts), 11)]    
        fileformat = 0
    else:
        raise ValueError('fileformat')
    if len(well_parts) != 96:
        raise ValueError("Did not find 96 well parts in Storage0")
    well_names = []
    for part in well_parts:
        length = ord(part[4])
        name = part[5:5 + length]
        well_names.append(name)
    assay_names = []
    for part in assay_parts:
        length = ord(part[8])
        name = part[9:9 + length]
        assay_names.append(name)
    well_names = np.array(well_names)
    assay_names = np.array(assay_names)
    #if (well_names == '').all(): # I have seen files without well names asigned...
        #raise ValueError("Could not find a single well name in that file!")
    if (assay_names == '').all():
        raise ValueError("Could not find a single assay name in that file!")
    return well_names, assay_names

def to_16_bit(letters):
    """Convert the internal (little endian) number format to an int"""
    a = ord(letters[0])
    b = ord(letters[1])
    return (b << 8) + a

def extract_amplification_curves(ole, fileformat, supposed_wells = 96):
    """extract amplification curves (40 cycles, 96 wells...) from an mxp file"""
    path = 'Storage2/Stream2'
    with ole.openstream(path) as op:
        x = op.read()
    if fileformat == 0:
        no_of_cyles = ord(x[0xf32]) # offset...
    elif fileformat == 1:
        no_of_cyles = ord(x[0x12f4]) # offset...
    else:
        raise ValueError("Unknown fileformat")
    if no_of_cyles != 40:
        raise ValueError("File does not contain 40 cycles. Were: %i" % no_of_cyles)
    y = x.split("\x00\x00\x00\x60") #96...
    y = y[4]
    y = x.split("\x00\x00\x00\x28")#possibly use 00 00 00 60 to split first
    y = y[1:supposed_wells + 1]
    y[-1] = y[-1][:len(y[0])] # there is a different seperator after the last one, so we set it to the first length
    if max(set([len(a) for a in y])) > 466: #428:
        raise ValueError("Seen a very large chun: %i " %max(set([len(a) for a in y])))
    result_fluorescence = []
    result_temperatures = []
    for block in y:
        numbers = [to_16_bit(block[3+offset*10:3+2+offset*10]) for offset in xrange(0, no_of_cyles)]
        if len(numbers) != no_of_cyles:
            raise ValueError("Not exactly 40 datapoints in amplification curve")
        result_fluorescence .append(numbers)
        temperatures = [to_16_bit(block[3+4+offset*10:3+4+2+offset*10]) / 10.0 for offset in xrange(0, no_of_cyles)]
        result_temperatures.append(temperatures)
    if len(result_fluorescence) != supposed_wells:
        raise ValueError("Not exactly the supposed %i wells - was %i" % (supposed_wells, len(y)))
    return result_fluorescence, result_temperatures
