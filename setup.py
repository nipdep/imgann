
from setuptools import setup
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(

    name='imgann',

    version='0.5.4',

    description='image annotation file operation provider.',

    long_description=long_description,

    long_description_content_type='text/markdown',

    url='https://github.com/nipdep/imgann.git',

    author='nipdep',

    author_email='nipun1deelaka@gmail.com',

    classifiers=[  # Optional

        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
    ],


    keywords='sample, setuptools, development',

    # package_dir={'': 'src'},

    # py_modules = ["helloworld"],
    packages=['imgann','imgann/operators'],

    python_requires='>=3.5, <4',

    install_requires=['numpy', 'pandas', 'matplotlib', 'opencv-python'],

    extras_require={
        'dev': ['check-manifest',
                'pytest>=3.7'],
        'test': ['coverage', 'unittest'],
    },

    # package_data={  # Optional
    #     'sample': ['package_data.dat'],
    # },

    # data_files=[('my_data', ['data/data_file'])],  # Optional

    # entry_points={  # Optional
    #     'console_scripts': [
    #         'hello=sample:main',
    #     ],
    # },

    project_urls={  # Optional
        'Bug Reports': 'https://github.com/nipdep/imgann/issues',
        # 'Funding': 'https://donate.pypi.org',
        # 'Say Thanks!': 'http://saythanks.io/to/example',
        'Source': 'https://github.com/nipdep/imgann/',
    },
)
