from setuptools import setup, find_packages

setup(
    name="tv-price-scraper",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        'requests>=2.26.0',
        'beautifulsoup4>=4.9.3',
        'aiohttp>=3.8.1',
        'python-dotenv>=0.19.0',
        'lxml>=4.6.3',
    ],
    extras_require={
        'dev': [
            'pytest>=6.2.5',
            'pytest-asyncio>=0.16.0',
            'black>=21.5b2',
            'flake8>=3.9.2',
        ],
    },
    author="Chinelo Kwazu",
    author_email="nelokwaz@gmail.com",
    description="A web scraper for TV prices from various retailers",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
) 