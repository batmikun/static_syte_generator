from generator.constants import CONTENT_PATH
from generator.constants import PUBLIC_PATH
from generator.constants import STATIC_PATH
from generator.constants import TEMPLATE_PATH
from generator.generator import Generator
from helpers.helpers import copy_directories
from helpers.helpers import delete_public_directory


def main():
    # Removing Old Data
    delete_public_directory(PUBLIC_PATH)

    # Copying Necessary data to public
    copy_directories(STATIC_PATH, PUBLIC_PATH)

    # Generating html files
    generator = Generator()
    generator.generate_pages_recursive(
        CONTENT_PATH,
        TEMPLATE_PATH,
        PUBLIC_PATH,
    )


if __name__ == "__main__":
    main()

