import glob

from IPython.display import Image
from ipywidgets import \
    Button, \
    Dropdown, \
    IntSlider, \
    HTML, \
    Image as ImageWidget, \
    HBox, \
    VBox

from collections import \
    OrderedDict, \
    defaultdict
import itertools
import os
import re
import six

def get_storage(plot_type):
    if plot_type == 'image':
        storage = image_storage
    elif plot_type == 'radial-profile':
        storage = profile_storage
    else:
        raise RuntimeError
    return storage


def create_image(sim_name, plot_type, file_index, field_type, field_name):
    storage = get_storage(plot_type)
    try:
        image_filename = \
            storage[sim_name][filenames[file_index]][field_type][field_name]
    except KeyError:
        image_filename = \
            'http://upload.wikimedia.org/wikipedia/commons/c/ca/1x1.png'
    return Image(image_filename, embed=True).data


def initialize_storage(storage):
    for sn in used_sim_names:
        storage[sn] = OrderedDict()


def movie_callback(widget):
    cached_value = file_control.value
    storage = get_storage(type_control.value)
    for i in range(len(storage[sim_control.value].keys())):
        file_control.value = i
    file_control.value = cached_value


def type_trait_callback(name, old_value, new_value):
    storage = get_storage(new_value)
    saved_value = field_dropdown.value
    possible_field_names = sorted(
        storage[sim_control.value][filenames[file_control.value]][field_type_dropdown.value].keys())
    field_dropdown.options = OrderedDict((
        (override_field_names[k] or k.replace('-', ' ').title(), k)
        for k in possible_field_names))
    if saved_value in possible_field_names:
        field_dropdown.value = saved_value
    else:
        field_dropdown.value = possible_field_names[0]
    image_widget.value = \
        create_image(sim_control.value, new_value,
                     file_control.value, field_type_dropdown.value,
                     field_dropdown.value)


def slider_trait_callback(name, old_value, new_value):
    image_widget.value = \
        create_image(sim_control.value, type_control.value,
                     new_value, field_type_dropdown.value, field_dropdown.value)
    file_time_display.value = '%s Myr' % new_value


def slider_displayed_callback(widget):
    image_widget.value = \
        create_image(sim_control.value, type_control.value,
                     widget.value, field_type_dropdown.value,
                     field_dropdown.value)
    file_time_display.value = '%s Myr' % widget.value


def field_name_trait_callback(name, old_value, new_value):
    image_widget.value = \
        create_image(sim_control.value, type_control.value,
                     file_control.value, field_type_dropdown.value, new_value)


def field_type_trait_callback(name, old_value, new_value):
    storage = get_storage(type_control.value)
    saved_value = field_dropdown.value
    possible_field_names = sorted(
        storage[sim_control.value][filenames[file_control.value]][new_value].keys())
    field_dropdown.options = OrderedDict((
        (override_field_names[k] or k.replace('-', ' ').title(), k)
        for k in possible_field_names))
    if saved_value in possible_field_names:
        field_dropdown.value = saved_value
    else:
        field_dropdown.value = possible_field_names[0]
    image_widget.value = \
        create_image(sim_control.value, type_control.value,
                     file_control.value, new_value, field_dropdown.value)


def sim_dropdown_trait_callback(name, old_value, new_value):
    image_widget.value = \
        create_image(new_value, type_control.value,
                     file_control.value, field_type_dropdown.value,
                     field_dropdown.value)
    file_control.max = len(image_storage[new_value])-1

override_field_names = defaultdict(lambda: None)
override_field_names['c-eff'] = 'Effective Sound Speed'

field_type_names = OrderedDict(
    [
        ('gas', six.text_type('Gas')),
        ('star_formation', six.text_type('Star Formation')),
        ('stars', six.text_type('Stars')),
        ('formed_stars', six.text_type('Formed Stars')),
        ('young_stars', six.text_type('Young Stars')),
        ('rot', six.text_type('Rotation')),
    ]
)

fiducial_sim_name = 'feedback_20pc_lgf'

used_sim_names = [os.path.basename(n) for n in glob.glob("data/*feedback*")]

search_directories = ['data' + '/' + sn + '/' for sn in used_sim_names]

glob_pattern = 'covering_grids/plots/*.png'

plot_filenames = sorted(
    itertools.chain(*[glob.glob(sd+glob_pattern) for sd in search_directories]))

image_storage = OrderedDict()
profile_storage = OrderedDict()

initialize_storage(image_storage)
initialize_storage(profile_storage)

for file_path in plot_filenames:
    split_path = file_path.split(os.path.sep)
    filename = split_path[-1]
    sim_dir = split_path[1]
    basename = os.path.splitext(os.path.basename(filename))[0]
    ddbase, plot_type, field_type, field_name = re.split(
        '(?<!formed)(?<!young)(?<!star)_|_(?!star)(?!formation)(?!stars)',
        basename)
    field_type = field_type
    field_name = field_name

    storage = get_storage(plot_type)

    name = sim_dir

    if ddbase not in storage[name]:
        storage[name][ddbase] = {}
    if field_type not in storage[name][ddbase]:
        storage[name][ddbase][field_type] = {}
    if field_name not in storage[name][ddbase][field_type]:
        storage[name][ddbase][field_type][field_name] = {}
    storage[name][ddbase][field_type][field_name] = file_path

filenames = []

for sim in image_storage:
    filenames += list(image_storage[sim].keys())

filenames = sorted(list(set(filenames)))

sim_names = list(image_storage.keys())
field_types = list(image_storage[fiducial_sim_name][filenames[0]].keys())

field_names = OrderedDict()

for field_type in field_types:
    field_names[field_type] = sorted(list(
        image_storage[fiducial_sim_name][filenames[0]][field_type].keys()))

field_types = OrderedDict(((field_type_names[ft], ft) for ft in field_types))

field_type_dropdown = Dropdown(options=field_types, value='gas')
field_type_dropdown.margin = '8px'

field_name_mapping = OrderedDict(
    ((override_field_names[fn] or fn.replace('-', ' ').title(), fn)
     for fn in field_names[field_type_dropdown.value]))

field_dropdown = Dropdown(options=field_name_mapping,
                          value=('surface-density'))
field_dropdown.margin = '8px'

sim_control = Dropdown(options=list(image_storage.keys()),
                       value=fiducial_sim_name)
sim_control.margin = '8px'

type_control = Dropdown(options=OrderedDict(
    [('Image', 'image'), ('Radial Profile', 'radial-profile')]), value='image')
type_control.margin = '8px'

top_buttons = HBox(children=[sim_control, type_control, field_type_dropdown, field_dropdown])
top_button_container = HBox(children=[top_buttons])

top_button_container.pack = 'center'
top_button_container.margin = 'auto'

image_widget = ImageWidget()
image_widget.width = '100%'

movie_control = Button(description='Movie')
movie_control.margin = '10px'

file_control = IntSlider(min=0, max=len(image_storage[fiducial_sim_name])-1, readout=False)
file_control.margin = '10px'

file_time_display = HTML(value='')
file_time_display.width = '100px'
file_time_display._dom_classes = ('file_time_display',)
file_time_display._css = (('.file_time_display', 'margin-top', '13px'),)

slider_container = HBox(children=[movie_control, file_control, file_time_display])
bottom_button_container = HBox(children=[slider_container])

bottom_button_container.pack = 'center'
bottom_button_container.margin = 'auto'

galaxy_widget = VBox(
    children=[top_button_container, image_widget, bottom_button_container])
galaxy_widget.pack = 'center'

file_control.on_trait_change(slider_trait_callback, 'value')
file_control.on_displayed(slider_displayed_callback)

field_dropdown.on_trait_change(field_name_trait_callback, 'value')
field_type_dropdown.on_trait_change(field_type_trait_callback, 'value')

sim_control.on_trait_change(sim_dropdown_trait_callback, 'value')

type_control.on_trait_change(type_trait_callback, 'value')

movie_control.on_click(movie_callback)
