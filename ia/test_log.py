from logging import getLogger
from logging.config import fileConfig

f=open("petit.ini")
fileConfig(f)
logger = getLogger("ia")
logger.error("no")
