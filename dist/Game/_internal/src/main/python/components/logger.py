import os
import logging

logDirectory = os.path.join("", "src/main/log")
os.makedirs(logDirectory, exist_ok=True)

logger = logging.getLogger("app")
logger.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

fileHandler = logging.FileHandler(os.path.join(logDirectory, "app.log"), mode="a", encoding="utf-8")
fileHandler.setFormatter(formatter)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(formatter)

logger.addHandler(fileHandler)
logger.addHandler(consoleHandler)
