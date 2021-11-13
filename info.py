from variables import bcolors


def info_normal(cardname, message):
    print(f"[{truncate(cardname)}]{bcolors.ENDC} \t\t{message}")


def info_success(cardname, message):
    print(f"{bcolors.OKGREEN}[{truncate(cardname)}]{bcolors.ENDC} \t\t{message}")


def info_skip(cardname, message):
    print(f"{bcolors.OKBLUE}[{truncate(cardname)}]{bcolors.ENDC} \t\t{message}")


def info_warn(cardname, message):
    print(f"{bcolors.WARNING}[{truncate(cardname)}]{bcolors.ENDC} \t\t{message}")


def info_fail(cardname, message):
    print(f"{bcolors.FAIL}[{truncate(cardname)}]{bcolors.ENDC} \t\t{message}")


def truncate(string, size=20):
    return string[:size - 2] + ".." if len(string) > size else string
