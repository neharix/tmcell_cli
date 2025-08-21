import os


def clear_string(string: str):
    return string.replace("\r", "").replace("\n", "").replace("\xa0", " ").strip()


def clear_screen():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")
