from distutils.core import setup

setup(
    name="thermostat",
    version=0.1,
    packages=["thermostat.calendarevents", "thermostat.ui"],
    long_description="A python package that controls the RaspberryPi Thermostat",
    install_requires=["google-api-python-client", "oauth2client", "APScheduler", "Cython", "kivy"]
)
