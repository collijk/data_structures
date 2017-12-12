from setuptools import setup, find_packages

setup(
    name='data_structures',
    version='0.1',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=[
        'pytest',
    ],
    author='James Collins',
    author_email='collijk@uw.edu',
)
