__author__ = 'ces55739', 'phg49389'

import os
import xml.etree.ElementTree as Et
from wtforms.widgets import HTMLString

# TODO: submit via POST through AJAX from the form to Python directly; bypass JS
# TODO: finish implementing the Submit functions
# TODO: implement loading screen while file permissions crunches
# TODO: return success page when submitted
# Later, if feasible
# TODO: metadata?
# TODO: find a way to minify dynamic_scripts and dynamic_style in the constructor (rJSmin and rCSSmin look really promising, but have errors during local install)
# Relevant to this last one: http://stackoverflow.com/questions/22603195/fatal-error-include-stdio-h-generated-after-pip-install-mysql-python-comma

class DataDefinitionBuilder:
    def __init__(self, my_cascade, users_username):
        self.storage = ""
        self.cascade = my_cascade  # By passing in a copy of Cascade instead of creating one, it allows Cascade to call this class
        self.user_name = users_username  # Passed on to interfacer.py by being dynamically built into the HTML/JS
        self.num_multiple_tags_seen = 0  # Used to make sure all ids being assigned to divs are unique; those ids are use later by the JS
        self.radio_group_counter = 0
        self.my_form = ""

    # This method is called initially after the data definition has been selected. It turns an XML ElementTree structure
    # into a usable list of lists. When a parent or leaf is encountered, a tuple is added consisting of the tag name,
    # attributes, and the number of children that it may have. Then, a list of all its children is added, and so on and
    # so forth, thus making the list of lists mimic the XML structure, but is still easier to parse later.
    def recursive_structure_build(self, xml):
        to_return = []
        if len(list(xml)) > 0:
            for elem in xml:
                if 'type' in elem.attrib and (elem.attrib['type'] == "dropdown" or elem.attrib['type'] == "radiobutton"):
                    list_of_options = (elem.tag, elem.attrib, 0) + ([el.attrib['value'] for el in list(elem)],)
                    to_return.append(list_of_options)
                else:
                    children_to_append = self.recursive_structure_build(elem)
                    if len(children_to_append) > 0:
                        to_return.append((elem.tag, elem.attrib, len(children_to_append)))
                        to_return.append(children_to_append)
                    else:
                        to_return.append((elem.tag, elem.attrib, 0))
        return to_return

    # This method is analagous to structure_build, in that it parses through the given structuredDataNodes, and extracts
    # the data into tuples while maintaining the structure. If the given structuredDataNode has any children, it adds
    # the children as a list directly after the parent tuple.
    def recursive_data_build(self, structured_data_node_list):
        to_return = []
        for data_node in structured_data_node_list:
            if data_node['type'] == "asset":
                if data_node['assetType'] == "page":
                    path_to_use = str(data_node['pagePath'])
                elif data_node['assetType'] == "block":
                    path_to_use = str(data_node['blockPath'])
                else:
                    path_to_use = str(data_node['filePath'])
                tuple_to_append = (str(data_node['type']), str(data_node['identifier']), path_to_use)
            elif data_node['type'] == "group":
                tuple_to_append = (str(data_node['type']), str(data_node['identifier']), None)
            else:
                tuple_to_append = (str(data_node['type']), str(data_node['identifier']), str(data_node['text']))
            to_return.append(tuple_to_append)
            if data_node['structuredDataNodes'] is not None:
                to_return.append(self.recursive_data_build(data_node['structuredDataNodes']['structuredDataNode']))
        return to_return

    # This method is a bit complicated, but the idea behind it is this: the data definition defines how it will be
    # structured, but for any given multiple group or element in the DD, a page or block could have more elements. This
    # method takes the structured list of lists made by structure_build above, and then duplicates multiple elements as
    # necessary to make the structured list of lists match the page that's going to be edited.
    def make_structure_mimic_data(self, structure, data):
        part_a = []
        part_b = []
        for i in range(len(structure)):
            if isinstance(structure[i], tuple):
                num_instances_of_this_multiple = 1
                if 'multiple' in structure[i][1]:
                    num_instances_of_this_multiple = len(
                        [el for el in data if isinstance(el, tuple) and el[1] == structure[i][1]['identifier']])
                if structure[i][2] > 0:  # Means it is a parent with children to grab
                    batch_to_insert = structure[i:i + 2]
                else:  # Means it's a multiple-line textfield or some other stand-alone element
                    batch_to_insert = [structure[i]]
                for j in range(num_instances_of_this_multiple):
                    if j > 0:
                        print "Adding", structure[i][1]['identifier']
                    for k in range(len(batch_to_insert)):
                        part_a.append(batch_to_insert[k])
        # Now that this level of structure mimics the data at this level, go a level deeper!
        for i in range(len(part_a)):
            if isinstance(part_a[i], tuple):
                part_b.append(part_a[i])
            else:
                part_b.append(self.make_structure_mimic_data(part_a[i], data[i]))
        return part_b

    # This method takes in a structured list of lists, and appends the appropriate HTML code onto the form that's being
    # built, in order of how it should go.
    def build_empty_form(self, structure, depth=1, close_div=False):
        group_open = False
        indent = depth * "    "
        looking_at_group_of_multiples = False
        name_of_mult_elem = ""
        starting_multiple_counter = self.num_multiple_tags_seen
        for i in range(len(structure)):
            self.my_form += indent
            if isinstance(structure[i], tuple):

                type_of_tag = structure[i][0]
                identifier = structure[i][0]
                if 'identifier' in structure[i][1]:
                    identifier = structure[i][1]['identifier']
                if 'label' in structure[i][1]:
                    label = structure[i][1]['label']
                else:
                    label = identifier

                parameters = ""
                required_text = ""
                if 'required' in structure[i][1]:
                    required_text = " <span><small style=\"color:red\">*Required</small></span>"
                    parameters += "required=\"required\" "


                if not looking_at_group_of_multiples and 'multiple' in structure[i][1] and structure[i][1][
                    'multiple'] == "true":
                    looking_at_group_of_multiples = True
                    name_of_mult_elem = structure[i][1]['label']
                    self.my_form += """<div id="ext%(0)s" class="noborder">\n""" % {'0': self.num_multiple_tags_seen}
                    self.num_multiple_tags_seen += 1
                    self.my_form += indent

                if looking_at_group_of_multiples and 'multiple' not in structure[i][1]:
                    looking_at_group_of_multiples = False
                    # Close the invisible div
                    self.my_form += """%s</div>\n""" % indent

                    self.num_multiple_tags_seen -= 1

                    # Add the button which will add more instances
                    self.my_form += """%(3)s<input type="button" id="%(0)s" value="%(1)s" onclick="%(2)s"/></input>\n""" \
                                    % {'0': "addTo_ext" + str(self.num_multiple_tags_seen),
                                       '1': "Add " + name_of_mult_elem,
                                       '2': "addAnotherTo_ext" + str(self.num_multiple_tags_seen) + "();",
                                       '3': indent}

                    # Add the button that will remove instances
                    self.my_form += """%(3)s<input type="button" id="%(0)s" value="%(1)s" onclick="%(2)s"></input><br/><br/>\n""" \
                                    % {'0': "removeFrom_ext" + str(self.num_multiple_tags_seen),
                                       '1': "Remove last item in list",
                                       '2': "removeLastDivIn_ext" + str(self.num_multiple_tags_seen) + "();",
                                       '3': indent}

                    self.add_scripts_for("ext" + str(self.num_multiple_tags_seen), indent)
                    # print "Closing pair #" + str(self.num_multiple_tags_seen)
                    self.num_multiple_tags_seen += 1

                if type_of_tag == "text":
                    # wysiwyg or textarea
                    if ('wysiwyg' in structure[i][1] and structure[i][1]['wysiwyg']) \
                            or ('multi-line' in structure[i][1] and structure[i][1]['multi-line']):
                        if 'size' in structure[i][1]:
                            parameters += "maxlength=\""+structure[i][1]['size']+"\" "
                        self.my_form += """<label for="%(0)s">%(1)s%(4)s</label><br/>\n%(2)s<textarea id="%(0)s" class="ckeditor" %(3)s></textarea><br/>\n""" \
                                        % {'0': identifier, '1': label, '2': indent, '3': parameters, '4': required_text}
                    elif 'type' in structure[i][1] and structure[i][1]['type'] == "dropdown":
                        # get all dropdown-items
                        self.my_form += """<label for="%(0)s">%(1)s%(3)s</label><br/>\n%(2)s<select id="%(0)s" %(4)s>\n""" \
                                        % {'0': identifier, '1': label, '2': indent, '3': required_text, '4': parameters}
                        drop_list = structure[i][3]
                        for value in drop_list:
                            self.my_form += """%(1)s<option value="%(0)s">%(0)s</option>\n""" % {'0': value,
                                                                                                 '1': indent + "    "}
                        self.my_form += """%s</select><br/>\n""" % indent
                    elif 'type' in structure[i][1] and structure[i][1]['type'] == "radiobutton":
                        # get all dropdown-items
                        self.my_form += """ <label for="%(0)s">%(1)s%(3)s</label><br/>\n
                                            %(2)s<ul id="%(0)s">\n""" \
                                        % {'0': identifier, '1': label, '2': indent, '3': required_text}
                        radio_list = structure[i][3]
                        for value in radio_list:
                            self.my_form += """
%(3)s<li>
%(4)s<input id="%(0)s-%(1)s" type="radio" name="%(5)s" value="%(2)s" %(6)s></input>\n
%(4)s<label for="%(0)s-%(1)s">%(2)s</label>\n
%(3)s</li>\n""" % {'0': identifier, '1': radio_list.index(value), '2': value, '3': indent, '4': indent + "    ", '5': "radio_group-"+str(self.radio_group_counter), '6': parameters}
                        # print "About to increment radio counter from", self.radio_group_counter
                        self.radio_group_counter += 1
                        self.my_form += """%s</ul>\n""" % indent
                        # print "End of radio group"
                    else:
                        if 'size' in structure[i][1]:
                            parameters += "maxlength=\""+structure[i][1]['size']+"\" "
                        self.my_form += """<label for="%(0)s">%(1)s%(4)s</label><br/>\n%(2)s<input id="%(0)s" type="text" value="" size="20" %(3)s></input><br/>\n""" \
                                        % {'0': identifier, '1': label, '2': indent, '3': parameters, '4':required_text}
                elif type_of_tag == "asset":
                    # This line is what originally sets the type of file to be filtered by
                    # data-def-form.html's fetchArrayFromCascade() and constructInternalDisplay()

                    prefix = "asset_"

                    if structure[i][1]['type'] == "page":
                        prefix +="p_"
                    elif structure[i][1]['type'] == "file":
                        prefix +="f_"
                    elif structure[i][1]['type'] == "block":
                        prefix +="b_"

                    self.my_form += """<label for="%(0)s">%(3)s%(5)s</label><br/>\n%(4)s<input type="button" id="%(0)s" value="%(1)s" onclick="%(2)s" %(6)s/><br/>\n""" \
                                    % {'0': prefix + identifier,
                                       '1': "Choose an asset (" + str(structure[i][1]['type']) + ")",
                                       '2': "fetchArrayFromCascade('','" +
                                            structure[i][1][
                                                'type'] + "', '" + self.user_name + "', '" + prefix + identifier + "');",
                                       '3': label,
                                       '4': indent,
                                       '5': required_text,
                                       '6': parameters}
                elif type_of_tag == "group":
                    # %(1)s    <input type="hidden" id="group_%(2)s" value="%(0)s"></input>\n
                    self.my_form += """<div class="border">\n%(1)s    <h2>%(0)s</h2>\n""" \
                                    % {'0': label, '1': indent, '2': identifier}
                    group_open = True
            else:
                self.build_empty_form(structure[i], depth + 1, group_open)
                group_open = False
        if looking_at_group_of_multiples:  # Catch any un-closed multiples
            # Close the invisible div
            self.my_form += """%s</div>\n""" % indent

            # Add the button which will add more instances
            self.my_form += """%(3)s<input type="button" id="%(0)s" value="%(1)s" onclick="%(2)s"></input>\n""" \
                            % {'0': "addTo_ext" + str(starting_multiple_counter),
                               '1': "Add " + name_of_mult_elem,
                               '2': "addAnotherTo_ext" + str(starting_multiple_counter) + "();",
                               '3': indent}

            # Add the button that will remove instances
            self.my_form += """%(3)s<input type="button" id="%(0)s" value="%(1)s" onclick="%(2)s"></input><br/><br/>\n""" \
                            % {'0': "removeFrom_ext" + str(starting_multiple_counter),
                               '1': "Remove last item in list",
                               '2': "removeLastDivIn_ext" + str(starting_multiple_counter) + "();",
                               '3': indent}

            self.add_scripts_for("ext" + str(starting_multiple_counter), indent)
        if close_div:
            self.my_form += (depth - 1) * "    " + "</div><br/>\n"

    # This method follows the exact same logic as build_empty_structure, but it uses the data (whose structure it
    # already mimics) to insert pre-filled data into the page
    def build_form_with_data(self, structure, data, depth=1, close_div=False):
        group_open = False
        indent = depth * "    "
        looking_at_group_of_multiples = False
        name_of_mult_elem = ""
        starting_multiple_counter = self.num_multiple_tags_seen
        for i in range(len(structure)):
            self.my_form += indent
            if isinstance(structure[i], tuple):

                type_of_tag = structure[i][0]
                identifier = structure[i][0]
                if 'identifier' in structure[i][1]:
                    identifier = structure[i][1]['identifier']
                if 'label' in structure[i][1]:
                    label = structure[i][1]['label']
                else:
                    label = identifier

                parameters = ""
                required_text = ""
                if 'required' in structure[i][1]:
                    required_text = " <span><small style=\"color:red\">*Required</small></span>"
                    parameters += "required=\"required\" "

                if not looking_at_group_of_multiples and 'multiple' in structure[i][1] and structure[i][1][
                    'multiple'] == "true":
                    looking_at_group_of_multiples = True
                    name_of_mult_elem = structure[i][1]['label']
                    self.my_form += """<div id="ext%(0)s" class="noborder">\n""" % {'0': self.num_multiple_tags_seen}
                    self.num_multiple_tags_seen += 1
                    self.my_form += indent

                if looking_at_group_of_multiples and 'multiple' not in structure[i][1]:
                    looking_at_group_of_multiples = False
                    # Close the invisible div
                    self.my_form += """%s</div>\n""" % indent

                    self.num_multiple_tags_seen -= 1

                    # Add the button which will add more instances
                    self.my_form += """%(3)s<input type="button" id="%(0)s" value="%(1)s" onclick="%(2)s"></input>\n""" \
                                    % {'0': "addTo_ext" + str(self.num_multiple_tags_seen),
                                       '1': "Add " + name_of_mult_elem,
                                       '2': "addAnotherTo_ext" + str(self.num_multiple_tags_seen) + "();",
                                       '3': indent}

                    # Add the button that will remove instances
                    self.my_form += """%(3)s<input type="button" id="%(0)s" value="%(1)s" onclick="%(2)s"></input><br/><br/>\n""" \
                                    % {'0': "removeFrom_ext" + str(self.num_multiple_tags_seen),
                                       '1': "Remove last item in list",
                                       '2': "removeLastDivIn_ext" + str(self.num_multiple_tags_seen) + "();",
                                       '3': indent}

                    self.add_scripts_for("ext" + str(self.num_multiple_tags_seen), indent)
                    self.num_multiple_tags_seen += 1

                # Default to None, which just won't render
                if type_of_tag == "text":
                    # wysiwyg or textarea
                    if ('wysiwyg' in structure[i][1] and structure[i][1]['wysiwyg']) \
                            or ('multi-line' in structure[i][1] and structure[i][1]['multi-line']):

                        if 'size' in structure[i][1]:
                            parameters += "maxlength=\""+structure[i][1]['size']+"\" "
                        if data[i][2] == "None":
                            data_to_display = ""
                        else:
                            data_to_display = data[i][2]
                        self.my_form += """<label for="%(0)s">%(1)s%(4)s</label><br/>\n%(2)s<textarea id="%(0)s" class="ckeditor" %(5)s>%(3)s</textarea><br/>\n""" \
                                        % {'0': identifier, '1': label, '2': indent, '3': data_to_display, '4': required_text, '5': parameters}
                    elif 'type' in structure[i][1] and structure[i][1]['type'] == "dropdown":
                        # get all dropdown-items
                        self.my_form += """<label for="%(0)s">%(1)s %(3)s</label><br/>\n%(2)s<select id="%(0)s" %(4)s>\n""" \
                                        % {'0': identifier, '1': label, '2': indent, '3': required_text, '4': parameters}
                        drop_list = structure[i][3]
                        for value in drop_list:
                            if value == data[i][2]:
                                self.my_form += """%(1)s<option value="%(0)s" selected="true">%(0)s</option>\n""" % {
                                    '0': value, '1': indent + "    "}
                            else:
                                self.my_form += """%(1)s<option value="%(0)s">%(0)s</option>\n""" % {'0': value,
                                                                                                     '1': indent + "    "}
                        self.my_form += """%s</select><br/>\n""" % indent
                    elif 'type' in structure[i][1] and structure[i][1]['type'] == "radiobutton":
                        # get all dropdown-items
                        self.my_form += """<label for="%(0)s">%(1)s %(3)s</label><br/>\n
                                            %(2)s<ul id="%(0)s">\n""" \
                                        % {'0': identifier, '1': label, '2': indent, '3': required_text}
                        radio_list = structure[i][3]
                        for value in radio_list:
                            if value == data[i][2]:
                                self.my_form += """
%(3)s<li>
%(4)s<input id="%(0)s-%(1)s" type="radio" value="%(2)s" checked="true" %(5)s></input>\n
%(4)s<label for="%(0)s-%(1)s">%(2)s</label>\n
%(3)s</li>\n""" % {'0': identifier, '1': i, '2': value, '3': indent, '4': indent + "    ", '5': parameters}
                            else:
                                self.my_form += """
%(3)s<li>
%(4)s<input id="%(0)s-%(1)s" type="radio" value="%(2)s" %(5)s></input>\n
%(4)s<label for="%(0)s-%(1)s">%(2)s</label>\n
%(3)s</li>\n""" % {'0': identifier, '1': i, '2': value, '3': indent, '4': indent + "    ", '5': parameters}
                        self.my_form += """%s</ul>\n""" % indent
                    else:
                        if data[i][2] == "None":
                            data_to_display = ""
                        else:
                            data_to_display = data[i][2]
                        self.my_form += """<label for="%(0)s">%(1)s %(4)s</label><br/>\n%(2)s<input id="%(0)s" type="text" value="%(3)s" size="20" %(5)s></input><br/>\n""" \
                                        % {'0': identifier, '1': label, '2': indent, '3': data_to_display, '4': required_text, '5': parameters}
                elif type_of_tag == "asset":
                    # This line is what originally sets the type of file to be filtered by
                    # data-def-form.html's fetchArrayFromCascade() and constructInternalDisplay()

                    prefix = "asset_"

                    if structure[i][1]['type'] == "page":
                        prefix +="p_"
                    elif structure[i][1]['type'] == "file":
                        prefix +="f_"
                    elif structure[i][1]['type'] == "block":
                        prefix +="b_"

                    self.my_form += """<label for="%(0)s">%(3)s</label><br/>\n%(4)s<input type="button" id="%(0)s" value="%(1)s" onclick="%(2)s"/><br/>\n""" \
                                    % {'0': prefix + identifier,
                                       '1': data[i][2],
                                       '2': "fetchArrayFromCascade('','" +
                                            structure[i][1][
                                                'type'] + "', '" + self.user_name + "', '" + prefix + identifier + "');",
                                       '3': label,
                                       '4': indent}
                elif type_of_tag == "group":
                    # %(1)s    <input type="hidden" id="group_%(2)s" value="%(0)s"></input>\n
                    self.my_form += """<div class="border">\n%(1)s    <input type="hidden" id="group_%(2)s" value="%(0)s"></input>\n%(1)s    <h2>%(0)s</h2>\n""" \
                                    % {'0': label, '1': indent, '2': identifier}
                    group_open = True
            else:
                self.build_form_with_data(structure[i], data[i], depth + 1, group_open)
                group_open = False
        if looking_at_group_of_multiples:  # Catch any un-closed multiples
            # Close the invisible div
            self.my_form += """%s</div>\n""" % indent

            # Add the button which will add more instances
            self.my_form += """%(3)s<input type="button" id="%(0)s" value="%(1)s" onclick="%(2)s"></input>\n""" \
                            % {'0': "addTo_ext" + str(starting_multiple_counter),
                               '1': "Add " + name_of_mult_elem,
                               '2': "addAnotherTo_ext" + str(starting_multiple_counter) + "();",
                               '3': indent}

            # Add the button that will remove instances
            self.my_form += """%(3)s<input type="button" id="%(0)s" value="%(1)s" onclick="%(2)s"></input><br/><br/>\n""" \
                            % {'0': "removeFrom_ext" + str(starting_multiple_counter),
                               '1': "Remove last item in list",
                               '2': "removeLastDivIn_ext" + str(starting_multiple_counter) + "();",
                               '3': indent}

            self.add_scripts_for("ext" + str(starting_multiple_counter), indent)
        if close_div:
            self.my_form += depth * "    " + """<input type="hidden" id="group_close" value="Ignore this"></input>\n"""
            self.my_form += (depth - 1) * "    " + "</div><br/>\n"

    # This method is all about the meta-programming. This script tag needs to be put in every time that there is a
    # multiple element so that the buttons work dynamically. These meta-programming methods are why the names are
    # standardized to ext# and also why the num_multiple_tags_seen counter exists; to make sure that these meta-methods
    # never overlap on which elements to edit.
    def add_scripts_for(self, id_to_work_with, indent):
        self.my_form += """
%(1)s<script>
%(1)s    var %(0)s_internal_code = document.getElementById("%(0)s").firstElementChild.outerHTML.replace(/^\s+|\s+$/gm, ' ');
%(1)s    var %(0)s_instance_counter = document.getElementById("%(0)s").children.length/2;
%(1)s    if (2 > %(0)s_instance_counter) {
%(1)s        document.getElementById("removeFrom_%(0)s").disabled = true;
%(1)s    }
%(1)s
%(1)s    function addAnotherTo_%(0)s() {
%(1)s        var arr_returned = incrementIDs(%(0)s_internal_code, %(0)s_instance_counter);
%(1)s        document.getElementById("%(0)s").insertAdjacentHTML('beforeend', arr_returned[0]);
%(1)s        for (var i = arr_returned.length; i > 1; i--) {
%(1)s            document.body.appendChild(arr_returned[arr_returned.length - i + 1]);
%(1)s        }
%(1)s        var text_areas = document.getElementById("%(0)s").children[document.getElementById("%(0)s").children.length-2].getElementsByTagName('textarea');
%(1)s        if(text_areas.length > 0){
%(1)s           for(var i = text_areas.length-1; i > -1; i--){
%(1)s               CKEDITOR.replace(text_areas[i]);
%(1)s           }
%(1)s        }
%(1)s        %(0)s_instance_counter++;
%(1)s        if (%(0)s_instance_counter > 1) {
%(1)s            document.getElementById("removeFrom_%(0)s").disabled = false;
%(1)s        }
%(1)s    }
%(1)s
%(1)s    function removeLastDivIn_%(0)s() {
%(1)s        if (%(0)s_instance_counter > 1) {
%(1)s            var parent = document.getElementById("%(0)s");
%(1)s            for(var i = 2; i > 0; i--) {
%(1)s                parent.children[parent.children.length-1].remove();
%(1)s            }
%(1)s           %(0)s_instance_counter--;
%(1)s            if (2 > %(0)s_instance_counter) {
%(1)s                document.getElementById("removeFrom_%(0)s").disabled = true;
%(1)s            }
%(1)s        }
%(1)s    }
%(1)s</script>\n""" % {'0': id_to_work_with, '1': indent}

    def add_header(self, new_or_edit):
        # This is the start of HTML div that gets dynamically built and then returned. Both creates and edits use this opening.

        path_name = os.path.dirname(os.path.realpath(__file__))
        # print path_name
        with open(path_name+"/static/dynamic_scripts.js", "r") as script_file:
            scripts = script_file.read()
        with open(path_name+"/static/dynamic_style.css", "r") as style_file:
            styling = style_file.read()
        # Note: the CKEditor references where it is in Tinker
        if new_or_edit:  # new form
            ckeditor_path = "../../../static/ckeditor/ckeditor.js"
        else:  # edit form
            ckeditor_path = "../../../../static/ckeditor/ckeditor.js"

        self.my_form = """
<div>
    <style>
        %(0)s
    </style>
    <script src="http://ajax.googleapis.com/ajax/libs/jquery/2.1.0/jquery.js"></script>
    <script src="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/js/bootstrap.min.js"></script>
    <script>
        %(1)s
    </script>
    <script src="%(2)s"></script>

    <!-- Modal -->
    <div class="modal fade" id="myModal" role="dialog">
        <div class="modal-dialog">

            <!-- Modal content-->
            <div class="modal-content">
                <div class="modal-header">
                    <h3 class="modal-title">Choose an asset</h3>
                </div>
                <div class="modal-body" id="divToAddTableTo">
                    <p>Placeholder text that should never be seen.</p>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-default" data-dismiss="modal">Cancel</button>
                </div>
            </div>

        </div>
    </div>

    <form id="datadefform" enctype="multipart/form-data" method="post" action="JavaScript:submitForm()">
""" % {'0': styling, '1': scripts, '2': ckeditor_path}

    # This is the method that is called externally by Cascade Connector when someone wants to make a new page or block
    # from an existing data definition. First, it gets the DD from Cascade, grabs the XML version of it, turns that XML
    # into a String, then that String gets parsed into an ElementTree. That ET then gets turned into a structure, which
    # is then turned into the HTML div which gets returned.
    def build_data_def(self, data_def_id):
        self.add_header(True)
        dd = self.cascade.read(data_def_id, "datadefinition")
        dd = dd['asset']['dataDefinition']['xml']

        # print dd

        dd = dd.split('\n')
        structure = ""
        for line in dd:
            line = line.strip()
            structure += str(line)
        xml = Et.fromstring(structure)

        structure = self.recursive_structure_build(xml)
        self.build_empty_form(structure)

        self.my_form += """%(0)s<hr/>\n%(0)s<input type="submit" value="Submit"/>\n    </form>\n</div>""" % {
            '0': "    "}
        return HTMLString(self.my_form)

    # Similar to build_data_def, this method is called externally by Cascade Connector when editing an existing page or
    # block based off of an existing data definition. First, it gets the page, then extracts what DD to use, then
    # continues building it similar to an empty one. Once the structure is made, it make the structure mimic the data
    # structure given to it, then builds the div to return with the data pre-filled in.
    def edit_page_built_from_data_def(self, page_id, page_type):
        self.add_header(False)
        dd = self.cascade.read(page_id, page_type)

        self.storage = (dd['asset']['xhtmlDataDefinitionBlock']['name'],
                        dd['asset']['xhtmlDataDefinitionBlock']['siteId'],
                        dd['asset']['xhtmlDataDefinitionBlock']['parentFolderPath'],
                        dd['asset']['xhtmlDataDefinitionBlock']['metadataSetPath'],
                        "contentTypePath",  # TODO: find these two values
                        "configurationSetPath",
                        dd['asset']['xhtmlDataDefinitionBlock']['metadata'],
                        dd['asset']['workflowConfiguration'])

        # print "STORAGE:"
        # print self.storage

        dd = dd['asset']['xhtmlDataDefinitionBlock']['structuredData']

        # print dd

        data_def_id = dd['definitionId']
        dd = dd['structuredDataNodes']['structuredDataNode']
        data = self.recursive_data_build(dd)

        # self.pretty_print(data)

        dd = self.cascade.read(data_def_id, "datadefinition")
        dd = dd['asset']['dataDefinition']['xml']

        dd = dd.split('\n')
        structure = ""
        for line in dd:
            line = line.strip()
            structure += str(line)
        xml = Et.fromstring(structure)

        structure = self.make_structure_mimic_data(self.recursive_structure_build(xml), data)
        self.build_form_with_data(structure, data)

        self.my_form += """%(0)s<hr/>\n%(0)s<input type="submit" value="Submit"/>\n    </form>\n</div>""" % {
            '0': "    "}

        return HTMLString(self.my_form)

    # This method, once finished, will construct an asset, then have Cascade either create it or edit it appropriately.
    # Still need to finish the methods below before this one will work.
    def submit_form(self, form_contents, submit_new):
        print "Submit has been called in dynamic_data_def"
        data = [(elem.split("=", 1)[0], elem.split("=", 1)[1]) for elem in form_contents.split("`")]
        data_structure = self.recursively_create_structure_for_data_nodes(data)
        structured_data_nodes = self.turn_data_structure_into_nodes(data_structure)
        # self.pretty_print(structured_data_nodes)

        asset = {
            'page': {
                'name': self.storage[0],
                'siteId': self.storage[1],
                'parentFolderPath': self.storage[2],
                'metadataSetPath': self.storage[3],
                'contentTypePath': self.storage[4],
                'configurationSetPath': self.storage[5],
                'structuredData': structured_data_nodes,
                'metadata': self.storage[6]
            },
            'workflowConfiguration': self.storage[7]
        }
        print submit_new
        print "Submitted"
        # if submit_new:
        #     self.cascade.create(asset)
        # else:
        #     self.cascade.edit(asset)

    def recursively_create_structure_for_data_nodes(self, unstructured_data):
        to_return = []
        group = []
        inside_group = False
        group_counter = 0  # Will count the depth of groups being nested
        for datum in unstructured_data:
            if "group_" in datum[0]:
                if datum[0] != "group_close":
                    if not inside_group:
                        inside_group = True
                        to_return.append(datum)
                    else:
                        group.append(datum)
                    group_counter += 1
                else:
                    group_counter -= 1
                    if group_counter == 0:
                        to_return.append(self.recursively_create_structure_for_data_nodes(group))
                        group = []
                        inside_group = False
                    else:
                        group.append(datum)
            else:
                if inside_group:
                    group.append(datum)
                else:
                    to_return.append(datum)
        return to_return

    def turn_data_structure_into_nodes(self, data_structure):
        # print "Beginning build of structuredDataNodes; there are", len(data_structure), "elements"
        structured_data = []
        for i in range(len(data_structure)):
            if isinstance(data_structure[i], tuple):  # Either element or group header; either way make a new node
                # print data_structure[i]
                if "group_" in data_structure[i][0]:
                    # It's a group; grab next element; will be a list with this group's children in it
                    ident = data_structure[i][0][6:]
                    foo = self.structured_data_node(ident, data_structure[i][1], "group", data_structure[i+1])
                else:
                    # It's data; make a structured data node with no children and add it on to the list we have
                    # print data_structure[i]
                    if "asset_" in data_structure[i][0]:
                        type_letter = data_structure[i][0][6]
                        type_of_asset = None
                        if type_letter == "p":
                            type_of_asset = "page"
                        elif type_letter == "f":
                            type_of_asset = "file"
                        elif type_letter == "b":
                            type_of_asset = "block"
                        ident = data_structure[i][0][8:]
                        foo = self.structured_data_node(ident, data_structure[i][1], type_of_asset)
                    else:
                        foo = self.structured_data_node(data_structure[i][0], data_structure[i][1])
                structured_data.append(foo)
            # Ignore the lists, as they'll be grabbed by the groups
        return structured_data

    def structured_data_node(self, node_id, text_value, node_type=None, children_list=None):
        b_path = None
        f_path = None
        p_path = None
        if not node_type:
            node_type = "text"
        else:
            if node_type == "block":
                b_path = text_value
                text_value = None
            elif node_type == "file":
                f_path = text_value
                text_value = None
            elif node_type == "page":
                p_path = text_value
                text_value = None

        if children_list:
            children_list = self.turn_data_structure_into_nodes(children_list)

        to_return = {
            'assetType': None,
            'blockId': None,
            'blockPath': b_path,
            'fileId': None,
            'filePath': f_path,
            'identifier': node_id,
            'pageId': None,
            'pagePath': p_path,
            'recycled': False,
            'structuredDataNodes': children_list,
            'symlinkId': None,
            'symlinkPath': None,
            'text': text_value,
            'type': node_type
        }
        return to_return

    def pretty_print(self, to_print, depth=0):
        if isinstance(to_print, list):
            print depth * "    " + "["
            for elem in to_print:
                if isinstance(elem, list) or isinstance(elem, dict):
                    self.pretty_print(elem, depth+1)
                else:
                    print((depth + 1) * "    " + str(elem))
            print depth * "    " + "]"
        elif isinstance(to_print, dict):
            print depth * "    " + "{"
            for key, value in to_print.iteritems():
                if isinstance(value, dict) or isinstance(value, list):
                    print (depth+1)*"    " + str(key) + " = "
                    self.pretty_print(value, depth+2)
                else:
                    print (depth+1)*"    " + str(key) + " = " + str(value)
            print depth * "    " + "}"

