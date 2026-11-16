from __future__ import annotations
from bs4 import BeautifulSoup
import shutil
import json
import os


class SiteInformation:
    def __init__(
        self,
        name: str,
        content: str = "",
        children: list[SiteInformation] | None = None,
        imgPath: str | None = None,
        links: list[str] = [],
    ) -> None:
        self.name: str = name
        self.content: str = content
        self.children: list[SiteInformation] | None = children
        self.imgPath: str | None = imgPath
        self.links: list[str] = []

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

    def copy(self: SiteInformation) -> SiteInformation:
        return SiteInformation(self.name, self.content, self.children, self.imgPath)


def allNav(
    allSites: list[SiteInformation], selected: int, subSelected: int | None = None
) -> str:
    currentSite: SiteInformation = allSites[selected]
    if subSelected is None:
        subSelected = 0
    currentIsLandingPage: bool = subSelected == 0
    currentPrefix: str = "./" if currentIsLandingPage else "../"

    def pagePath(site: SiteInformation, childIndex: int | None = None) -> str:
        if childIndex is None or not site.children:
            return f"{currentPrefix}{site.file}.html"
        child: SiteInformation = site.children[childIndex]
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
            f'<a href="{pagePath(site)}" class="largeIconLink"><img src="{currentPrefix}assets/icons/{site.imgPath}" alt="{site.name}" class="largeIcon" id="largeIcon{site.name.replace(" ", "")}"><div class="largeIconBar"></div></a>'
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
    """
    <nav class="secondary-nav">
        <h1 class="section-title">Local</h1>
        <table>
            <tr class="mini-selector" id="mini-selector-selected">
                <td><a href="./local.html" id="controls"><img src="./assets/icons/controls.png" alt="Controls"
                            class="smallIcon"></a></td>
                <td class="mini-selector-label"><a href="./local.html" id="controls">Controls</a></td>
            </tr>
            <tr class="mini-selector">
                <td><a href="./local/pong.html" id="pong"><img src="./assets/icons/pong.png" alt="Pong"
                            class="smallIcon"></a></td>
                <td class="mini-selector-label"><a href="./local/pong.html" id="pong">Pong</a></td>
            </tr>
        </table>
    </nav>
    """

    # Sub Nav
    iconButtons: list[str] = []
    for childIndex, sit in enumerate(currentSite.children):
        href: str = pagePath(currentSite, childIndex)
        iconButtons.append(
            f'<li class="mini-selector">'
            + f"<a href='{href}' id='{sit.file}'>"
            + f'<img src="{currentPrefix}assets/icons/{sit.imgPath}" alt="{sit.name}" class="smallIcon">'
            + f'<p class="mini-selector-label">{sit.name}</p>'
            + f"</a></li>"
        )

    # Selected Sub Nav Item
    iconButtons[subSelected] = iconButtons[subSelected].replace(
        '<li class="mini-selector">',
        '<li class="mini-selector" id="mini-selector-selected">',
    )

    subNav: str = (
        f'<nav class="secondary-nav"><h1 class="section-title">{currentSite.name}</h1><ul class="second-list">'
        + "".join(iconButtons)
        + r"</ul></nav>"
    )
    return mainNav + subNav


def createPage(
    allSites: SiteInformation | list[SiteInformation],
    selected: int = 0,
    subSelected: int | None = None,
    allLinks: list[str] = [
        "style.css",
        "https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200",
    ],
) -> str:
    if type(allSites) is list:
        site: SiteInformation = allSites[selected]
        if subSelected is None:
            subSelected = 0
        page: SiteInformation = site.children[subSelected] if site.children else site
        prefix: str = "./" if subSelected == 0 else "../"
    else:
        page: SiteInformation = allSites
        prefix: str = "./"

    findLinks: list[str] = page.links + allLinks
    headLinks: list[str] = []
    for lnk in findLinks:
        headLinks.append('<link href="')
        if not lnk.startswith("https"):
            headLinks[-1] += prefix
        headLinks[-1] += lnk
        headLinks[-1] += '"'
        if lnk.endswith(".js"):
            headLinks[-1] += ' rel="script"'
        else:
            headLinks[-1] += ' rel="stylesheet"'
        headLinks[-1] += ">"

    # <link href="{prefix}style.css" rel="stylesheet"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" />
    head: str = f'<!DOCTYPE html><html><head><title>Go Games Jack</title><meta name="viewport" content="width=device-width,initial-scale=1">{"".join(headLinks)}</head><body><h1 class="site-name">Go Games Jack</h1><main class="page-body">'
    startNav: str = f'<nav class="sidebar"><nav class="top-nav">'
    finishNav: str = f'</nav><aside class="user-nav"><a href="{prefix}login.html" id="accountIcon" class="material-symbols-outlined">account_circle</a><a href="{prefix}login.html" id="accountText">Login</a></aside></nav>'
    midSection: str = f'<main class="page"><header class="page-header"><img src="{prefix}assets/icons/{page.imgPath}" alt="{page.name}" class="miniIcon"><h1 class="page-title">{page.name}</h1></header><main class="page-content"><section class="content">'
    footer: str = f'</section><footer class="rightBarFooter"><p><a href="../../Jacob Leskowski/index.html" target="_blank" rel="noopener noreferrer">JackLeskowski</a></p></footer></main></main></main></body></html>'
    if type(allSites) is list:
        return (
            head
            + startNav
            + allNav(allSites, selected, subSelected)
            + finishNav
            + midSection
            + page.content
            + footer
        )
    return head + midSection + page.content + footer


def McKaylaify(page: str) -> str:
    soup: BeautifulSoup = BeautifulSoup(page, "html.parser")
    formated: str = soup.prettify()
    # count spaces until it's a non space character for each line
    newPage: str = ""
    for line in formated.splitlines():
        index: int = 0
        while line[index] == " ":
            index += 1
        newPage += line.replace(" " * index, " " * (4 * index)) + "\n"
    return newPage


def createSites(
    allSites: list[SiteInformation] = [],
    directory: str = os.getcwd(),
    allLinks: list[str] = [
        "style.css",
        "https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200",
    ],
) -> None:
    for site in allSites:
        os.makedirs(f"{directory}/{site.file}", exist_ok=True)
        for index, subSit in enumerate(site.children):
            page: str = createPage(allSites, allSites.index(site), index, allLinks)
            outputPath: str = (
                f"{directory}/{site.file}.html"
                if index == 0
                else f"{directory}/{site.file}/{subSit.file}.html"
            )
            with open(outputPath, "w") as f:
                f.write(McKaylaify(page))


def deleteAll(directory: str = os.getcwd()) -> list[str] | None:
    # saved folders

    with open("saveFolders.txt", "r") as f:
        saveFolders = [line.strip() for line in f.readlines()]

    for folder in [
        ".git",
        ".venv",
    ]:
        if folder not in saveFolders:
            saveFolders.append(folder)

    with open("saveFolders.txt", "w") as f:
        f.write("\n".join(saveFolders))

    # saved files

    with open("saveFiles.txt", "r") as f:
        saveFiles = [line.strip() for line in f.readlines()]

    for file in [
        ".gitignore",
        "website.json",
        "build.py",
        "clear.py",
        "saveFiles.txt",
        "saveFolders.txt",
    ]:
        if file not in saveFiles:
            saveFiles.append(file)

    with open("saveFiles.txt", "w") as f:
        f.write("\n".join(saveFiles))

    currentDir = directory
    killed: list[str] = []
    for item in os.listdir(currentDir):
        itemPath = os.path.join(currentDir, item)
        if os.path.isfile(itemPath):
            if item not in saveFiles:
                killed.append(itemPath)
                os.remove(itemPath)
        elif os.path.isdir(itemPath):
            if item not in saveFolders:
                killed.append(itemPath)
                shutil.rmtree(itemPath)
    return killed if killed else None


def saveSites(SITES: list[SiteInformation], filename: str = "website.json") -> None:

    guess: str = input(
        "THIS WILL REWRITE ALL OF THE SITES IN WEBSITE.JSON. INPUT THE PASSWORD TO CONTINUE: "
    )
    import uuid

    if guess != str(uuid.uuid4()):
        print("Incorrect password. Aborting.")
        return

    def SiteInformationToDict(site: SiteInformation) -> dict:
        return {
            "name": site.name,
            "content": site.content,
            "children": [SiteInformationToDict(child) for child in site.children]
            if site.children
            else [],
            "imgPath": site.imgPath,
            "links": site.links,
        }

    with open(filename, "w") as f:
        json.dump([SiteInformationToDict(site) for site in SITES], f, indent=4)


def loadSites(filename: str = "website.json") -> list[SiteInformation]:

    def dictToSiteInformation(
        data: dict[
            str, str | list[str] | list[dict[str, str | list[str]]]
        ],  # I'm not fact checking this annotation
    ) -> SiteInformation:
        # check for imgPath
        if "imgPath" not in data:
            data["imgPath"] = None
        return SiteInformation(
            name=data["name"],
            content=data["content"],
            children=[dictToSiteInformation(child) for child in data["children"]]
            if data["children"]
            else [],
            imgPath=data.get("imgPath"),
            links=data.get("links"),
        )

    with open(filename, "r") as f:
        data = json.load(f)
    return [dictToSiteInformation(site) for site in data]


def main() -> None:
    deleteAll()
    createSites(loadSites())


if __name__ == "__main__":
    main()
