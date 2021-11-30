import re
import xml

from PIL import Image

from utility import utility_split_string_along_regex, utility_file_exists, utility_indesign_get_coordinates, \
    utility_vector_bounding_box
from info import info_fail
from variables import image_types, regex_oracle, mana_mapping


def insert_value_content(identifier, value):
    tree = xml.etree.ElementTree.parse("data/memory/Stories/Story_" + identifier + ".xml")
    entry = tree.find(".//Content[1]")
    entry.text = value

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

    content_split = utility_split_string_along_regex(content, ("\n", "type", "break"))

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
    if not utility_file_exists(path_file + "/" + name_file + "." + type_file):
        info_fail(card.name, "Specified graphic does not exist")
        return

    tree = xml.etree.ElementTree.parse("data/memory/Spreads/Spread_" + identifier_spread + ".xml")
    element = tree.find(".//Rectangle[@Self='" + identifier_field + "']")
    coordinates = utility_indesign_get_coordinates(element)

    # Size of the container
    size_box_x = abs(coordinates[1][0] - coordinates[0][0])
    size_box_y = abs(coordinates[2][1] - coordinates[1][1])

    # Bounding box defined in the file
    if type_file == "svg":
        xml_element = xml.etree.ElementTree.Element("SVG")
        bounding_box = utility_vector_bounding_box(path_file, name_file)
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
    if not utility_file_exists(path_file + "/" + name_file + ".pdf"):
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


def insert_multi_font_text(oracle_text, object_id, align="variable", regex=None, font="", style="", size="8"):
    id_text_box = object_id

    tree = xml.etree.ElementTree.parse("data/memory/Stories/Story_" + id_text_box + ".xml")
    parent = tree.find(".//ParagraphStyleRange[1]")
    child = tree.find(".//CharacterStyleRange[1]")
    parent.remove(child)

    # Check alignment
    if (len(oracle_text) > 100 and align == "variable") or align == "left":
        parent.set("Justification", "LeftAlign")

    if regex is None:
        regex = regex_oracle

    # Split into different cases to treat
    text_array = utility_split_string_along_regex(oracle_text, *regex)

    # Remove reminder text
    text_array = list(filter(lambda x: (x[2] != "reminder"), text_array))

    # Remove initial newline
    if len(text_array) > 0 and text_array[0][0].startswith("\n"):
        text_array[0] = (text_array[0][0][1:], text_array[0][1], text_array[0][2])

    # Remove trailing newline
    if len(text_array) > 0 and text_array[-1][0].endswith("\n"):
        text_array[-1] = (
            text_array[-1][0][:-2 or None], text_array[-1][1], text_array[-1][2])

    for part in text_array:
        if part[1] == "type":
            if part[2] == "normal":
                parent.append(insert_text_element(part[0], font=font, style=style, size=size))
        elif part[1] == "font":
            if part[2][0] == "KyMana":
                mana = []
                for item in re.findall("({[A-Z0-9]+})", part[0]):
                    mana.append(mana_mapping[item])
                mana = "".join(mana)
                parent.append(insert_text_element(mana, font=part[2][0], style=part[2][1], size=size))
            else:
                parent.append(insert_text_element(part[0], font=part[2][0], style=part[2][1], size=size))

    tree.write("data/memory/Stories/Story_" + id_text_box + ".xml")