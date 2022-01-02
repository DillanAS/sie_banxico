import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sie_banxico",
    version="0.0.1",
    author="Dillan Aguirre Sedeño",
    author_email="dillan.as22@gmail.com",
    description="A python class for the Economic Information System (SIE) API of Banco de México.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DillanAS/sie_banxico",
    project_urls={
    'Source': 'https://github.com/DillanAS/',
    'Tracker': 'https://github.com/DillanAS/sie_banxico/issues',
    'Connect with me!': 'https://www.linkedin.com/in/dillanas22/',
    },
    keywords=['python', 'api', 'economic data', 'banxico', 'mexico'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6"
)