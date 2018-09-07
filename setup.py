from setuptools import setup, find_packages

version = '0.1.0'

requires = [
    'setuptools',
    'chaussette',
    'gevent',
    'retrying',
    'pytz',
    'pyramid',
    'pyramid_exclog',
    'request_id_middleware',
    'server_cookie_middleware'
]

test_requires = requires + [
    'webtest',
    'python-coveralls',
    'mock==1.0.1',
    'requests_mock==1.3.0',
    'bottle'
]

# api_requires = requires + [
#     'pyramid_exclog'
# ]

docs_requires = requires + [
    'sphinxcontrib-httpdomain',
]

entry_points = {
    'paste.app_factory': [
        'main = openprocurement.digital.signature:main'
    ],
    'console_scripts': [
        'digital_signature = openprocurement.digital.signature:main',
        'main = openprocurement.digital.signature:main'
    ]
}

setup(
    name='openprocurement.digital.signature',
    version=version,
    description="",
    long_description=open("README.md").read(),
    classifiers=[
        "Framework :: Pylons",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application"
    ],
    keywords='',
    author='ITVaan',
    author_email='',
    license='Apache License 2.0',
    url='https://github.com/ProzorroUKR/openprocurement.digital.signature.git',
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    extras_require={
        # 'api': api_requires,
        'test': test_requires,
        'docs': docs_requires,
    },
    entry_points=entry_points
)
