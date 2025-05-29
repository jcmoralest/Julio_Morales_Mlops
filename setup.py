from setuptools import setup, find_packages

setup(
    name="predictor-medico",
    version="2.0.0",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "pandas",
        "scikit-learn",
        "python-multipart",
        "pydantic",
        "pytest"
    ],
)