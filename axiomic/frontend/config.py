
import axiomic.core_config as core_config


class ToDeleteConfig:
    def __init__(self, cfg):
        self.cfg = cfg

    def _write(self):
        core_config.set_global_config(self.cfg)

    def disable_file_cache(self):
        self.cfg.enable_file_cache = False
        self._write()

    def enable_file_cache(self):
        self.cfg.enable_file_cache = True
        self._write()

    def disable_caching(self):
        self.cfg.enable_caching = False
        self._write()

    def enable_caching(self):
        self.cfg.enable_caching = True
        self._write()

    def set_thought_crime_retry_count(self, count):
        self.cfg.thought_crime_retry_count = count
        self._write()


# config = WeaveConfig(core_config.global_config)