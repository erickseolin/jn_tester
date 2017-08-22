from setuptools import setup

__version__ = '0.2.0'


def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name='jn_tester',
    version=__version__,
    description='Make tests and performance runs on python functions (for Jupyter Notebook).',
    packages=['jn_tester.professor', 'jn_tester.student'],
    long_description=readme(),
    author='Erick, Rodolfo, Angel, Fabio',
    url='https://github.com/erickseolin/jn_tester/',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Education',
        'Topic :: Utilities',
        'Topic :: Software Development :: Testing',
        'Framework :: IPython',
        'Programming Language :: Python :: 3'
    ],
    keywords='tests jupyter education',
    license='MIT',
    install_requires=[
        'dill',
        'memory_profiler',
        'psutil',
        'numpy',
        'pandas',
    ],
    zip_safe=False,
)
