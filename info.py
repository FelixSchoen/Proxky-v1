from helper import *


def info_normal(cardname, message):
    print(f"[{helper_truncate(cardname)}]{bcolors.ENDC} \t\t{message}")


def info_success(cardname, message):
    print(f"{bcolors.OKGREEN}[{helper_truncate(cardname)}]{bcolors.ENDC} \t\t{message}")


def info_skip(cardname, message):
    print(f"{bcolors.OKBLUE}[{helper_truncate(cardname)}]{bcolors.ENDC} \t\t{message}")


def info_warn(cardname, message):
    print(f"{bcolors.WARNING}[{helper_truncate(cardname)}]{bcolors.ENDC} \t\t{message}")


def info_fail(cardname, message):
    print(f"{bcolors.FAIL}[{helper_truncate(cardname)}]{bcolors.ENDC} \t\t{message}")
