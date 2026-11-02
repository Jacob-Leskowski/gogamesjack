from php_gogamesjack import deleteAll
import os


def main() -> None:
    killed = deleteAll()
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
