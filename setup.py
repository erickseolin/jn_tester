from setuptools import setup
import os.path

__version__ = '0.1.0-Beta'

descr_file = os.path.join(os.path.dirname(__file__), 'README.md')

setup(
    name='jn_tester',
    version=__version__,

    packages=['jn_tester.professor', 'jn_tester.student'],

    description='Library to make tests and performance runs on python functions.'
                ' Visial interface for Jupyter Notebok',
    long_description=open(descr_file).read(),
    author='Erick, Rodolfo, Angel, Fabio',
    url='https://github.com/erickseolin/jn_tester/',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Testing',
        'Topic :: Jupiter Notebook',
    ],
    install_requires=[
        'dill',
        'memory_profiler',
        'psutil',
        'numpy',
        'pandas',
    ],
)