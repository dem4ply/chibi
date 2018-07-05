try:
    from setuptools import setup, find_packages
except:
    from distutils.core import setup, find_packages

# here = os.path.abspath( os.path.dirname( __file__ ) )
# README = open(os.path.join( here, 'README.rst' ) ).read()

setup(name='chibi',
      version='0.1',
      description='',
      # long_description=README,
      license='',
      author='',
      author_email='',
      packages=find_packages(),
      install_requires=[ 'GitPython==2.1.5', 'requests==2.19.1' ],
      dependency_links = [],
      classifiers=[
          'Environment :: Console',
          'Intended Audience :: Developers',
          'Programming Language :: Python',
      ])
