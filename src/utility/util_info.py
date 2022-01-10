from src.utility.variables import bcolors


def info_normal(name, message):
    print(f"[{truncate(name)}]{bcolors.ENDC} \t\t{message}")


def info_success(name, message):
    print(f"{bcolors.OKGREEN}[{truncate(name)}]{bcolors.ENDC} \t\t{message}")


def info_skip(name, message):
    print(f"{bcolors.OKBLUE}[{truncate(name)}]{bcolors.ENDC} \t\t{message}")


def info_warn(name, message):
    print(f"{bcolors.WARNING}[{truncate(name)}]{bcolors.ENDC} \t\t{message}")


def info_fail(name, message):
    print(f"{bcolors.FAIL}[{truncate(name)}]{bcolors.ENDC} \t\t{message}")


def truncate(string, size=20):
    return string[:size - 2] + ".." if len(string) > size else string
