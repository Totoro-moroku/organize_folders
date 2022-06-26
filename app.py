import config
from organizedFile import file


def main():
    file.organizedFiles(config.BRAVE_PATH, config.AFTER_ORGANIZE_PATH)
    # file.organizedFiles(config.SLACK_PATH, config.AFTER_ORGANIZE_PATH)
    # file.organizedFiles(config.SCREENSHOTS_PATH, config.SCREENSHOTS_PATH)


if __name__ == '__main__':
    main()
