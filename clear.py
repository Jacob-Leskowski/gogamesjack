from build import deleteAll, createPage, SiteInformation
from bs4 import BeautifulSoup
import os


def addPrebuilt(site: SiteInformation, directory: str = os.getcwd()) -> None:
    page: str = createPage(site)
    print(page[310:350])
    soup = BeautifulSoup(page, "html.parser")
    formated: str = soup.prettify()
    with open(f"{directory}/index.html", "w") as f:
        f.write(formated)


def main() -> None:
    killed = deleteAll()

    landing: SiteInformation = SiteInformation(
        name="Error",
        content="<h2>Action Needed</h2><h3>Error: Unbuilt Website</h3><p>Please Run 'build.py' to build the website.</p>",
        imgPath="action.png",
    )
    addPrebuilt(landing)

    print()
    if killed:
        print(
            f"Removed the following files and folders:\n"
            + "\n".join(killed).removeprefix(os.getcwd() + "/")
        )
    else:
        print("No files were removed.")


if __name__ == "__main__":
    main()

# pip install beautifulsoup4 lxml html5lib requests
