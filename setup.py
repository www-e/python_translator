from setuptools import setup, find_packages

setup(
    name='pdf-translator',
    version='1.0.0',
    description='Offline English to Arabic PDF Translator',
    packages=find_packages(),
    install_requires=[
        'PyPDF2>=3.0.1',
        'pdfplumber>=0.10.3',
        'reportlab>=4.0.7',
        'arabic-reshaper>=3.0.0',
        'python-bidi>=0.4.2',
        'argostranslate>=1.9.1',
        'tqdm>=4.66.1',
        'pillow>=10.1.0',
    ],
    python_requires='>=3.8',
)
