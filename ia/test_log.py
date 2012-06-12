from logging import getLogger
from logging.config import fileConfig
from io import open

f=open(u"petit.ini")
fileConfig(f)
logger = getLogger(u"ia")
logger.error(u"no")
