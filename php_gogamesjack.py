from __future__ import annotations
import shutil
import json
import os


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


def deleteAll(directory: str = os.getcwd()) -> list[str] | None:
    # saved folders

    with open("saveFolders.txt", "r") as f:
        saveFolders = [line.strip() for line in f.readlines()]

    if ".git" not in saveFolders:
        saveFolders.append(".git")

    with open("saveFolders.txt", "w") as f:
        f.write("\n".join(saveFolders))

    # saved files

    with open("saveFiles.txt", "r") as f:
        saveFiles = [line.strip() for line in f.readlines()]

    for file in [
        "website.json",
        "php_gogamesjack.py",
        "php_clear.py",
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
                shutil.rmtree(itemPath)
    return killed if killed else None


def saveSites(SITES: list[siteInformation], filename: str = "website.json") -> None:

    guess: str = input(
        "THIS WILL REWRITE ALL OF THE SITES IN WEBSITE.JSON. INPUT THE PASSWORD TO CONTINUE: "
    )
    import uuid

    if guess != str(uuid.uuid4()):
        print("Incorrect password. Aborting.")
        return

    def siteInformationToDict(site: siteInformation) -> dict:
        return {
            "name": site.name,
            "content": site.content,
            "children": [siteInformationToDict(child) for child in site.children]
            if site.children
            else [],
            "imgPath": site.imgPath,
        }

    with open(filename, "w") as f:
        json.dump([siteInformationToDict(site) for site in SITES], f, indent=4)


def loadSites(filename: str = "website.json") -> list[siteInformation]:

    def dictToSiteInformation(
        data: dict[
            str, str | list[dict[str, str]]
        ],  # I'm not fact checking this annotation
    ) -> siteInformation:
        # check for imgPath
        if "imgPath" not in data:
            data["imgPath"] = None
        return siteInformation(
            name=data["name"],
            content=data["content"],
            children=[dictToSiteInformation(child) for child in data["children"]]
            if data["children"]
            else [],
            imgPath=data.get("imgPath"),
        )

    with open(filename, "r") as f:
        data = json.load(f)
    return [dictToSiteInformation(site) for site in data]


def main() -> None:
    deleteAll()
    createSites(loadSites())


if __name__ == "__main__":
    main()
