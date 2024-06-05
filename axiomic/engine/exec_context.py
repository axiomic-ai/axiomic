import axiomic.core_config as core_config

import sqlite3

DB_PATH = '/tmp/axiomic_cache.db'

def should_cache():
    return core_config.global_config.enable_caching

class ExecutionContext:
    def __init__(self, disk_cache=True):
        if not core_config.global_config.enable_file_cache:
            disk_cache = False
        self._mem_cache = {}
        self._mem_cache_enabled = True
        self._disk_cache_enabled = disk_cache
        if self._disk_cache_enabled:
            self._load_disk_cache()

    def __del__(self):
        self.flush_cache()

    def _load_disk_cache(self):
        self._mem_cache.update(load_cache(DB_PATH))

    def set_mem_cache_enable(self, enable: bool):
        self._mem_cache_enabled = enable

    def flush_cache(self):
        if self._disk_cache_enabled:
            save_cache(DB_PATH, self._mem_cache)

    def is_cached(self, node: any) -> bool:
        if not self._mem_cache_enabled:
            return False
        nodestr = str(node)
        return nodestr in self._mem_cache

    def get_cached(self, node: any) -> str:
        nodestr = str(node)
        return self._mem_cache[nodestr]

    def cache_put(self, node: any, value: str):
        nodestr = str(node)
        self._mem_cache[nodestr] = value

    def posion_cache(self, node: any):
        nodestr = str(node)
        if nodestr in self._mem_cache:
            del self._mem_cache[nodestr]


def load_cache(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS cache (key TEXT PRIMARY KEY, value TEXT)")
    cursor.execute("SELECT key, value FROM cache")
    cache = dict(cursor.fetchall())
    print('exec_context.load_cache: loaded cache of ', len(cache))
    conn.close()
    return cache

def save_cache(db_path, cache):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS cache (key TEXT PRIMARY KEY, value TEXT)")
    cursor.executemany("REPLACE INTO cache (key, value) VALUES (?, ?)", cache.items())
    conn.commit()
    conn.close()

