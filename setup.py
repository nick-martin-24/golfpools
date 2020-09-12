from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='golfpools',
    version='0.1.0',
    author='Nick Martin',
    author_email='nsm5102@gmail.com',
    long_description=long_description,
    url='<https://github.com/nick-martin-24/golfpools>',
    packages=find_packages(),
    install_requires=[
        bs4,
        requests,
        selenium,
    ],
)
