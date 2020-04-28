import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fantasy_pi_server", # Replace with your own username
    version="0.0.1",
    author="Bernard Louis Alecu",
    author_email="bernard.alecu10@gmail.com",
    description="Flask application to serve data to our ui",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
