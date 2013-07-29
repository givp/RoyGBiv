from setuptools import setup, find_packages

setup(
    name='RoyGBiv',
    version='0.3.1',
    url='https://github.com/givp/RoyGBiv',
    classifiers=[
        'Programming Language :: Python',
        ],
    include_package_data=True,
    description='A set of image color analysis tools',
    long_description=open("README.md").read(),
    packages=find_packages(),
    author='Giv Parvaneh',
    install_requires=['Pillow', 'colormath', 'numpy'],
    license="http://www.opensource.org/licenses/mit-license.php",
    )

