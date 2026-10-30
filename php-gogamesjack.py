from __future__ import annotations
from typing import Any
import os
import shutil


class siteInformation:
    def __init__(
        self,
        name: str,
        content: str = "",
        children: list[siteInformation] | None = None,
        imgPath: str | None = None,
    ) -> None:
        self.name: str = name
        self.content: str = content
        self.children: list[siteInformation] | None = children
        self.imgPath: str | None = imgPath

        # adjust name
        self.name = self.name.strip().title()

        # adjust file name
        self.file: str = self.name.strip().lower().replace(" ", "_")
        if self.file == "home":
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
        return siteInformation(self.name, self.content, self.children, self.imgPath)


def allNav(
    allSites: list[siteInformation], selected: int, subSelected: int | None = None
) -> str:
    currentSite: siteInformation = allSites[selected]
    if subSelected is None:
        subSelected = 0
    currentIsLandingPage: bool = subSelected == 0
    currentPrefix: str = "./" if currentIsLandingPage else "../"

    def pagePath(site: siteInformation, childIndex: int | None = None) -> str:
        if childIndex is None or not site.children:
            return f"{currentPrefix}{site.file}.html"
        child: siteInformation = site.children[childIndex]
        if childIndex == 0:
            return f"{currentPrefix}{site.file}.html"
        return (
            f"{currentPrefix}{site.file}/{child.file}.html"
            if currentIsLandingPage
            else f"./{child.file}.html"
        )

    # Main Nav
    iconButtons: list[str] = []
    for site in allSites:
        iconButtons.append(
            f'<a href="{pagePath(site)}" class="largeIconLink"><img src="{currentPrefix}assets/{site.imgPath}" alt="{site.name}" class="largeIcon" id="largeIcon{site.name.replace(" ", "")}"><div class="largeIconBar"></div></a>'
        )

    # Selected Main Nav Item
    iconButtons[selected] = (
        iconButtons[selected]
        .replace(
            '<div class="largeIconBar">',
            '<div class="largeIconBar" id="largeIconBarSelected">',
        )
        .replace('class="largeIcon"', 'class="largeIcon largeIconSelected"')
    )
    mainNav: str = r'<nav class="main-nav">' + "".join(iconButtons) + r"</nav>"

    # Sub Nav
    iconButtons: list[str] = []
    for childIndex, sit in enumerate(currentSite.children):
        href: str = pagePath(currentSite, childIndex)
        iconButtons.append(
            f'<tr class="mini-selector">'
            + f'<td><a href="{href}" id="{sit.file}"><img src="{currentPrefix}assets/{sit.imgPath}" alt="{sit.name}" class="smallIcon"></a></td>'
            + f'<td class="mini-selector-label"><a href="{href}" id="{sit.file}">{sit.name}</a></td>'
            + f"</tr>"
        )

    # Selected Sub Nav Item
    iconButtons[subSelected] = iconButtons[subSelected].replace(
        '<tr class="mini-selector">',
        '<tr class="mini-selector" id="mini-selector-selected">',
    )

    subNav: str = (
        f'<nav class="secondary-nav"><h1 class="section-title">{currentSite.name}</h1><table>'
        + "".join(iconButtons)
        + r"</table></nav>"
    )
    return mainNav + subNav


def createPage(
    allSites: list[siteInformation], selected: int = 0, subSelected: int | None = None
) -> str:
    site: siteInformation = allSites[selected]
    if subSelected is None:
        subSelected = 0
    page: siteInformation = site.children[subSelected] if site.children else site
    prefix: str = "./" if subSelected == 0 else "../"
    head: str = f'<!DOCTYPE html><html><head><title>Go Games Jack</title><meta name="viewport" content="width=device-width,initial-scale=1"><link href="{prefix}style.css" rel="stylesheet"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" /></head><body><h1 class="site-name">Go Games Jack</h1><main class="page-body"><nav class="sidebar"><nav class="top-nav">'
    midSection: str = f'</nav><aside class="user-nav"><a href="{prefix}login.html" class="material-symbols-outlined">account_circle</a><a href="{prefix}login.html">Login</a></aside></nav><main class="page"><header class="page-header"><img src="{prefix}assets/{page.imgPath}" alt="{page.name}" class="miniIcon"><h1 class="page-title">{page.name}</h1></header><main class="page-content"><section class="content">'
    footer: str = f'</section><footer class="rightBarFooter"><p><a href="../../Jacob Leskowski/index.html" target="_blank" rel="noopener noreferrer">JackLeskowski</a></p></footer></main></main></main></body></html>'
    return (
        head
        + allNav(allSites, selected, subSelected)
        + midSection
        + page.content
        + footer
    )


def createSites(
    allSites: list[siteInformation] = [], directory: str = os.getcwd()
) -> None:
    for site in allSites:
        os.makedirs(f"{directory}/{site.file}", exist_ok=True)
        for index, subSit in enumerate(site.children):
            page: str = createPage(allSites, allSites.index(site), index)
            outputPath: str = (
                f"{directory}/{site.file}.html"
                if index == 0
                else f"{directory}/{site.file}/{subSit.file}.html"
            )
            with open(outputPath, "w") as f:
                f.write(page)


def deleteAll(
    directory: str = os.getcwd(),
    saveFolders: list[str] = [],
    saveFiles: list[str] = [],
) -> None:
    # hard-codes folders & files that NEED to be saved
    saveFolders.append("assets")
    saveFolders.append("scripts")
    saveFiles.append("style.css")
    saveFiles.append("php-gogamesjack.py")
    saveFiles.append("README.md")
    currentDir = directory
    for item in os.listdir(currentDir):
        itemPath = os.path.join(currentDir, item)
        if os.path.isfile(itemPath):
            if item not in saveFiles:
                os.remove(itemPath)
        elif os.path.isdir(itemPath):
            if item not in saveFolders:
                shutil.rmtree(itemPath)


SITES: list[siteInformation] = [
    siteInformation(
        "home",
        "<h2>Welcome</h2><h3>What is Go Games Jack?</h3><p>Go Games Jack is a website that allows you to play games with your friends and family. You can play games online or locally. You can also play single player games.</p>",
        [
            siteInformation(
                "welcome",
                "<h2>Welcome</h2><h3>What is Go Games Jack?</h3><p>Go Games Jack is a website that allows you to play games with your friends and family. You can play games online or locally. You can also play single player games.</p>",
            ),
            siteInformation(
                "leaderboard",
                "<h2>Leaderboard</h2><h3>Snake</h3><table><tr><th>Rank</th><th>Player</th><th>Score</th></tr><tr><td>1</td><td>Player 1</td><td>100</td></tr></table><p>Stuff goes here.</p>",
            ),
            siteInformation(
                "help",
                "<h2>Help</h2><h3>Navigation</h3><p>Use the navigation bar on the far left to navigate between pages.</p><h3>Solo</h3><p>Solo games are played by one player against the computer. Simply go to the game's tab to play.</p><h3>Local</h3><p>Local games are played by two players on the same device. Simply go to the game's tab to play.</p>",
            ),
        ],
    ),
    siteInformation(
        "solo",
        "<h2>Scores</h2><h3>Snake</h3><table><tr><th>Rank</th><th>Player</th><th>Score</th></tr><tr><td>1</td><td>Player 1</td><td>100</td></tr><tr><td>2</td><td>Player 2</td><td>80</td></tr><tr><td>3</td><td>Player 3</td><td>60</td></tr></table>",
        [
            siteInformation(
                "scores",
                "<h2>Scores</h2><h3>Snake</h3><table><tr><th>Rank</th><th>Player</th><th>Score</th></tr><tr><td>1</td><td>Player 1</td><td>100</td></tr><tr><td>2</td><td>Player 2</td><td>80</td></tr><tr><td>3</td><td>Player 3</td><td>60</td></tr></table>",
                imgPath="scoreboard",
            ),
            siteInformation("snake", "<h2>Snake</h2>", imgPath="snake"),
        ],
        "single",
    ),
    siteInformation(
        "local",
        "<h2>Controls</h2>",
        [
            siteInformation("controls", "<h2>Controls</h2>", imgPath="controls"),
            siteInformation("pong", "<h2>Pong</h2>", imgPath="pong"),
        ],
        "local",
    ),
]


def main() -> None:
    deleteAll()
    # createSites(SITES)


if __name__ == "__main__":
    main()
