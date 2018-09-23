from setuptools import setup, find_packages

setup(name='pesc',
      version='0.1',
      description='API wrapper for ikus.pesc.ru',
      long_description='Really, the funniest around.',
      classifiers=['Development Status :: 3 - Alpha',
                   'License :: OSI Approved :: MIT License',
                   'Programming Language :: Python :: 3.7', 
                   'Topic :: Software Development ', ],
      keywords='pesc api',
      url='http://github.com/we1tkind/pesc',
      author='Alexander Erdyakov',
      author_email='sa@prg.re',
      license='MIT',
      packages=find_packages(),
      install_requires=[ 'requests', ],
      include_package_data=True,
      zip_safe=False)