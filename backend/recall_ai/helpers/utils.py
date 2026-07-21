from datetime import timedelta
import logging
import os
import time
from concurrent_log_handler import ConcurrentRotatingFileHandler

def setup_logging():
    logger = logging.getLogger("recallAi")
    if not logger.hasHandlers():
        logger.setLevel(logging.INFO)
        log_dir = "logs"
        os.makedirs(log_dir, exist_ok=True)

        file_handler = ConcurrentRotatingFileHandler(
            os.path.join(log_dir, "recallAi.log"),
            maxBytes=10000,
            backupCount=500
        )
        file_handler.setLevel(logging.INFO)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(pathname)s - %(filename)s - %(lineno)d",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    return logger


def truthy(value) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y", "on"}

class ThinkStripper:
    """Remove <think>...</think> reasoning blocks from a token stream.

    Reasoning models (qwen3, deepseek-r1, ...) emit their chain-of-thought inline
    wrapped in <think></think> when Ollama's separate reasoning channel isn't used.
    This filter drops that content across chunk boundaries so only the final answer
    reaches the client. Feed each chunk, yield whatever it returns, then call flush().
    """

    _OPEN = "<think>"
    _CLOSE = "</think>"

    def __init__(self):
        self._buf = ""
        self._in_think = False

    def feed(self, text: str) -> str:
        if not text:
            return ""
        self._buf += text
        out = []
        while True:
            if not self._in_think:
                i = self._buf.find(self._OPEN)
                if i == -1:
                    # Emit everything except a possible partial "<think>" at the tail.
                    hold = len(self._OPEN) - 1
                    if len(self._buf) > hold:
                        out.append(self._buf[:len(self._buf) - hold])
                        self._buf = self._buf[len(self._buf) - hold:]
                    break
                out.append(self._buf[:i])
                self._buf = self._buf[i + len(self._OPEN):]
                self._in_think = True
            else:
                j = self._buf.find(self._CLOSE)
                if j == -1:
                    # Discard thinking; keep only a possible partial "</think>" at the tail.
                    hold = len(self._CLOSE) - 1
                    self._buf = self._buf[-hold:] if hold and len(self._buf) > hold else (self._buf if len(self._buf) <= hold else "")
                    break
                self._buf = self._buf[j + len(self._CLOSE):]
                self._in_think = False
        return "".join(out)

    def flush(self) -> str:
        # Emit any trailing text only if we're not mid-think (partial open tag counts as text).
        rem = "" if self._in_think else self._buf
        self._buf = ""
        return rem


def get_file_creation_age(file_path):
    if not os.path.exists(file_path):
        return None
    creation_time = os.path.getctime(file_path)  # Get creation time in seconds since epoch
    current_time = time.time() # Get current time in seconds since epoch
    age_seconds = current_time - creation_time # Calculate age in seconds
    days, remainder = divmod(int(age_seconds), 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, _ = divmod(remainder, 60)
    age_str = f"{days} days, {hours} hours, {minutes} minutes"
    age_timedelta = timedelta(seconds=age_seconds)
    return age_timedelta, age_str

