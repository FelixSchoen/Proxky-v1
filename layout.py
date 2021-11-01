from insert_xml import *


def card_layout_double_faced(id_sets):
    for i, id_set in enumerate(id_sets):
        tree = xml.etree.ElementTree.parse("data/memory/Spreads/Spread_" + id_set[ids.SPREAD] + ".xml")
        modal = tree.find(".//Group[@Self='" + id_set[ids.GROUP_MODAL_O] + "']")
        modal.set("Visible", "true")

        shift_by = VALUE_MODAL_HEIGHT

        color_bars = [tree.find(".//Rectangle[@Self='" + id_set[ids.COLOR_BARS_O][0] + "']"),
                      tree.find(".//Rectangle[@Self='" + id_set[ids.COLOR_BARS_O][1] + "']")]

        for color_bar in color_bars:
            coordinates = color_bar.attrib["ItemTransform"].split(" ")
            color_bar.set("ItemTransform",
                          coordinates[0] + " " + coordinates[1] + " " + coordinates[2] + " " + coordinates[3] + " " +
                          coordinates[4] + " " + str(float(coordinates[5]) + shift_by))

        oracle_text = tree.find(".//TextFrame[@Self='" + id_set[ids.ORACLE_TEXT_O] + "']")

        helper_indesign_shift_y_coordinates(oracle_text, [shift_by, shift_by, 0, 0])

        side_indicator_o = tree.find(".//Group[@Self='" + id_set[ids.SIDE_INDICATOR_O] + "']")
        side_indicator_o.set("Visible", "true")

        if i == 0:
            insert_value_content(id_set[ids.SIDE_INDICATOR_T], "FRONT")
        elif i == 1:
            insert_value_content(id_set[ids.SIDE_INDICATOR_T], "BACK")

        tree.write("data/memory/Spreads/Spread_" + id_set[ids.SPREAD] + ".xml")


def card_layout_planeswalker(id_set):
    tree = xml.etree.ElementTree.parse("data/memory/Spreads/Spread_" + id_set[ids.SPREAD] + ".xml")

    # Show value
    value_text = tree.find(".//TextFrame[@Self='" + id_set[ids.VALUE_O] + "']")
    value_text.set("Visible", "true")

    # Show Planeswalker
    oracle_planeswalker = tree.find(".//Group[@Self='" + id_set[ids.GROUP_ORACLE_PLANESWALKER_O] + "']")
    oracle_planeswalker.set("Visible", "true")

    value_short_frame = tree.find(".//Rectangle[@Self='" + id_set[ids.VALUE_SHORT_FRAME_O] + "']")
    value_short_frame.set("Visible", "true")
    value_long_frame = tree.find(".//Rectangle[@Self='" + id_set[ids.VALUE_LONG_FRAME_O] + "']")
    value_long_frame.set("Visible", "false")

    # Change Mask
    mask = tree.find(".//Group[@Self='" + id_set[ids.MASK_O] + "']")
    bottom = tree.find(".//Group[@Self='" + id_set[ids.GROUP_BOTTOM_O] + "']")
    mask_short = tree.find(".//Polygon[@Self='" + id_set[ids.MASK_SHORT_O] + "']")
    mask_long = tree.find(".//Polygon[@Self='" + id_set[ids.MASK_LONG_O] + "']")

    for child in mask.findall("./Group[@Self='" + id_set[ids.GROUP_BOTTOM_O] + "']"):
        mask.remove(child)
    for child in mask_long.findall("./Group[@Self='" + id_set[ids.GROUP_BOTTOM_O] + "']"):
        mask_long.remove(child)

    mask_short.append(bottom)

    oracle_text = tree.find(".//TextFrame[@Self='" + id_set[ids.ORACLE_TEXT_O] + "']")
    oracle_text.set("Visible", "false")

    tree.write("data/memory/Spreads/Spread_" + id_set[ids.SPREAD] + ".xml")


def card_layout_no_value(id_set):
    if ids.VALUE_O not in id_set:
        return

    tree = xml.etree.ElementTree.parse("data/memory/Spreads/Spread_" + id_set[ids.SPREAD] + ".xml")

    # Hide value
    value_text = tree.find(".//TextFrame[@Self='" + id_set[ids.VALUE_O] + "']")
    value_text.set("Visible", "false")

    value_short_frame = tree.find(".//Rectangle[@Self='" + id_set[ids.VALUE_SHORT_FRAME_O] + "']")
    value_short_frame.set("Visible", "false")
    value_long_frame = tree.find(".//Rectangle[@Self='" + id_set[ids.VALUE_LONG_FRAME_O] + "']")
    value_long_frame.set("Visible", "false")

    # Remove Mask
    mask = tree.find(".//Group[@Self='" + id_set[ids.MASK_O] + "']")
    bottom = tree.find(".//Group[@Self='" + id_set[ids.GROUP_BOTTOM_O] + "']")
    mask_short = tree.find(".//Polygon[@Self='" + id_set[ids.MASK_SHORT_O] + "']")
    mask_long = tree.find(".//Polygon[@Self='" + id_set[ids.MASK_LONG_O] + "']")

    mask.append(bottom)

    for child in mask_short.findall(".//Group[@Self='" + id_set[ids.GROUP_BOTTOM_O] + "']"):
        mask_short.remove(child)
    for child in mask_long.findall(".//Group[@Self='" + id_set[ids.GROUP_BOTTOM_O] + "']"):
        mask_long.remove(child)

    # Expand Oracle Text Box
    oracle_text = tree.find(".//TextFrame[@Self='" + id_set[ids.ORACLE_TEXT_O] + "']")

    shift_by = 42.0944859662393 - 37.13385826771649

    bottom_left = oracle_text.find(".//PathPointType[2]")
    bottom_right = oracle_text.find(".//PathPointType[3]")

    for point in [bottom_left, bottom_right]:
        x_coordinate, y_coordinate = point.attrib["Anchor"].split(" ")
        point.attrib.pop("Anchor")
        point.attrib.pop("LeftDirection")
        point.attrib.pop("RightDirection")

        coordinates = x_coordinate + " " + str(float(y_coordinate) + shift_by)
        point.set("Anchor", coordinates)
        point.set("LeftDirection", coordinates)
        point.set("RightDirection", coordinates)

    tree.write("data/memory/Spreads/Spread_" + id_set[ids.SPREAD] + ".xml")


def card_layout_split(id_set):
    tree = xml.etree.ElementTree.parse("data/memory/Spreads/Spread_" + id_set[ids.SPREAD] + ".xml")

    group_normal = tree.find(".//Group[@Self='" + id_set[ids.GROUP_NORMAL_O] + "']")
    group_normal.set("Visible", "false")

    group_normal = tree.find(".//Group[@Self='" + id_set[ids.GROUP_SPLIT_O] + "']")
    group_normal.set("Visible", "true")

    tree.write("data/memory/Spreads/Spread_" + id_set[ids.SPREAD] + ".xml")


def card_layout_adventure(id_set):
    tree = xml.etree.ElementTree.parse("data/memory/Spreads/Spread_" + id_set[ids.SPREAD] + ".xml")

    oracle_text = tree.find(".//TextFrame[@Self='" + id_set[ids.ORACLE_TEXT_O] + "']")
    oracle_text.set("Visible", "false")

    layout_adventure = tree.find(".//Group[@Self='" + id_set[ids.GROUP_ORACLE_ADVENTURE_O] + "']")
    layout_adventure.set("Visible", "true")

    tree.write("data/memory/Spreads/Spread_" + id_set[ids.SPREAD] + ".xml")


def card_layout_token(id_set, card):
    tree = xml.etree.ElementTree.parse("data/memory/Spreads/Spread_" + id_set[ids.SPREAD] + ".xml")

    oracle_entries = helper_split_string_along_regex(card.oracle_text, *regex_oracle)
    if all(oracle_type == "reminder" for (_, _, oracle_type) in oracle_entries):
        card_layout_no_oracle_text(id_set, card)


def card_layout_no_oracle_text(id_set, card):
    tree = xml.etree.ElementTree.parse("data/memory/Spreads/Spread_" + id_set[ids.SPREAD] + ".xml")

    oracle_text = tree.find(".//TextFrame[@Self='" + id_set[ids.ORACLE_TEXT_O] + "']")
    oracle_text.set("Visible", "false")

    artwork = tree.find(".//Rectangle[@Self='" + id_set[ids.ARTWORK_O] + "']")
    header = tree.find(".//Group[@Self='" + id_set[ids.GROUP_HEADER_O] + "']")

    additional_shift = 0

    if card.power == "" and card.toughness == "":
        additional_shift = VALUE_SHIFT_TOKEN_NO_VALUE

    helper_indesign_shift_y_coordinates(artwork, [0, 0, VALUE_SHIFT_ARTWORK_TOKEN_WITH_VALUE + additional_shift,
                                                  VALUE_SHIFT_ARTWORK_TOKEN_WITH_VALUE + additional_shift])

    coordinates = header.attrib["ItemTransform"].split(" ")
    header.set("ItemTransform",
               coordinates[0] + " " + coordinates[1] + " " + coordinates[2] + " " + coordinates[3] + " " +
               coordinates[4] + " " + str(
                   float(coordinates[5]) + VALUE_SHIFT_HEADER_TOKEN_WITH_VALUE + additional_shift))

    tree.write("data/memory/Spreads/Spread_" + id_set[ids.SPREAD] + ".xml")


def card_delete_backside(id_set):
    os.remove("data/memory/Spreads/Spread_" + id_set[ids.SPREAD] + ".xml")

    tree = xml.etree.ElementTree.parse("data/memory/designmap.xml")
    element = tree.getroot().find(".//*[@src='Spreads/Spread_" + id_set[ids.SPREAD] + ".xml']")
    tree.getroot().remove(element)

    with open("data/memory/designmap.xml", "wb") as file:
        file.write(b'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>')
        file.write(b'<?aid style="50" type="document" readerVersion="6.0" featureSet="257" product="16.4(55)" ?>')
        tree.write(file, xml_declaration=False, encoding="utf-8")
