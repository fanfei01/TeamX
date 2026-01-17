from setuptools import setup, find_packages

setup(
    name="lego-instruction-personalizer",
    version="1.0.0",
    description="Personalized building instruction experience for Lego sets",
    author="TeamX",
    packages=find_packages(),
    install_requires=[
        "PyPDF2>=3.0.0",
        "pdf2image>=1.16.0",
        "Pillow>=10.0.0",
    ],
    python_requires=">=3.7",
)
