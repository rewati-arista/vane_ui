import setuptools

setuptools.setup(
    name="vane",
    version="1.0.0",
    author="Arista",
    author_email="Arista",
    description="Test framework for Arista EOS+",
    long_description="Test framework for Arista EOS+",
    long_description_content_type="text/markdown",
    url="https://gitlab-gslab.act.arista.com/gslab-dev/vane",
    project_urls={
        "Bug Tracker": "https://gitlab-gslab.act.arista.com/gslab-dev/vane/issues",
    },
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
        'pytest-cov'
    ],
    python_requires=">=3.6",
    keywords=['vane', 'pytest'],
    zip_safe=False,
    include_package_data=True
)
