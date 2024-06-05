from setuptools import setup, find_packages


# Read the requirements from the requirements.txt file
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(
    name='axiomic',
    version='0.0.3',
    packages=find_packages(),
    author='Victor Bittorf',
    author_email='bitfort@gmail.com',
    description='Primitives for Genreative AI.',
    url='https://github.com/axiomic-ai/axiomic',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=requirements,
    package_data={
        'axiomic': ['protos/axiomic.proto', 'core_data/**/*'],
    },
    entry_points={
        'console_scripts': [
            'axiomic_params = aximoic.tools.params:main',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
)

