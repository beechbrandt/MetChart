from setuptools import setup, find_packages

setup(name='MetChart',
      version='0.0.1',
      description='Web App for plotting weather information',
      author='Tom Edwards',
      author_email='tom.edwards@cityfinancial.co.uk',
      license='UNKNOWN',
      packages=find_packages(),
      include_package_data=True,
      install_requires=["matplotlib", "ujson", "flask"],
      entry_points = {
          'console_scripts' : [ 'start-MetChart=MetChart.MetChart:main'],
      },
      url="http://example.com"
      )
