import setuptools

with open("README.md", "r") as file:
    long_description = file.read()

setuptools.setup(
    name="basketball",
    version="0.0.1",
    install_requires=[
        "numpy",
        "scipy",
        "scikit-learn",
        "ipython",
        "jupyter",
        "click",
        "tqdm",
        "pandas",
        "beautifulsoup4",
        "lxml",
        "html5lib",
        "requests",
        "matplotlib",
        "clickutil",
        "pollster",
    ],
    extra_requires={
        "dev": [
            "twine",
            "flake8",
            "mypy",
            "pytest",
            "wheel"
        ]
    },
    author="Daniel Suo",
    author_email="danielsuo@gmail.com",
    description="Wrangling basketball data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/danielsuo/basketball",
    python_requires=">3.6",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ]
)
