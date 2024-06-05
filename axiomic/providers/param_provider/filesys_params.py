
import os

import axiomic.configure.default_config as default_config
import axiomic.errors as errors
import axiomic.logalytics.explainers as explainers
import axiomic.utils.paramtool as paramtool

WEAVEROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BUILTIN_ROOT = os.path.join(WEAVEROOT, 'core_data')


def handle_missing_param_file(param_name, filepath):
    raise errors.WeaveError(f'Param file for \'{param_name}\' not found: {filepath}')


class FilesystemParamProviderImpl:
    '''
    A filesystem backed reference store.
    '''
    def __init__(self):
        self._root_dir = None

    def exists(self, name) -> bool:
        return os.path.exists(self._filename(name))

    def is_bucket(self, name) -> bool:
        '''
        :param name: the name of the param or bucket

        :return: True if the name is a bucket, and the bucket exists.
        '''
        filename = self._filename(name, suffix='')
        return os.path.isdir(filename)

    def _get_root_dir(self):
        if self._root_dir is None:
            self._root_dir = default_config.file_ref_store.data_path
        if self._root_dir is None:
            explainers.set_file_store_path()
        return os.path.abspath(self._root_dir)

    def get_ref_nav_breadcrumbs(self, name) -> str:
        filename = self._filename(name, '.txt')
        return {'file ref': filename}

    def get_default_value(self, name) -> str:
        '''
        Returns the default value for a given name by reading the store.
        '''
        return self._read_file(name)

    def _filename(self, name, suffix: str = '.txt') -> str:
        parts = paramtool.segment_param_name(name)
        if parts[0] == 'core':
            return self._builtin_filename(name, suffix)
        return self._external_filename(name, suffix)

    def _builtin_filename(self, name, suffix: str) -> str:
        parts = paramtool.segment_param_name(name)
        builtin_path = os.path.join(BUILTIN_ROOT, 'P', *parts[:-1], f'{parts[-1]}{suffix}')
        return builtin_path

    def _external_filename(self, name, suffix: str) -> str:
        root = self._get_root_dir()
        parts = paramtool.segment_param_name(name)
        return os.path.join(root, 'P', *parts[:-1],  f'{parts[-1]}{suffix}')

    def _assert_file_exists(self, name, suffix: str = '.txt'):
        filepath = self._filename(name, suffix)
        if not os.path.exists(filepath):
            explainers.missing_file_ref(name, filepath)

    def _read_file(self, name) -> str:
        self._assert_file_exists(name)
        with open(self._filename(name), 'r') as f:
            return f.read()



