from setuptools import setup, find_packages

setup(
    name='RoyGBiv',
    version='0.2',
    url='https://github.com/givp/RoyGBiv',
    classifiers=[
        'Programming Language :: Python',
        ],
    include_package_data=True,
    description='A set of image analysis tools',
    long_description=open("README.md").read(),
    packages=find_packages(),
    author='Giv Parvaneh',
    license="http://www.opensource.org/licenses/mit-license.php",
    )

