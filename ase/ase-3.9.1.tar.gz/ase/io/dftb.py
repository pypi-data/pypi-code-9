from ase.atoms import Atoms

def read_dftb(filename='dftb_in.hsd'):
    """Method to read coordinates form DFTB+ input file dftb_in.hsd
    additionally read information about fixed atoms
    and periodic boundary condition
    """
    from ase import Atoms

    if isinstance(filename, str):
        myfile = open(filename)

    lines = myfile.readlines()
    atoms_pos = []
    atom_symbols = []
    type_names = []
    my_pbc = False
    mycell = []


    for iline, line in enumerate(lines):
        if (line.strip().startswith('#')):
            pass
        else:
            if ('TypeNames' in line):
                col = line.split()
                for i in range(3, len(col)-1):
                    type_names.append(col[i].strip("\""))
            elif ('Periodic' in line):
                if ('Yes' in line):
                    my_pbc = True
            elif ('LatticeVectors' in line):
                for imycell in range(3):
                    extraline = lines[iline+imycell+1]
                    cols = extraline.split()
                    mycell.append(\
                        [float(cols[0]),float(cols[1]),float(cols[2])])
            else:
                pass

    start_reading_coords = False
    stop_reading_coords = False
    for line in lines:
        if (line.strip().startswith('#')):
            pass
        else:
            if ('TypesAndCoordinates' in line):
                start_reading_coords = True
            if start_reading_coords:
                if ('}' in line):
                    stop_reading_coords = True
            if (start_reading_coords and not(stop_reading_coords)
            and not 'TypesAndCoordinates' in line):
                typeindexstr, xxx, yyy, zzz = line.split()[:4]
                typeindex = int(typeindexstr)
                symbol = type_names[typeindex-1]
                atom_symbols.append(symbol)
                atoms_pos.append([float(xxx), float(yyy), float(zzz)])

            
    if isinstance(filename, str):
        myfile.close()

    atoms = Atoms(positions = atoms_pos, symbols = atom_symbols, 
                  cell = mycell, pbc = my_pbc)


    return atoms

def read_dftb_velocities(atoms, filename='geo_end.xyz'):
    """Method to read velocities (AA/ps) from DFTB+ output file geo_end.xyz
    """
    from ase import Atoms
    from ase.units import second
    #AA/ps -> ase units
    AngdivPs2ASE = 1.0/(1e-12*second)


    if isinstance(filename, str):
        myfile = open(filename)

    lines = myfile.readlines()
    #remove empty lines
    lines_ok = []
    for line in lines:
        if line.rstrip():
            lines_ok.append(line)
    
    velocities = []
    natoms = atoms.get_number_of_atoms()
    last_lines = lines_ok[-natoms:]
    for iline, line in enumerate(last_lines):
        inp = line.split()
        velocities.append([float(inp[4])*AngdivPs2ASE,
                           float(inp[5])*AngdivPs2ASE,
                           float(inp[6])*AngdivPs2ASE])

    atoms.set_velocities(velocities)
    return atoms

def write_dftb_velocities(atoms, filename='velocities.txt'):
    """Method to write velocities (in atomic units) from ASE
       to a file to be read by dftb+
    """
    from ase import Atoms
    from ase.units import AUT, Bohr
    #ase units -> atomic units
    ASE2au = Bohr / AUT

    if isinstance(filename, str):
        myfile = open(filename, 'w')
    else: # Assume it's a 'file-like object'
        myfile = filename
    
    velocities = atoms.get_velocities()
    for velocity in velocities:
        myfile.write(' %19.16f %19.16f %19.16f \n' 
                %(  velocity[0] / ASE2au, 
                    velocity[1] / ASE2au, 
                    velocity[2] / ASE2au))
                     
    return


def write_dftb(filename, atoms):
    """Method to write atom structure in DFTB+ format
       (gen format)
    """
    import numpy as np

    #sort
    atoms.set_masses()
    masses = atoms.get_masses()
    indexes = np.argsort(masses)
    atomsnew = Atoms()
    for i in indexes:
        atomsnew = atomsnew + atoms[i]

    if isinstance(filename, str):
        myfile = open(filename, 'w')
    else: # Assume it's a 'file-like object'
        myfile = filename

    ispbc = atoms.get_pbc()
    box = atoms.get_cell()
    
    if (any(ispbc)):
        myfile.write('%8d %2s \n' %(len(atoms), 'S'))
    else:
        myfile.write('%8d %2s \n' %(len(atoms), 'C'))

    chemsym = atomsnew.get_chemical_symbols()
    allchem = ''
    for i in chemsym:
        if i not in allchem:
            allchem = allchem + i + ' '
    myfile.write(allchem+' \n')

    coords = atomsnew.get_positions()
    itype = 1
    for iatom, coord in enumerate(coords):
        if iatom > 0:
            if chemsym[iatom] != chemsym[iatom-1]:
                itype = itype+1
        myfile.write('%5i%5i  %19.16f %19.16f %19.16f \n' \
                    %(iatom+1, itype, 
                      coords[iatom][0], coords[iatom][1], coords[iatom][2]))
    # write box
    if (any(ispbc)):
        #dftb dummy
        myfile.write(' %19.16f %19.16f %19.16f \n' %(0, 0, 0))
        myfile.write(' %19.16f %19.16f %19.16f \n' 
                %( box[0][0], box[0][1], box[0][2]))
        myfile.write(' %19.16f %19.16f %19.16f \n' 
                %( box[1][0], box[1][1], box[1][2]))
        myfile.write(' %19.16f %19.16f %19.16f \n' 
                %( box[2][0], box[2][1], box[2][2]))

    if isinstance(filename, str):    
        myfile.close()
