from setuptools import setup, find_packages


setup(
    name='soulsave',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'setuptools',
        'pyyaml'
    ],
    entry_points={
        'console_scripts': [
            'soulsave = SoulsSaveCLI:cli',
        ],
    },
    extras_require={
        "dev": ["pytest", "twine"]
    }
)
