import os
import xml

from src.utility.util_xml import utility_indesign_shift_coordinates, utility_split_string_along_regex, \
    utility_make_object_transparent, mm_to_pt, utility_change_text_color, utility_change_text_style
from src.utility.variables import ids, VALUE_MODAL_HEIGHT, regex_template_oracle, VALUE_SHIFT_WITHOUT_ORACLE_WITHOUT_VALUE, \
    VALUE_SHIFT_WITHOUT_ORACLE_WITH_VALUE, VALUE_SHIFT_ARTWORK_FULL_BODY


def card_layout_double_faced(id_sets):
    for i, id_set in enumerate(id_sets):
        tree = xml.etree.ElementTree.parse("data/memory/Spreads/Spread_" + id_set[ids.SPREAD] + ".xml")
        modal = tree.find(".//TextFrame[@Self='" + id_set[ids.MODAL_O] + "']")
        modal.set("Visible", "true")

        shift_by = VALUE_MODAL_HEIGHT

        # Shift oracle text
        oracle_text = tree.find(".//TextFrame[@Self='" + id_set[ids.ORACLE_O] + "']")
        utility_indesign_shift_coordinates(oracle_text, y_coordinates=[shift_by, shift_by, 0, 0])

        # Shift planeswalker texts
        planeswalker_boxes = [id_set[ids.PLANESWALKER_VALUE_O][0],
                              id_set[ids.PLANESWALKER_ORACLE_NUMBERED_O][0],
                              id_set[ids.PLANESWALKER_VALUE_O][1],
                              id_set[ids.PLANESWALKER_ORACLE_NUMBERED_O][1],
                              id_set[ids.PLANESWALKER_VALUE_O][2],
                              id_set[ids.PLANESWALKER_ORACLE_NUMBERED_O][2],
                              id_set[ids.PLANESWALKER_VALUE_O][3],
                              id_set[ids.PLANESWALKER_ORACLE_NUMBERED_O][3],
                              id_set[ids.PLANESWALKER_ORACLE_FINAL_O]]
        for box_id in planeswalker_boxes:
            box = tree.find(".//TextFrame[@Self='" + box_id + "']")
            utility_indesign_shift_coordinates(box, y_coordinates=[shift_by, shift_by, shift_by, shift_by])

        tree.write("data/memory/Spreads/Spread_" + id_set[ids.SPREAD] + ".xml")


def card_layout_planeswalker(id_set):
    tree = xml.etree.ElementTree.parse("data/memory/Spreads/Spread_" + id_set[ids.SPREAD] + ".xml")

    # Show value
    value_text = tree.find(".//TextFrame[@Self='" + id_set[ids.VALUE_O] + "']")
    value_text.set("Visible", "true")

    # Show Planeswalker
    oracle_planeswalker = tree.find(".//Group[@Self='" + id_set[ids.GROUP_PLANESWALKER_O] + "']")
    oracle_planeswalker.set("Visible", "true")

    oracle_text = tree.find(".//TextFrame[@Self='" + id_set[ids.ORACLE_O] + "']")
    oracle_text.set("Visible", "false")

    tree.write("data/memory/Spreads/Spread_" + id_set[ids.SPREAD] + ".xml")


def card_layout_no_value(id_set):
    # Important for adventure type cards
    if ids.VALUE_O not in id_set:
        return

    tree = xml.etree.ElementTree.parse("data/memory/Spreads/Spread_" + id_set[ids.SPREAD] + ".xml")

    # Hide value
    value_text = tree.find(".//TextFrame[@Self='" + id_set[ids.VALUE_O] + "']")
    value_text.set("Visible", "false")

    # Remove mask
    if ids.MASK_COLOR_INDICATOR_BOT_O in id_set:
        footer = tree.find(".//Group[@Self='" + id_set[ids.GROUP_FOOTER_O] + "']")
        mask = tree.find(".//Polygon[@Self='" + id_set[ids.MASK_COLOR_INDICATOR_BOT_O] + "']")
        color_indicator_bot = tree.find(".//Rectangle[@Self='" + id_set[ids.COLOR_INDICATOR_BOT_O] + "']")

        # Appending it to footer group incurs this movement, idk why
        SHIFT_BY = -1.417322834646
        utility_indesign_shift_coordinates(color_indicator_bot, y_coordinates=[SHIFT_BY, SHIFT_BY, SHIFT_BY, SHIFT_BY])

        mask.remove(color_indicator_bot)
        footer.append(color_indicator_bot)

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

    oracle_text = tree.find(".//TextFrame[@Self='" + id_set[ids.ORACLE_O] + "']")
    oracle_text.set("Visible", "false")

    layout_adventure = tree.find(".//Group[@Self='" + id_set[ids.GROUP_ADVENTURE_O] + "']")
    layout_adventure.set("Visible", "true")

    tree.write("data/memory/Spreads/Spread_" + id_set[ids.SPREAD] + ".xml")


def card_layout_token(id_set, card):
    oracle_entries = utility_split_string_along_regex(card.oracle_text, *regex_template_oracle)
    if all(oracle_type == "reminder" for (_, _, oracle_type) in oracle_entries):
        card_layout_no_oracle_text(id_set, card)


def card_layout_no_oracle_text(id_set, card):
    tree = xml.etree.ElementTree.parse("data/memory/Spreads/Spread_" + id_set[ids.SPREAD] + ".xml")

    oracle_text = tree.find(".//TextFrame[@Self='" + id_set[ids.ORACLE_O] + "']")
    oracle_text.set("Visible", "false")

    artwork = tree.find(".//Rectangle[@Self='" + id_set[ids.ARTWORK_O] + "']")
    header = tree.find(".//Group[@Self='" + id_set[ids.GROUP_HEADER_O] + "']")
    color_indicator = tree.find(".//Rectangle[@Self='" + id_set[ids.COLOR_INDICATOR_TOP_O] + "']")
    backdrop = tree.find(".//Rectangle[@Self='" + id_set[ids.BACKDROP_O] + "']")

    additional_shift = 0
    color_indicator.set("Visible", "false")

    if card.power == "" and card.toughness == "":
        additional_shift = VALUE_SHIFT_WITHOUT_ORACLE_WITHOUT_VALUE

    utility_indesign_shift_coordinates(artwork,
                                       y_coordinates=[0, 0, VALUE_SHIFT_WITHOUT_ORACLE_WITH_VALUE + additional_shift,
                                                      VALUE_SHIFT_WITHOUT_ORACLE_WITH_VALUE + additional_shift])
    utility_indesign_shift_coordinates(backdrop,
                                       y_coordinates=[VALUE_SHIFT_WITHOUT_ORACLE_WITH_VALUE + additional_shift,
                                                      VALUE_SHIFT_WITHOUT_ORACLE_WITH_VALUE + additional_shift, 0, 0])

    coordinates = header.attrib["ItemTransform"].split(" ")
    header.set("ItemTransform",
               coordinates[0] + " " + coordinates[1] + " " + coordinates[2] + " " + coordinates[3] + " " +
               coordinates[4] + " " + str(
                   float(coordinates[5]) + VALUE_SHIFT_WITHOUT_ORACLE_WITH_VALUE + additional_shift))

    tree.write("data/memory/Spreads/Spread_" + id_set[ids.SPREAD] + ".xml")


def card_layout_transparent_body_art(id_set):
    tree = xml.etree.ElementTree.parse("data/memory/Spreads/Spread_" + id_set[ids.SPREAD] + ".xml")

    artwork = tree.find(".//Rectangle[@Self='" + id_set[ids.ARTWORK_O] + "']")
    utility_indesign_shift_coordinates(artwork, y_coordinates=[0, 0, VALUE_SHIFT_ARTWORK_FULL_BODY,
                                                               VALUE_SHIFT_ARTWORK_FULL_BODY])

    rectangles_50 = []
    rectangles_85 = [id_set[ids.BACKDROP_O]]
    groups_75 = []

    for object_id in rectangles_50:
        element = tree.find(".//Rectangle[@Self='" + object_id + "']")
        utility_make_object_transparent(element, 50)

    for object_id in rectangles_85:
        element = tree.find(".//Rectangle[@Self='" + object_id + "']")
        utility_make_object_transparent(element, 85)

    for object_id in groups_75:
        element = tree.find(".//Group[@Self='" + object_id + "']")
        utility_make_object_transparent(element, 75, mode="")

    tree.write("data/memory/Spreads/Spread_" + id_set[ids.SPREAD] + ".xml")


def card_layout_full_body_art(id_set):
    tree = xml.etree.ElementTree.parse("data/memory/Spreads/Spread_" + id_set[ids.SPREAD] + ".xml")

    artwork = tree.find(".//Rectangle[@Self='" + id_set[ids.ARTWORK_O] + "']")
    utility_indesign_shift_coordinates(artwork, y_coordinates=[0, 0, VALUE_SHIFT_ARTWORK_FULL_BODY,
                                                               VALUE_SHIFT_ARTWORK_FULL_BODY])

    backdrop = tree.find(".//Rectangle[@Self='" + id_set[ids.BACKDROP_O] + "']")
    utility_make_object_transparent(backdrop, 85)
    utility_indesign_shift_coordinates(backdrop,
                                       x_coordinates=[mm_to_pt(4.5), mm_to_pt(-4.5), mm_to_pt(4.5), mm_to_pt(-4.5)],
                                       y_coordinates=[0, 0, mm_to_pt(-6.25), mm_to_pt(-6.25)])
    backdrop.set("TopLeftCornerOption", "RoundedCorner")
    backdrop.set("TopRightCornerOption", "RoundedCorner")
    backdrop.set("BottomLeftCornerOption", "RoundedCorner")
    backdrop.set("BottomRightCornerOption", "RoundedCorner")
    backdrop.set("TopLeftCornerRadius", str(mm_to_pt(1)))
    backdrop.set("TopRightCornerRadius", str(mm_to_pt(1)))
    backdrop.set("BottomLeftCornerRadius", str(mm_to_pt(1)))
    backdrop.set("BottomRightCornerRadius", str(mm_to_pt(1)))

    artist = xml.etree.ElementTree.parse("data/memory/Stories/Story_" + id_set[ids.ARTIST_INFORMATION_T] + ".xml")
    utility_change_text_color(artist, "Color/Paper")
    utility_change_text_style(artist, "Display Bold")
    artist.write("data/memory/Stories/Story_" + id_set[ids.ARTIST_INFORMATION_T] + ".xml")

    collector_information = xml.etree.ElementTree.parse(
        "data/memory/Stories/Story_" + id_set[ids.COLLECTOR_INFORMATION_T] + ".xml")
    utility_change_text_color(collector_information, "Color/Paper")
    utility_change_text_style(collector_information, "Display Bold")
    collector_information.write("data/memory/Stories/Story_" + id_set[ids.COLLECTOR_INFORMATION_T] + ".xml")

    value = xml.etree.ElementTree.parse(
        "data/memory/Stories/Story_" + id_set[ids.VALUE_T] + ".xml")
    utility_change_text_color(value, "Color/Paper")
    value.write("data/memory/Stories/Story_" + id_set[ids.VALUE_T] + ".xml")

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
