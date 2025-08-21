from loguru import logger

logger.remove()
logger.add(
    "app/logs/app.log",
    rotation="10 MB",
    retention="10 days",
    enqueue=True,
    backtrace=True,
    diagnose=True,
)

# logger.add(
#     lambda msg: print(msg, end=""),
#     level="INFO",
#     format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
#     colorize=True,
#     enqueue=True,
#     backtrace=True,
#     diagnose=True,
# )
