""" Package setup """
import setuptools

PACKAGE = "marketing"


def get_long_description():
    """
    Return long description from `README.md`.
    """
    with open("README.md", "r", encoding="utf-8") as fp:
        return fp.read()


setuptools.setup(
    name=PACKAGE,
    version="0.0.0",
    author="Mindspun",
    author_email="mindspun@mindspun",
    description="Mindspun Marketing",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    python_requires=">=3.5",
    install_requires=[
        "addict",
        "google-api-python-client",
        "google-auth-httplib2",
        "google-auth-oauthlib",
        "hubspot-api-client",
        "python-dotenv",
        "tld"
    ],
    extras_require={
        "dev": [
            "flake8",
            "flake8-quotes",
            "pylint<2.13.0"
            "pytest",
            "pytest-cov",
            "pytest-mock"
        ]
    }
)
