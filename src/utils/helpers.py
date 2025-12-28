"""
Utility functions
"""
import logging
from loguru import logger
import sys


def setup_logging(log_level: str = "INFO"):
    """Setup logging configuration"""
    logger.remove()
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
        level=log_level
    )


class InterceptHandler(logging.Handler):
    """Intercept standard logging and redirect to loguru"""
    
    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno
        
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1
        
        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def format_currency(amount: float, currency: str = "INR") -> str:
    """Format currency for display"""
    if currency == "INR":
        if amount >= 10000000:  # 1 Crore
            return f"₹{amount/10000000:.2f} Cr"
        elif amount >= 100000:  # 1 Lakh
            return f"₹{amount/100000:.2f} L"
        else:
            return f"₹{amount:,.0f}"
    return f"{currency} {amount:,.2f}"
