from setuptools import setup, find_packages

setup(
    name="coresync-python",
    version="2.4.0",
    description="Official Python SDK for S&R CoreSync ERP & Open Banking PSD2 Gateway",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="S&R CoreSync For Intelligent Solutions B.V.",
    author_email="dev@sr-coresync.com",
    url="https://sr-coresync.com/developer-portal.html",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Office/Business :: Financial :: Accounting"
    ],
    python_requires=">=3.8",
)
