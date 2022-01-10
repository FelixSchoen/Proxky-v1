import math
import os
import re
import xml.etree.ElementTree

from src.utility.util_info import info_fail
from src.utility.variables import *


def utility_split_string_along_regex(string, *matchers: ([str], str, str), standard_category="type",
                                     standard_identifier="normal"):
    # Build list of all available regex
    all_regex = []
    for triple in matchers:
        for regex in triple[0]:
            all_regex.append(regex)
    all_regex = list(dict.fromkeys(all_regex))

    working_string = string
    result = []

    while len(working_string) > 0:
        current_span = [math.inf, 0]
        current_regex = ""

        # Check which regex matches first, disregard regex that matches after already found ones
        for regex in all_regex:
            pattern = re.compile(regex)
            matches = list(pattern.finditer(working_string))
            if len(matches) > 0 and matches[0].span()[0] < current_span[0]:
                current_span = matches[0].span()
                current_regex = regex
                if current_span[0] == 0:
                    break

        # If no regex matched we are dealing with a normal string
        if current_span[0] == math.inf:
            result.append((working_string, standard_category, standard_identifier))
            working_string = ""
        else:
            # Split into two parts
            part_one = working_string[:current_span[0]]
            part_two = working_string[current_span[0]:]

            # Everything before match is normal, remove it first
            rectifier = 0
            if current_span[0] > 0:
                result.append((part_one, standard_category, standard_identifier))
                rectifier = len(part_one)

            part_one = part_two[:current_span[1] - rectifier]
            part_two = part_two[current_span[1] - rectifier:]

            # Search which regex matched and add to result
            for triple in matchers:
                if current_regex in triple[0]:
                    result.append((part_one, triple[1], triple[2]))
                    working_string = part_two
                    break

    return result


def utility_make_object_transparent(element, opacity, mode="Fill"):
    transparency = xml.etree.ElementTree.Element(mode + "TransparencySetting")
    blending = xml.etree.ElementTree.Element("BlendingSetting")
    blending.set("Opacity", str(opacity))
    transparency.append(blending)
    element.append(transparency)


def utility_change_text_color(element, color):
    for entry in element.findall(".//CharacterStyleRange"):
        entry.set("FillColor", color)


def utility_change_text_style(element, style):
    for entry in element.findall(".//CharacterStyleRange"):
        entry.set("FontStyle", style)


def utility_nested_reminder_text(text_array):
    array_to_return = []

    for element in text_array:
        if element[2] != "reminder":
            array_to_return.append(element)
        else:
            returned_array = utility_split_string_along_regex(element[0], *regex_template_mana,
                                                              standard_identifier="reminder")
            array_to_return.extend(returned_array)

    return array_to_return


def utility_file_exists(path):
    return os.path.exists(path)


def utility_vector_bounding_box(path, filename):
    tree = xml.etree.ElementTree.parse(path + "/" + filename + ".svg")
    values = tree.getroot().attrib["viewBox"].split(" ")
    return float(values[2]), float(values[3])


def utility_indesign_get_coordinates(element):
    point_top_left = element.find(".//PathPointType[1]")
    point_bottom_left = element.find(".//PathPointType[2]")
    point_top_right = element.find(".//PathPointType[4]")
    point_bottom_right = element.find(".//PathPointType[3]")

    values = point_top_left.attrib["Anchor"].split(" ")
    coordinates_top_left = float(values[0]), float(values[1])

    values = point_bottom_left.attrib["Anchor"].split(" ")
    coordinates_bottom_left = float(values[0]), float(values[1])

    values = point_top_right.attrib["Anchor"].split(" ")
    coordinates_top_right = float(values[0]), float(values[1])

    values = point_bottom_right.attrib["Anchor"].split(" ")
    coordinates_bottom_right = float(values[0]), float(values[1])

    return coordinates_top_left, coordinates_top_right, coordinates_bottom_left, coordinates_bottom_right


def utility_indesign_change_coordinates(indesign_object, x_coordinates=None, y_coordinates=None):
    top_left = indesign_object.find(".//PathPointType[1]")
    top_right = indesign_object.find(".//PathPointType[4]")
    bottom_left = indesign_object.find(".//PathPointType[2]")
    bottom_right = indesign_object.find(".//PathPointType[3]")

    for i, point in enumerate([top_left, top_right, bottom_left, bottom_right]):
        x_coordinate, y_coordinate = point.attrib["Anchor"].split(" ")
        point.attrib.pop("Anchor")
        point.attrib.pop("LeftDirection")
        point.attrib.pop("RightDirection")

        coordinates = ""

        if x_coordinates is not None:
            coordinates += str(x_coordinates[i]) + " "
        else:
            coordinates += x_coordinate + " "
        if y_coordinates is not None:
            coordinates += str(y_coordinates[i])
        else:
            coordinates += y_coordinate

        point.set("Anchor", coordinates)
        point.set("LeftDirection", coordinates)
        point.set("RightDirection", coordinates)

    return indesign_object


def utility_indesign_shift_coordinates(indesign_object, x_coordinates=None, y_coordinates=None):
    top_left = indesign_object.find(".//PathPointType[1]")
    top_right = indesign_object.find(".//PathPointType[4]")
    bottom_left = indesign_object.find(".//PathPointType[2]")
    bottom_right = indesign_object.find(".//PathPointType[3]")

    x_coordinates_set_to = []
    y_coordinates_set_to = []

    for i, point in enumerate([top_left, top_right, bottom_left, bottom_right]):
        x_coordinate, y_coordinate = point.attrib["Anchor"].split(" ")

        if x_coordinates is not None:
            x_coordinates_set_to.append(float(x_coordinate) + x_coordinates[i])
        else:
            x_coordinates_set_to.append(float(x_coordinate))
        if y_coordinates is not None:
            y_coordinates_set_to.append(float(y_coordinate) + y_coordinates[i])
        else:
            y_coordinates_set_to.append(float(y_coordinate))

    return utility_indesign_change_coordinates(indesign_object, x_coordinates=x_coordinates_set_to,
                                               y_coordinates=y_coordinates_set_to)


def utility_cardfile_to_pdf(app, card):
    cleansed_name = card.name.replace("//", "--")
    input_folder_path = f_documents + "/" + card.set.upper()
    input_file_path = input_folder_path + "/" + card.collector_number + " - " + cleansed_name + ".idml"
    output_folder_path = f_pdf + "/" + card.set.upper()
    output_file_path = output_folder_path + "/" + card.collector_number + " - " + cleansed_name + ".pdf"

    return_code = ""

    if utility_file_exists(output_file_path):
        return_code = FLAG_FILE_EXISTS

    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    myDoc = app.Open(input_file_path)

    profile = app.PreflightProfiles.Item(1)
    process = app.PreflightProcesses.Add(myDoc, profile)
    process.WaitForProcess()
    results = process.processResults

    if "None" not in results:
        # Fix errors
        script = open("src/utility/script.jsx")
        app.DoScript(script.read(), 1246973031, resize_array)

        process.WaitForProcess()
        results = process.processResults

        # Check if problems were resolved
        if "None" not in results:
            info_fail(card.name, "Error while running preflight")
            myDoc.Close(1852776480)
            return FLAG_PREFLIGHT_FAIL

    myPDFPreset = app.PDFExportPresets.Item(7)
    idPDFType = 1952403524
    myDoc.Export(idPDFType, output_file_path, False, myPDFPreset)
    myDoc.Close(1852776480)

    if return_code == "":
        return_code = FLAG_OK

    return return_code


def utility_divide_chunks(l, n):
    # looping till length l
    for i in range(0, len(l), n):
        yield l[i:i + n]


def mm_to_pt(mm):
    return mm * 2.83464566929134
