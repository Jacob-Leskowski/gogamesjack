from __future__ import annotations
from typing import Any
import os


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

def createPage(site: siteInformation, mainNav: str, subNav: str) -> str:
    head: str = f'<!DOCTYPE html><html><head><title>Go Games Jack {site.name}</title><meta name="viewport" content="width=device-width,initial-scale=1"><link href="./style.css" rel="stylesheet"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" /></head><body><h1 class="site-name">Go Games Jack</h1><main class="page-body"><nav class="sidebar"><nav class="top-nav">'
    midSection: str = f'</nav><aside class="user-nav"> <a href="./login.html" class="material-symbols-outlined">account_circle </aside></a> <a href="./login.html">Login</aside> </a></nav><main class="page"><header class="page-header"> <img src="./assets/welcome.png" alt="Welcome" class="miniIcon"><h1 class="page-title">Welcome</h1></header><main class="page-content"><section class="content">'
    footer: str = f'</section><footer class="rightBarFooter"><p><a href="../../Jacob Leskowski/index.html" target="_blank" rel="noopener noreferrer">JackLeskowski</aside> </a></p></footer></main></main></main></body></html>'
    return head + mainNav + subNav + midSection + site.content + footer

def createBrantch(site: siteInformation, allSites: list[siteInformation], mainNav: str) -> str:
    return ""


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


def deleteAll() -> None:
    currentDir = os.getcwd()
    for item in os.listdir(currentDir):
        itemPath = os.path.join(currentDir, item)
        if os.path.isfile(itemPath):
            if item not in ["style.css", "php-gogamesjack.py"]:
                os.remove(itemPath)
        elif os.path.isdir(itemPath):
            if item not in ["assets", "scripts"]:
                os.rmdir(itemPath)

def writeSite(information) -> None:
    with open("index.html", "w", encoding="utf-8") as file:
        file.write(information)