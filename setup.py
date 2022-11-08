import sys, os
from setuptools import setup

dependencies = ['Pillow']

if os.path.exists('/sys/bus/platform/drivers/gpiomem-bcm2835'):
    dependencies += ['RPi.GPIO', 'spidev']
elif os.path.exists('/sys/bus/platform/drivers/gpio-x3'):
    dependencies += ['Hobot.GPIO', 'spidev']
else:
    dependencies += ['Jetson.GPIO']

setup(
    name='cornersign',
    description='CornerSign e-Paper Display',
    author='Yuri Fukuda',
    package_dir={'': 'lib'},
    packages=['waveshare_epd'],
    install_requires=dependencies,
)

