from __future__ import annotations
# from typing import Any
# import os


class siteInformation:
    def __init__(
        self,
        name: str,
        content: str = "",
        imgPath: str | None = None,
        children: list[siteInformation] | None = None,
    ) -> None:
        self.name: str = name
        self.content: str = content
        self.imgPath: str | None = imgPath
        self.children: list[siteInformation] | None = children

        # adjust name
        self.name = self.name.strip().title()

        # adjust file name
        self.file: str = self.name.strip().lower().replace(" ", "_")
        if self.file == "welcome":
            self.file = "index"

        # adjust image path
        if self.imgPath is None:
            self.imgPath = self.name
        self.imgPath = self.imgPath.strip().lower().replace(" ", "_")
        if "." not in self.imgPath:
            self.imgPath += ".png"

        # create a blank page
        self.page: str | None = None

    def copy(self: siteInformation) -> siteInformation:
        return siteInformation(self.name, self.content, self.imgPath, self.children)


"""

# DELETE LATER

def organize(
    infoSites: list[siteInformation],
) -> tuple[dict[str, siteInformation], dict[str, list[str]]]:
    pointers: dict[str, siteInformation] = {}
    for info in infoSites:
        pointers[info.name] = infoSites.copy()
    allSites: dict[str, list[str]] = {"mainSites": []}
    waitingQ: list[tuple[str, str]] = []
    for info in infoSites:
        if not info.parent is None:
            waitingQ.append((info.name, info.parent))
            continue
        allSites["mainSites"].append(info.name)
        allSites[info.name] = []
    for names, parents in waitingQ:
        allSites[parents].append(names)
    print(pointers)
    print(allSites)
    return pointers, allSites
"""


def mainNav(allSites: list[siteInformation]) -> str:
    iconButtons: list[str] = []
    for site in allSites:
        iconButtons.append(
            f'<a href="./{site.file}.html" class="largeIconLink"><img src="./assets/{site.imgPath}" alt="{site.name}" class="largeIcon" id="largeIconHome"><div class="largeIconBar"></div></a>'
        )
    return r'<nav class="main-nav">' + "".join(iconButtons) + r"</nav>"


def basePage(info: siteInformation) -> str:
    pass


SITES: list[siteInformation] = [
    siteInformation(
        "welcome",
        "<h2>Welcome</h2><h3>What is Go Games Jack?</h3><p>Go Games Jack is a website that allows you to play games with your friends and family. You can play games online or locally. You can also play single player games.</p>",
        "home",
        [
            siteInformation(
                "leaderboard",
                "<h2>Leaderboard</h2><h3>Snake</h3><table><tr><th>Rank</th><th>Player</th><th>Score</th></tr><tr><td>1</td><td>Player 1</td><td>100</td></tr></table><p>Stuff goes here.</p>",
            ),
            siteInformation(
                "help",
                "<h2>Help</h2><h3>Navigation</h3><p>Use the navigation bar on the far left to navigate between pages.</p><h3>Solo</h3><p>Solo games are played by one player against the computer. Simply go to the game's tab to play.</p><h3>Local</h3><p>Local games are played by two players on the same device. Simply go to the game's tab to play.</p>",
            ),
        ],
    )
]

print(mainNav(SITES))

"""

USE WHEN WORKING WITH OS


def deleteAll() -> None:
    # except assets/ & style.css & scripts/
    pass

def writeSite(information) -> None:
    with open("index.html", "w", encoding="utf-8") as file:
        file.write(information)
"""
