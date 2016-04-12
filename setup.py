from setuptools import setup

setup(name='eventlog',
      version='0.0.1',
      description='Command line event logger',
      author='Jari Torniainen, Quantified Employee, Finnish Institute of Occupational Health',
      author_email='jari.torniainen@ttl.fi',
      url='https://github.com/jtorniainen/event-logger',
      license='MIT',
      packages=['eventlog'],
      package_dir={'eventlog': 'eventlog'},
      include_package_data=False,
      entry_points={"console_scripts":
                    ["eventlog = eventlog.eventlog:run_from_cli"]})
