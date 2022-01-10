from src.utility.variables import bcolors


def info_normal(name, message):
    print(f"{name_in_brackets(name)}{bcolors.ENDC} \t\t{message}")


def info_success(name, message):
    print(f"{bcolors.OKGREEN}{name_in_brackets(name)}{bcolors.ENDC}{message}")


def info_skip(name, message):
    print(f"{bcolors.OKBLUE}{name_in_brackets(name)}{bcolors.ENDC}{message}")


def info_warn(name, message):
    print(f"{bcolors.WARNING}{name_in_brackets(name)}{bcolors.ENDC}{message}")


def info_fail(name, message):
    print(f"{bcolors.FAIL}{name_in_brackets(name)}{bcolors.ENDC}{message}")


def name_in_brackets(name, length=50):
    string = "["
    string += truncate(name)
    string += "]"

    for i in range(0, length - len(string)):
        string += " "

    return string


def truncate(string, length=40):
    return string[:length - 3] + "..." if len(string) > length else string
