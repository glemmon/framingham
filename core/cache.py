from __future__ import annotations
from typing import Any, Dict, Tuple
from cachetools import LRUCache

_cache = LRUCache(maxsize=128)

def cache_get(key: Tuple) -> Any:
    return _cache.get(key)

def cache_set(key: Tuple, value: Any) -> None:
    _cache[key] = value
