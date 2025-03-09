import sys
import logging
from pathlib import Path
from loguru import logger

# ログファイルパス
LOG_FILE_PATH = Path("logs/app.log")
LOG_FILE_PATH.parent.mkdir(parents=True, exist_ok=True)

# ログのフォーマット
LOG_FORMAT = (
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
    "<level>{message}</level>"
)

# LoguruをFastAPIのログシステムと統合するためのインターセプター
class InterceptHandler(logging.Handler):
    def emit(self, record):
        # LoguruでキャプチャしたいPythonの標準ログレコードを取得
        logger_opt = logger.opt(depth=6, exception=record.exc_info)
        logger_opt.log(record.levelno, record.getMessage())

# ロガー設定
def setup_logger():
    # Loguruの設定
    logger.configure(
        handlers=[
            {"sink": sys.stdout, "format": LOG_FORMAT, "level": "INFO"},
            {"sink": LOG_FILE_PATH, "format": LOG_FORMAT, "level": "DEBUG", "rotation": "10 MB"},
        ]
    )
    
    # 標準のPythonロガーをLoguruにリダイレクト
    logging.basicConfig(handlers=[InterceptHandler()], level=logging.INFO)
    
    # 特定のライブラリのログレベルを調整
    for logger_name in ["uvicorn", "uvicorn.error", "fastapi"]:
        logging_logger = logging.getLogger(logger_name)
        logging_logger.handlers = [InterceptHandler()]
    
    return logger

# デフォルトロガーをエクスポート
app_logger = setup_logger()
# DevMarketerアプリケーション用のロガー
logger = app_logger.bind(name="devmarketer")
