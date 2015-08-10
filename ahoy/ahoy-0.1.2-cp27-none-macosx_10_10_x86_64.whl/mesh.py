import fipy


gmsh_text_box = '''
// Define the square that acts as the system boundary.

dx = %(dx)g;
Lx = %(Lx)g;
Ly = %(Ly)g;
p_n_w = newp; Point(p_n_w) = {-Lx / 2.0, Ly / 2.0, 0, dx};
p_n_e = newp; Point(p_n_e) = {Lx / 2.0, Ly / 2.0, 0, dx};
p_s_e = newp; Point(p_s_e) = {Lx / 2.0, -Ly / 2.0, 0, dx};
p_s_w = newp; Point(p_s_w) = {-Lx / 2.0, -Ly / 2.0, 0, dx};
l_n = newl; Line(l_n) = {p_n_w, p_n_e};
l_e = newl; Line(l_e) = {p_n_e, p_s_e};
l_s = newl; Line(l_s) = {p_s_e, p_s_w};
l_w = newl; Line(l_w) = {p_s_w, p_n_w};
ll = newll; Line Loop(ll) = {l_n, l_e, l_s, l_w};

'''

gmsh_text_circle = '''
// Define a circle that acts as an obstacle
x = %(x)g;
y = %(y)g;
R = %(R)g;
p_c = newp; Point(p_c) = {x, y, 0, dx};
p_w = newp; Point(p_w) = {x - R, y, 0, dx};
p_n = newp; Point(p_n) = {x, y + R, 0, dx};
p_e = newp; Point(p_e) = {x + R, y, 0, dx};
p_s = newp; Point(p_s) = {x, y - R, 0, dx};
c_w_n = newreg; Circle(c_w_n) = {p_w, p_c, p_n};
c_n_e = newreg; Circle(c_n_e) = {p_n, p_c, p_e};
c_e_s = newreg; Circle(c_e_s) = {p_e, p_c, p_s};
c_s_w = newreg; Circle(c_s_w) = {p_s, p_c, p_w};
Line Loop(%(i)d) = {c_w_n, c_n_e, c_e_s, c_s_w};

'''

gmsh_text_surface = '''
// The first argument is the outer loop boundary.
// The remainder are holes in it.
Plane Surface(1) = {ll, %(args)s};
'''


def _porous_mesh_geo_factory(rs, R, dx, L):
    gmsh_text = gmsh_text_box % {'dx': dx, 'Lx': L[0], 'Ly': L[1]}
    circle_loop_indexes = []
    if rs is not None and len(rs) and R:
        for i in range(len(rs)):
            index = 10 * (i + 1)
            gmsh_text += gmsh_text_circle % {'x': rs[i][0], 'y': rs[i][1],
                                             'R': R, 'i': index}
            circle_loop_indexes += [index]
    surface_args = ', '.join([str(i) for i in circle_loop_indexes])
    gmsh_text += gmsh_text_surface % {'args': surface_args}
    return gmsh_text


def uniform_mesh_factory(L, dx):
    dim = len(L)
    if dim == 1:
        return fipy.Grid1D(dx=dx, Lx=L[0]) - L[0] / 2.0
    elif dim == 2:
        return (fipy.Grid2D(dx=dx, dy=dx, Lx=L[0], Ly=L[1]) -
                ((L[0] / 2.0,), (L[1] / 2.0,)))


def porous_mesh_factory(rs, R, dx, L):
    return fipy.Gmsh2D(_porous_mesh_geo_factory(rs, R, dx, L))
