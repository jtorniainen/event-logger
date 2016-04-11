from setuptools import setup

setup(name='event_logger',
      version='0.0.1',
      description='Command line event logger',
      author='Jari Torniainen, Quantified Employee, Finnish Institute of Occupational Health',
      author_email='jari.torniainen@ttl.fi',
      url='https://github.com/jtorniainen/event-logger',
      license='MIT',
      packages=['event_logger'],
      package_dir={'event_logger': 'event_logger'},
      include_package_data=False,
      entry_points={"console_scripts":
                    ["event_logger = event_logger.event_logger:run_from_cli"]})
