
from pydantic_settings import BaseSettings
from typing import Optional
from pydantic import field_validator, ValidationError, Field

import axiomic.configure.default_config_explainers as dc_explainers

import os


class FileRefStoreConfig(BaseSettings):
    data_path: Optional[str] = Field(default=None, pre=True)

    class Config:
        env_file = ".env"
        env_prefix = "WEAVE_FILE_"
    
    @field_validator('data_path')
    def set_abs_path_and_validate_existence(cls, v):
        if v is not None:
            abs_path = os.path.abspath(v)
            if not os.path.exists(abs_path):
                dc_explainers.explain_missing_path("file_ref_store.data_path", abs_path, 
                                                   [f'mkdir -p {abs_path}',
                                                    'export WEAVE_FILE_DATA_PATH=/path/to/your/data',
                                                    'default_config.file_ref_store.data_path = "/path/to/your/data"'])
                raise ValueError(f"The specified path does not exist: {abs_path}")
            return abs_path
        return None


class LLMConfig(BaseSettings):
    verbose: Optional[bool] = False

    class Config:
        env_file = ".env"
        env_prefix = "WEAVE_TEXT_"


class ConsoleConfig(BaseSettings):
    color_tracebacks: Optional[bool] = True
    help_on_exit: Optional[bool] = True
    enable: Optional[bool] = True

    class Config:
        env_file = ".env"
        env_prefix = "WEAVE_CONSOLE_"


file_ref_store = FileRefStoreConfig()
llm_config = LLMConfig()
console_config = ConsoleConfig()