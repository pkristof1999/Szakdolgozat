import logging

logger = logging.getLogger("app")
logger.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

fileHandler = logging.FileHandler("../../main/log/app.log", encoding="utf-8")
fileHandler.setFormatter(formatter)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(formatter)

logger.addHandler(fileHandler)
logger.addHandler(consoleHandler)