
import dataclasses
import os



@dataclasses.dataclass
class Config:
    enable_caching: bool = True
    enable_file_cache: bool = False 
    enable_mem_cache: bool = True
    thought_crime_retry_count: int = 3
    data_root_dir: str = './axiomic_data'

    def get_data_filepath(self, dirname, filename):
        # return os.path.join({global_config.data_root_dir}/{dirname}/{filename})
        return os.path.abspath(os.path.join(self.data_root_dir, dirname, filename))


def set_global_config(cfg: Config):
    global global_config
    global_config = cfg



global_config = Config()