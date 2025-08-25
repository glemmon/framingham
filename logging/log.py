from __future__ import annotations
import time
import logging

logger = logging.getLogger("framingham")
logging.basicConfig(level=logging.INFO)

class action_log:
    def __init__(self, action: str):
        self.action = action
    def __enter__(self):
        self.t0 = time.time()
        logger.info("start %s", self.action)
    def __exit__(self, exc_type, exc, tb):
        dt = (time.time() - self.t0)*1000
        if exc:
            logger.exception("error %s in %.1f ms: %s", self.action, dt, exc)
        else:
            logger.info("end %s in %.1f ms", self.action, dt)
