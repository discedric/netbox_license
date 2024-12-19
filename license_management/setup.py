from setuptools import setup, find_packages

setup(
    name='license_management',
    version='0.1.0',
    author = 'Cedric Vaneessen',
    author_email = 'cedric.vaneessen@zabun.be',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'netbox',
    ],
    entry_points={
        'netbox.plugins': [
            'license_management = license_management',
        ],
    },
)
