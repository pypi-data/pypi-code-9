#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import unittest
import sys
sys.path.append("./src/")
# import pdb
# pdb.set_trace();

import scipy.io
import math
import copy

import logging
logger = logging.getLogger(__name__)


import argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.widgets import Slider, Button

try:
    from PyQt4 import QtGui, QtCore
    from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
    from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
except:
    logger.warning('PyQt4 not detected')
    pass


class sed3:

    """ Viewer and seed editor for 2D and 3D data.

    sed3(img, ...)

    img: 2D or 3D grayscale data
    voxelsizemm: size of voxel, default is [1, 1, 1]
    initslice: 0
    colorbar: True/False, default is True
    cmap: colormap
    zaxis: axis with slice numbers
    show: (True/False) automatic call show() function
    sed3_on_close: callback function on close



    ed = sed3(img)
    ed.show()
    selected_seeds = ed.seeds

    """
    # if data.shape != segmentation.shape:
    # raise Exception('Input size error','Shape if input data and segmentation
    # must be same')

    def __init__(
        self, img, voxelsizemm=[1, 1, 1], initslice=0, colorbar=True,
        cmap=matplotlib.cm.Greys_r, seeds=None, contour=None, zaxis=0,
        mouse_button_map={1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8},
        windowW=[], windowC=[], show=False, sed3_on_close=None, figure=None
    ):

        
        self.sed3_on_close = sed3_on_close
        if figure is None:
            self.fig = plt.figure()
        else:
            self.fig = figure
        img = _import_data(img, axis=0, slice_step=1)

        if len(img.shape) == 2:
            imgtmp = img
            img = np.zeros([1, imgtmp.shape[0], imgtmp.shape[1]])
            # self.imgshape.append(1)
            img[-1, :, :] = imgtmp

            zaxis = 0
            # pdb.set_trace();

        # Rotate data in depndecy on zaxispyplot
        img = self._rotate_start(img, zaxis)
        seeds = self._rotate_start(seeds, zaxis)
        contour = self._rotate_start(contour, zaxis)

        self.rotated_back = False
        self.zaxis = zaxis

        # self.ax = self.fig.add_subplot(111)
        self.imgshape = list(img.shape)
        self.img = img
        self.actual_slice = initslice
        self.colorbar = colorbar
        self.cmap = cmap
        if seeds is None:
            self.seeds = np.zeros(self.imgshape, np.int8)
        else:
            self.seeds = seeds
        if not (windowW and windowC):
            self.imgmax = np.max(img)
            self.imgmin = np.min(img)
        else:
            self.imgmax = windowC + (windowW / 2)
            self.imgmin = windowC - (windowW / 2)

        """ Mapping mouse button to class number. Default is normal order"""
        self.button_map = mouse_button_map

        self.contour = contour

        self.press = None
        self.press2 = None

# language
        self.texts = {'btn_delete': 'Delete', 'btn_close': 'Close'}

        # iself.fig.subplots_adjust(left=0.25, bottom=0.25)
        self.ax = self.fig.add_axes([0.2, 0.3, 0.7, 0.6])

        self.draw_slice()

        if self.colorbar:
            self.fig.colorbar(self.imsh)

        # user interface look

        axcolor = 'lightgoldenrodyellow'
        ax_actual_slice = self.fig.add_axes(
            [0.2, 0.2, 0.6, 0.03], axisbg=axcolor)
        self.actual_slice_slider = Slider(ax_actual_slice, 'Slice', 0,
                                          self.imgshape[2] - 1,
                                          valinit=initslice)

        # conenction to wheel events
        self.fig.canvas.mpl_connect('scroll_event', self.on_scroll)
        self.actual_slice_slider.on_changed(self.sliceslider_update)
# draw
        self.fig.canvas.mpl_connect('button_press_event', self.on_press)
        self.fig.canvas.mpl_connect('button_release_event', self.on_release)
        self.fig.canvas.mpl_connect('motion_notify_event', self.on_motion)

# delete seeds
        self.ax_delete_seeds = self.fig.add_axes([0.2, 0.1, 0.1, 0.075])
        self.btn_delete = Button(
            self.ax_delete_seeds, self.texts['btn_delete'])
        self.btn_delete.on_clicked(self.callback_delete)

# close button
        self.ax_delete_seeds = self.fig.add_axes([0.7, 0.1, 0.1, 0.075])
        self.btn_delete = Button(self.ax_delete_seeds, self.texts['btn_close'])
        self.btn_delete.on_clicked(self.callback_close)

        self.draw_slice()
        if show:
            self.show()

    def _rotate_start(self, data, zaxis):
        if data is not None:
            if zaxis == 0:
                data = np.transpose(data, (1, 2, 0))
            elif zaxis == 2:
                pass
            else:
                print "problem with zaxis in _rotate_start()"

        return data

    def _rotate_end(self, data, zaxis):
        if data is not None:
            if self.rotated_back is False:
                if zaxis == 0:
                    data = np.transpose(data, (2, 0, 1))
                elif zaxis == 2:
                    pass
                else:
                    print "problem with zaxis in _rotate_start()"

            else:
                print "There is a danger in calling show() twice"

        return data

    def update_slice(self):
        # TODO tohle je tu kvuli contour, neumim ji odstranit jinak
        self.ax.cla()

        self.draw_slice()

    def draw_slice(self):
        sliceimg = self.img[:, :, int(self.actual_slice)]
        self.imsh = self.ax.imshow(sliceimg, self.cmap, vmin=self.imgmin,
                                   vmax=self.imgmax, interpolation='nearest')
        # plt.hold(True)
        # pdb.set_trace();
        self.ax.imshow(self.prepare_overlay(
            self.seeds[:, :, int(self.actual_slice)]
        ), interpolation='nearest', vmin=self.imgmin, vmax=self.imgmax)

        # vykreslení okraje
        # X,Y = np.meshgrid(self.imgshape[0], self.imgshape[1])

        if self.contour is not None:
            try:
                # exception catch problem with none object in image
                # ctr =
                self.ax.contour(
                    self.contour[:, :, int(self.actual_slice)], 1,
                    levels=[0.5, 1.5, 2.5],
                    linewidths=2)
            except:
                pass

        # print ctr
        # import pdb; pdb.set_trace()

        self.fig.canvas.draw()
        # self.ax.cla()
        # del(ctr)

        # pdb.set_trace();
        # plt.hold(False)

    def next_slice(self):
        self.actual_slice = self.actual_slice + 1
        if self.actual_slice >= self.imgshape[2]:
            self.actual_slice = 0

    def prev_slice(self):
        self.actual_slice = self.actual_slice - 1
        if self.actual_slice < 0:
            self.actual_slice = self.imgshape[2] - 1

    def sliceslider_update(self, val):
        # zaokrouhlení
        # self.actual_slice_slider.set_val(round(self.actual_slice_slider.val))
        self.actual_slice = round(val)
        self.update_slice()

    def prepare_overlay(self, seeds):
        sh = list(seeds.shape)
        if len(sh) == 2:
            sh.append(4)
        else:
            sh[2] = 4
        # assert sh[2] == 1, 'wrong overlay shape'
        # sh[2] = 4
        overlay = np.zeros(sh)

        overlay[:, :, 0] = (seeds == 1)
        overlay[:, :, 1] = (seeds == 2)
        overlay[:, :, 2] = (seeds == 3)

        overlay[:, :, 3] = (seeds > 0)

        return overlay

    def show(self):
        """ Function run viewer window.
        """
        plt.show()

        return self.prepare_output_data()

    def prepare_output_data(self):
        if rotated_back is False:
        # Rotate data in depndecy on zaxis
            self.img = self._rotate_end(self.img, self.zaxis)
            self.seeds = self._rotate_end(self.seeds, self.zaxis)
            self.contour = self._rotate_end(self.contour, self.zaxis)
            self.rotated_back = True
        return self.seeds

    def on_scroll(self, event):
        ''' mouse wheel is used for setting slider value'''
        if event.button == 'up':
            self.next_slice()
        if event.button == 'down':
            self.prev_slice()
        self.actual_slice_slider.set_val(self.actual_slice)
        # tim, ze dojde ke zmene slideru je show_slce volan z nej
        # self.show_slice()
        # print self.actual_slice

# malování -------------------
    def on_press(self, event):
        'on but-ton press we will see if the mouse is over us and store data'
        if event.inaxes != self.ax:
            return
        # contains, attrd = self.rect.contains(event)
        # if not contains: return
        # print 'event contains', self.rect.xy
        # x0, y0 = self.rect.xy
        self.press = [event.xdata], [event.ydata], event.button
        # self.press1 = True

    def on_motion(self, event):
        'on motion we will move the rect if the mouse is over us'
        if self.press is None:
            return

        if event.inaxes != self.ax:
            return
        # print event.inaxes

        x0, y0, btn = self.press
        x0.append(event.xdata)
        y0.append(event.ydata)

    def on_release(self, event):
        'on release we reset the press data'
        if self.press is None:
            return
        # print self.press
        x0, y0, btn = self.press
        if btn == 1:
            color = 'r'
        elif btn == 2:
            color = 'b'  # noqa

        # plt.axes(self.ax)
        # plt.plot(x0, y0)
        # button Mapping
        btn = self.button_map[btn]

        self.set_seeds(y0, x0, self.actual_slice, btn)
        # self.fig.canvas.draw()
        # pdb.set_trace();
        self.press = None
        self.update_slice()

    def callback_delete(self, event):
        self.seeds[:, :, int(self.actual_slice)] = 0
        self.update_slice()

    def callback_close(self, event):
        matplotlib.pyplot.clf()
        matplotlib.pyplot.close()
        if self.sed3_on_close is not None:
            self.sed3_on_close(self)

    def set_seeds(self, px, py, pz, value=1, voxelsizemm=[1, 1, 1],
                  cursorsizemm=[1, 1, 1]):
        assert len(px) == len(
            py), 'px and py describes a point, their size must be same'

        for i, item in enumerate(px):
            self.seeds[int(item), int(py[i]), int(pz)] = value

# @todo
    def get_seed_sub(self, label):
        """ Return list of all seeds with specific label
        """
        sx, sy, sz = np.nonzero(self.seeds == label)

        return sx, sy, sz

    def get_seed_val(self, label):
        """ Return data values for specific seed label"""
        return self.img[self.seeds == label]


def show_slices(data3d, contour=None, seeds=None, axis=0, slice_step=1,
                shape=None, show=True):
    """
    Show slices as tiled image

    :param data3d: Input data
    :param contour: Data for contouring
    :param seeds: Seed data
    :param axis: Axis for sliceing
    :param slice_step: Show each "slice_step"-th slice
    """

    data3d = _import_data(data3d, axis=axis, slice_step=slice_step)
    contour = _import_data(contour, axis=axis, slice_step=slice_step)
    seeds = _import_data(seeds, axis=axis, slice_step=slice_step)

    number_of_slices = data3d.shape[axis]
    # square image
#     nn = int(math.ceil(number_of_slices ** 0.5))

#     sh = [nn, nn]

    # 4:3 image
    sh = shape
    if sh is None:
        na = int(math.ceil(number_of_slices * 16.0 / 9.0)**0.5)
        nb = int(math.ceil(float(number_of_slices) / na))
        sh = [nb, na]

    dsh = __get_slice(data3d, 0, axis).shape
    slimsh = [int(dsh[0]*sh[0]), int(dsh[1] * sh[1])]
    slim = np.zeros(slimsh, dtype=data3d.dtype)
    slco = None
    slse = None
    if seeds is not None:
        slse = np.zeros(slimsh, dtype=seeds.dtype)
    if contour is not None:
        slco = np.zeros(slimsh, dtype=contour.dtype)
#         slse =
#     f, axarr = plt.subplots(sh[0], sh[1])

    for i in range(0, number_of_slices):
        cont = None
        seeds2d = None
        im2d = __get_slice(data3d, i, axis)
        if contour is not None:
            cont = __get_slice(contour, i, axis)
            slco = __put_slice_in_slim(slco, cont, sh, i)
        if seeds is not None:
            seeds2d = __get_slice(seeds, i, axis)
            slse = __put_slice_in_slim(slse, seeds2d, sh, i)
#         plt.axis('off')
#         plt.subplot(sh[0], sh[1], i+1)
#         plt.subplots_adjust(wspace=0, hspace=0)

        slim = __put_slice_in_slim(slim, im2d, sh, i)
#         show_slice(im2d, cont, seeds2d)
    plt.axis('off')
    show_slice(slim, slco, slse)
    if show:
        plt.show()

#         a, b = np.unravel_index(i, sh)

#     pass


def __get_slice(data, slice_number, axis=0):
    if axis == 0:
        return data[slice_number, :, :]
    elif axis == 1:
        return data[:, slice_number, :]
    elif axis == 2:
        return data[:, :, slice_number]
    else:
        print "axis number error"
        return None


def __put_slice_in_slim(slim, dataim, sh, i):
    """
    put one small slice as a tile in a big image
    """
    a, b = np.unravel_index(int(i), sh)

    st0 = int(dataim.shape[0] * a)
    st1 = int(dataim.shape[1] * b)
    sp0 = int(st0 + dataim.shape[0])
    sp1 = int(st1 + dataim.shape[1])

    slim[
        st0:sp0,
        st1:sp1
    ] = dataim

    return slim


# def show():
#     plt.show()
# \
#
# def close():
#     plt.close()


def show_slice(data2d, contour2d=None, seeds2d=None):
    import copy as cp
    # Show results
    colormap = cp.copy(plt.cm.get_cmap('brg'))
    colormap._init()
    colormap._lut[:1:, 3] = 0

    plt.imshow(data2d, cmap='gray', interpolation='none')
    if contour2d is not None:
        plt.contour(contour2d, levels=[0.5, 1.5, 2.5])
    if seeds2d is not None:
        # Show results
        colormap = copy.copy(plt.cm.get_cmap('brg'))
        colormap._init()
        colormap._lut[0, 3] = 0

        plt.imshow(seeds2d, cmap=colormap, interpolation='none')


def __select_slices(data, axis, slice_step):
    if axis == 0:
        data = data[::slice_step, :, :]
    if axis == 1:
        data = data[:, ::slice_step, :]
    if axis == 2:
        data = data[:, :, ::slice_step]
    return data


def _import_data(data, axis, slice_step):
    """
    import ndarray or SimpleITK data
    """
    try:
        import SimpleITK as sitk
        if type(data) is sitk.SimpleITK.Image:
            data = sitk.GetArrayFromImage(data)
    except:
        pass

    data = __select_slices(data, axis, slice_step)
    return data


# self.rect.figure.canvas.draw()

    # return data

class sed3qt(QtGui.QDialog):
    def __init__(self, *pars, **params):
    # def __init__(self,parent=None):
        parent = None


        QtGui.QDialog.__init__(self, parent)
        # super(Window, self).__init__(parent)
        # self.setupUi(self)
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)

# set the layout
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        # layout.addWidget(self.button)
        self.setLayout(layout)

    # def set_params(self, *pars, **params):
        # import sed3.sed3

        params["figure"] = self.figure 
        self.sed = sed3(*pars, **params)
        self.sed.sed3_on_close = self.callback_close
        # ed.show()
        self.output = None

    def callback_close(self, sed):
        self.output = sed
        sed.prepare_output_data()
        self.seeds = sed.seeds
        self.close()

    def get_values(self):
        return self.sed

# --------------------------tests-----------------------------
class Tests(unittest.TestCase):

    def test_t(self):
        pass

    def setUp(self):
        """ Nastavení společných proměnných pro testy  """
        datashape = [120, 85, 30]
        self.datashape = datashape
        self.rnddata = np.random.rand(datashape[0], datashape[1], datashape[2])
        self.segmcube = np.zeros(datashape)
        self.segmcube[30:70, 40:60, 5:15] = 1

        self.ed = sed3(self.rnddata)
        # ed.show()
        # selected_seeds = ed.seeds

    def test_same_size_input_and_output(self):
        """Funkce testuje stejnost vstupních a výstupních dat"""
        # outputdata = vesselSegmentation(self.rnddata,self.segmcube)
        self.assertEqual(self.ed.seeds.shape, self.rnddata.shape)

    def test_set_seeds(self):
        ''' Testuje uložení do seedů '''
        val = 7
        self.ed.set_seeds([10, 12, 13], [13, 13, 15], 3, value=val)
        self.assertEqual(self.ed.seeds[10, 13, 3], val)

    def test_prepare_overlay(self):
        ''' Testuje vytvoření rgba obrázku z labelů'''
        overlay = self.ed.prepare_overlay(self.segmcube[:, :, 6])
        onePixel = overlay[30, 40]
        self.assertTrue(all(onePixel == [1, 0, 0, 1]))

    def test_get_seed_sub(self):
        """ Testuje, jestli funkce pro vracení dat funguje správně,
        je to zkoušeno na konkrétních hodnotách
        """
        val = 7
        self.ed.set_seeds([10, 12, 13], [13, 13, 15], 3, value=val)
        seedsx, seedsy, seedsz = self.ed.get_seed_sub(val)

        found = [False, False, False]
        for i in range(len(seedsx)):
            if (seedsx[i] == 10) & (seedsy[i] == 13) & (seedsz[i] == 3):
                found[0] = True
            if (seedsx[i] == 12) & (seedsy[i] == 13) & (seedsz[i] == 3):
                found[1] = True
            if (seedsx[i] == 13) & (seedsy[i] == 15) & (seedsz[i] == 3):
                found[2] = True

        logger.debug(found)

        self.assertTrue(all(found))

    def test_get_seed_val(self):
        """ Testuje, jestli jsou správně vraceny hodnoty pro označené pixely
        je to zkoušeno na konkrétních hodnotách
        """
        label = 7
        self.ed.set_seeds([11], [14], 4, value=label)
        seedsx, seedsy, seedsz = self.ed.get_seed_sub(label)

        val = self.ed.get_seed_val(label)
        expected_val = self.ed.img[11, 14, 4]

        logger.debug(val)
        logger.debug(expected_val)

        self.assertIn(expected_val, val)


def generate_data(shp=[16, 20, 24]):
    """ Generating data """

    x = np.ones(shp)
# inserting box
    x[4:-4, 6:-2, 1:-6] = -1
    x_noisy = x + np.random.normal(0, 0.6, size=x.shape)
    return x_noisy

# --------------------------main------------------------------
if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.WARNING)
# při vývoji si necháme vypisovat všechny hlášky
    # logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
#   output configureation
    # logging.basicConfig(format='%(asctime)s %(message)s')
    logging.basicConfig(format='%(message)s')

    formatter = logging.Formatter(
        "%(levelname)-5s [%(module)s:%(funcName)s:%(lineno)d] %(message)s")
    # add formatter to ch
    ch.setFormatter(formatter)

    logger.addHandler(ch)

    # input parser
    parser = argparse.ArgumentParser(
        description='Segment vessels from liver. Try call sed3 -f lena')
    parser.add_argument(
        '-f', '--filename',
        # default = '../jatra/main/step.mat',
        default='lena',
        help='*.mat file with variables "data", "segmentation" and "threshod"')
    parser.add_argument(
        '-d', '--debug', action='store_true',
        help='run in debug mode')
    parser.add_argument(
        '-e3', '--example3d', action='store_true',
        help='run with 3D example data')
    parser.add_argument(
        '-t', '--tests', action='store_true',
        help='run unittest')
    parser.add_argument(
        '-o', '--outputfile', type=str,
        default='output.mat', help='output file name')
    args = parser.parse_args()

    if args.debug:
        logger.setLevel(logging.DEBUG)

    if args.tests:
        # hack for use argparse and unittest in one module
        sys.argv[1:] = []
        unittest.main()

    if args.example3d:
        data = generate_data()
    elif args.filename == 'lena':
        from scipy import misc
        data = misc.lena()
    else:
        #   load all
        mat = scipy.io.loadmat(args.filename)
        logger.debug(mat.keys())

        # load specific variable
        dataraw = scipy.io.loadmat(args.filename, variable_names=['data'])
        data = dataraw['data']

        # logger.debug(matthreshold['threshold'][0][0])

        # zastavení chodu programu pro potřeby debugu,
        # ovládá se klávesou's','c',...
        # zakomentovat
        # pdb.set_trace();

        # zde by byl prostor pro ruční (interaktivní) zvolení prahu z
        # klávesnice
        # tě ebo jinak

    pyed = sed3(data)
    output = pyed.show()

    scipy.io.savemat(args.outputfile, {'data': output})
    pyed.get_seed_val(1)
