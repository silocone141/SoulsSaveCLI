from setuptools import setup, find_packages


setup(
    name='soulsave-cli',
    version='0.2.0',
    packages=find_packages(),
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/silocone141/SoulsSaveCLI",
    author="silocone",
    license="MIT",
    include_package_data=True,
    install_requires=[
        'Click',
        'setuptools'
    ],
    entry_points={
        'console_scripts': [
            'soulsave = src:cli',
        ],
    },
    extras_require={
        "dev": ["twine"]
    }
)
