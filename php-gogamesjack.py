import os

def deleteAll() -> None:
    pass

def writeSite(information) -> None:

    with open("index.html", "w", encoding="utf-8") as file:
        file.write(information)