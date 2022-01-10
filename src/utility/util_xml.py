import os
import re
import xml
import xml.etree.ElementTree

from PIL import Image

from src.settings.settings import PRINT_FLAVOR_TEXT
from src.utility.util_info import info_fail
from src.utility.util_misc import does_file_exist, split_string_along_regex, handle_nested_reminder_text
from src.utility.variables import *
from src.utility.variables import image_types, regex_template_oracle, regex_template_flavor, FONT_STANDARD, \
    FONT_STANDARD_STYLE_ITALIC, regex_mana, mana_mapping


def change_object_transparency(element, opacity, mode="Fill"):
    transparency = xml.etree.ElementTree.Element(mode + "TransparencySetting")
    blending = xml.etree.ElementTree.Element("BlendingSetting")
    blending.set("Opacity", str(opacity))
    transparency.append(blending)
    element.append(transparency)


def change_text_color(element, color):
    for entry in element.findall(".//CharacterStyleRange"):
        entry.set("FillColor", color)


def change_text_style(element, style):
    for entry in element.findall(".//CharacterStyleRange"):
        entry.set("FontStyle", style)


# --------------------------
# --- InDesign Specifics ---
# --------------------------

def ind_get_bounding_box(path, filename):
    tree = xml.etree.ElementTree.parse(path + "/" + filename + ".svg")
    values = tree.getroot().attrib["viewBox"].split(" ")
    return float(values[2]), float(values[3])


def ind_get_coordinates(element):
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


def ind_change_coordinates(indesign_object, x_coordinates=None, y_coordinates=None):
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


def ind_shift_coordinates(indesign_object, x_coordinates=None, y_coordinates=None):
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

    return ind_change_coordinates(indesign_object, x_coordinates=x_coordinates_set_to,
                                  y_coordinates=y_coordinates_set_to)


def convert_card_to_pdf(app, card):
    cleansed_name = card.name.replace("//", "--")
    input_folder_path = f_documents + "/" + card.set.upper()
    input_file_path = input_folder_path + "/" + card.collector_number + " - " + cleansed_name + ".idml"
    output_folder_path = f_pdf + "/" + card.set.upper()
    output_file_path = output_folder_path + "/" + card.collector_number + " - " + cleansed_name + ".pdf"

    return_code = ""

    if does_file_exist(output_file_path):
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


# --------------
# --- Insert ---
# --------------

def insert_content(identifier, content, size=None):
    tree = xml.etree.ElementTree.parse("data/memory/Stories/Story_" + identifier + ".xml")

    if size is not None:
        parent = tree.find(".//CharacterStyleRange[1]")
        parent.set("PointSize", size)

    entry = tree.find(".//Content[1]")
    entry.text = content

    tree.write("data/memory/Stories/Story_" + identifier + ".xml")


def insert_text_element(content, font="", style="", size="8"):
    parent = xml.etree.ElementTree.Element("CharacterStyleRange")
    parent.set("PointSize", size)
    parent.set("AppliedCharacterStyle", "CharacterStyle/$ID/[No character style]")

    if font != "":
        if style != "":
            parent.set("FontStyle", style)

        properties = xml.etree.ElementTree.Element("Properties")
        applied_font = xml.etree.ElementTree.Element("AppliedFont")
        applied_font.set("type", "string")
        applied_font.text = font

        properties.append(applied_font)
        parent.append(properties)

    content_split = split_string_along_regex(content, ("\n", "type", "break"))

    for element in content_split:
        if element[1] == "type" and element[2] == "break":
            break_node = xml.etree.ElementTree.Element("Br")
            parent.append(break_node)
        else:
            content_node = xml.etree.ElementTree.Element("Content")
            content_node.text = element[0]
            parent.append(content_node)

    return parent


def insert_graphic(card, identifier_spread, identifier_field, path_file, name_file, type_file="svg",
                   mode_scale_image="fit", mode_align_vertical="center"):
    if not does_file_exist(path_file + "/" + name_file + "." + type_file):
        info_fail(card.name, "Specified graphic does not exist")
        return

    tree = xml.etree.ElementTree.parse("data/memory/Spreads/Spread_" + identifier_spread + ".xml")
    element = tree.find(".//Rectangle[@Self='" + identifier_field + "']")
    coordinates = ind_get_coordinates(element)

    # Size of the container
    size_box_x = abs(coordinates[1][0] - coordinates[0][0])
    size_box_y = abs(coordinates[2][1] - coordinates[1][1])

    # Bounding box defined in the file
    if type_file == "svg":
        xml_element = xml.etree.ElementTree.Element("SVG")
        bounding_box = ind_get_bounding_box(path_file, name_file)
    elif type_file in image_types:
        xml_element = xml.etree.ElementTree.Element("Image")
        with Image.open(path_file + "/" + name_file + "." + type_file) as img:
            bounding_box = img.size
    else:
        info_fail(card.name, "Unknown graphics type")
        return

    # Factor to scale the graphic by to fit in the container
    factor_x = size_box_x / bounding_box[0]
    factor_y = size_box_y / bounding_box[1]

    factor = None

    if mode_scale_image == "fit":
        factor = min(factor_x, factor_y)
    elif mode_scale_image == "fit_priority_x":
        if factor_x * bounding_box[1] >= size_box_y:
            factor = factor_x
        else:
            factor = factor_y

    # Final size of the scaled graphic
    size_insert_x = bounding_box[0] * factor
    size_insert_y = bounding_box[1] * factor

    # Distance to move graphic by to fit into center of container
    graphic_position_x = (size_box_x - size_insert_x) / 2 + coordinates[0][0]
    graphic_position_y = coordinates[0][1]
    if mode_align_vertical == "center":
        graphic_position_y += (size_box_y - size_insert_y) / 2

    # Factor (Rotation) (Rotation) Factor TranslateX TranslateY
    xml_element.set("ItemTransform",
                    str(factor) + " 0 0 " + str(factor) + " " + str(graphic_position_x) + " " + str(
                        graphic_position_y))

    xml_prop = xml.etree.ElementTree.Element("Properties")

    # Important to keep all 4 elements, otherwise sizing does not get applied
    xml_bounds = xml.etree.ElementTree.Element("GraphicBounds")
    xml_bounds.set("Left", str(0))
    xml_bounds.set("Top", str(0))
    xml_bounds.set("Right", str(bounding_box[0]))
    xml_bounds.set("Bottom", str(bounding_box[1]))

    xml_link = xml.etree.ElementTree.Element("Link")
    xml_link.set("LinkResourceURI", "file:" + path_file + "/" + name_file + "." + type_file)

    xml_prop.append(xml_bounds)
    xml_element.append(xml_prop)
    xml_element.append(xml_link)
    element.append(xml_element)

    tree.write("data/memory/Spreads/Spread_" + identifier_spread + ".xml")


def insert_pdf(card, identifier_spread, identifier_field, path_file, name_file, page_number=1):
    if not does_file_exist(path_file + "/" + name_file + ".pdf"):
        info_fail(card.name, "Specified pdf does not exist")
        return

    tree = xml.etree.ElementTree.parse("data/memory_print/Spreads/Spread_" + identifier_spread + ".xml")
    rectangle = tree.find(".//Rectangle[@Self='" + identifier_field + "']")
    pdf = xml.etree.ElementTree.Element("PDF")
    pdf.set("ItemTransform", "1 0 0 1 -77.95261341004854 -651.6848968746158")

    pdf_attribute = xml.etree.ElementTree.Element("PDFAttribute")
    pdf_attribute.set("PageNumber", str(page_number))

    link = xml.etree.ElementTree.Element("Link")
    link.set("LinkResourceURI", "file:" + path_file + "/" + name_file + ".pdf")

    rectangle.append(pdf)
    pdf.append(pdf_attribute)
    pdf.append(link)
    tree.write("data/memory_print/Spreads/Spread_" + identifier_spread + ".xml")


def insert_multi_font_text(oracle_text, object_id, align="variable", regex=None, font="", style="", size="8",
                           flavor_text=""):
    id_text_box = object_id

    tree = xml.etree.ElementTree.parse("data/memory/Stories/Story_" + id_text_box + ".xml")
    parent = tree.find(".//ParagraphStyleRange[1]")

    child = parent.find(".//CharacterStyleRange[1]")

    while child is not None:
        parent.remove(child)
        child = parent.find(".//CharacterStyleRange[1]")

    flavor_text_cleaned = flavor_text.replace("\n", " ")

    # Check alignment
    if (len(oracle_text) + len(flavor_text_cleaned) >= 100 and align == "variable") or align == "left":
        parent.set("Justification", "LeftAlign")

    if regex is None:
        regex = regex_template_oracle

    # Split into different cases to treat
    text_array = split_string_along_regex(oracle_text, *regex)

    # Deal with nested reminder text
    text_array = handle_nested_reminder_text(text_array)

    # Remove reminder text
    # text_array = list(filter(lambda x: (x[2] != "reminder"), text_array))

    # Remove initial newline
    if len(text_array) > 0 and text_array[0][0].startswith("\n"):
        text_array[0] = (text_array[0][0][1:], text_array[0][1], text_array[0][2])

    # Remove trailing newline
    if len(text_array) > 0 and text_array[-1][0].endswith("\n"):
        text_array[-1] = (
            text_array[-1][0][:-2 or None], text_array[-1][1], text_array[-1][2])

    # Insert flavor text
    if PRINT_FLAVOR_TEXT and len(flavor_text_cleaned) > 0:
        flavor_array = split_string_along_regex(flavor_text_cleaned, *regex_template_flavor,
                                                standard_identifier="flavor")
        if len(text_array) > 0:
            text_array.append(("\n", "type", "flavor"))
        for entry in flavor_array:
            if entry[2] == "flavor":
                text_array.append(entry)
            else:
                text_array.append((entry[0].replace("*", ""), entry[1], entry[2]))

    for part in text_array:
        if part[1] == "type":
            if part[2] == "normal":
                parent.append(insert_text_element(part[0], font=font, style=style, size=size))
            elif part[2] == "reminder":
                parent.append(
                    insert_text_element(part[0], font=FONT_STANDARD, style=FONT_STANDARD_STYLE_ITALIC, size=size))
            elif part[2] == "flavor":
                parent.append(
                    insert_text_element(part[0], font=FONT_STANDARD, style=FONT_STANDARD_STYLE_ITALIC, size=size))
        elif part[1] == "font":
            if part[2][0] == "KyMana":
                mana_array = []
                match = re.search(regex_mana, part[0])
                mana_array.append(mana_mapping[match.group("match")])

                mana = "".join(mana_array)
                parent.append(insert_text_element(mana, font=part[2][0], style=part[2][1], size=size))
            else:
                parent.append(insert_text_element(part[0], font=part[2][0], style=part[2][1], size=size))

    tree.write("data/memory/Stories/Story_" + id_text_box + ".xml")
