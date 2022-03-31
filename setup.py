import setuptools

from vane import __version__, __author__

setuptools.setup(
    name="vane",
    version=__version__,
    author=__author__,
    author_email="Arista",
    description="Network Certification Tool",
    long_description="Network Certification Tool",
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(include=['vane', 'vane.*']),
    entry_points={
        'console_scripts': [
            'vane = vane.vane_cli:main',
        ]
    },
    install_requires=[
        'pytest',
        'pyyaml',
        'jinja2',
        'pyeapi',
        'python-docx',
        'openpyxl',
        'pytest-excel',
        'pytest-xdist',
        'pytest-html',
        'pytest-json',
        'pytest-cache',
        'pytest-sugar',
        'pytest-cov',
        'netmiko'
    ],
    python_requires=">=3.6",
    keywords=['vane', 'pytest'],
    zip_safe=False,
    include_package_data=True
)
