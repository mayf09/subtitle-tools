from setuptools import setup

setup(
    name='subtool',
    version='1.0.0',
    py_modules=['subtool'],
    install_requires=[
        'Click==7.1.2',
        'srt==3.4.1',
        'cos-python-sdk-v5==1.9.0',
        'tencentcloud-sdk-python==3.0.273',
    ],
    entry_points={
        'console_scripts': [
            'subtool = subtool:subtool',
        ],
    },
)