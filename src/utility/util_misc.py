import math
import os
import re

from src.utility.variables import regex_template_mana


def split_string_along_regex(string, *matchers: ([str], str, str), standard_category="type",
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


def handle_nested_reminder_text(text_array):
    array_to_return = []

    for element in text_array:
        if element[2] != "reminder":
            array_to_return.append(element)
        else:
            returned_array = split_string_along_regex(element[0], *regex_template_mana,
                                                      standard_identifier="reminder")
            array_to_return.extend(returned_array)

    return array_to_return


def does_file_exist(path):
    return os.path.exists(path)


def divide_into_chunks(length, n):
    # looping till length l
    for i in range(0, len(length), n):
        yield length[i:i + n]


def mm_to_pt(mm):
    return mm * 2.83464566929134
