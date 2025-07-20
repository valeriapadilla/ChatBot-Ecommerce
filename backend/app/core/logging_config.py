import logging
import logging.config
import sys
from typing import Dict, Any
from app.config.app_config import app_settings


class LoggingConfig:
    """Logging configuration manager."""
    
    @staticmethod
    def setup_logging() -> None:
        """Setup application logging configuration."""
        logging_config = {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                },
                "detailed": {
                    "format": "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s",
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                }
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "level": app_settings.log_level.upper(),
                    "formatter": "default",
                    "stream": sys.stdout,
                },
                "file": {
                    "class": "logging.FileHandler",
                    "level": "INFO",
                    "formatter": "detailed",
                    "filename": "app.log",
                    "mode": "a",
                }
            },
            "loggers": {
                "app": {
                    "level": app_settings.log_level.upper(),
                    "handlers": ["console", "file"],
                    "propagate": False,
                },
                "uvicorn": {
                    "level": "INFO",
                    "handlers": ["console"],
                    "propagate": False,
                }
            },
            "root": {
                "level": "INFO",
                "handlers": ["console"],
            }
        }
        
        logging.config.dictConfig(logging_config)
        
        # Create logger for this module
        logger = logging.getLogger(__name__)
        logger.info("Logging configuration initialized") 