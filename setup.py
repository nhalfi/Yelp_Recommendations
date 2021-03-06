

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nhalfi",
    version="0.0.1",
    author="nhalfi",
    description="Healthy Restaurants on Yelp",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nhalfi/Yelp_Recommendations",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=['Yelp'],
    install_requires=['pandas', 'numpy', 'sklearn', 'nltk', 'pandas',
                      'dash==1.19.0', 'dash-bootstrap-components',
                      'dash-core-components', 'dash-html-components',
                      'dash-leaflet==0.1.13', 'Flask==1.1.2',
                      'flask-compress', 'plotly',
                      'dash-renderer', 'dash-table',
                      'future', 'Jinja2',
                      'requests'],
    python_requires=">=3.7"
)
