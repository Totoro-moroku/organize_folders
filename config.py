import getpass

USER = getpass.getuser()

DOWNLOADS_PATH = "/Users/{}/Downloads/".format(USER)

DOCUMENTS_PATH = "/Users/{}/Documents/".format(USER)

SCREENSHOTS_PATH = "{}スクリーンショット/".format(DOCUMENTS_PATH)

BRAVE_PATH = "{}Brave/".format(DOWNLOADS_PATH)

SLACK_PATH = "{}Slack/".format(DOWNLOADS_PATH)

AFTER_ORGANIZE_PATH = "{}整理済み/".format(DOWNLOADS_PATH)
