import pathlib

from setuptools import find_packages, setup

here = pathlib.Path(__file__).parent
long_description = (here / "README.md").read_text()

setup(
    name='flagger',
    version='0.1',
    description='Workflow as code',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/bbenabbes/flagger',
    author='Bilel BEN ABBES',
    author_email='bil.benabbes@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        "Topic :: Software Development :: Build Tools",
        "Topic :: Software Development :: Libraries :: Python Modules",
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
    ],
    include_package_data=True,
    packages=find_packages(exclude=['tests*']),
    python_requires='~=3.7',
    install_requires=[
        'celery==4.2.2',
        'click==7.0',
        'flake8==3.7.7',
        'isort== 4.3.16',
        'networkx==2.2',
        'pylint==2.3.1',
        'pytest==4.3.1',
        'pytest-cov==2.6.1',
        'SQLAlchemy==1.3.3',
    ],
    entry_points={
        'flagger.steps': [
            'DummyStep=flagger.steps.dummy_step:DummyStep',
        ],
    },
    zip_safe=False,
)
