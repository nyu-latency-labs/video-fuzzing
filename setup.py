from setuptools import setup, find_namespace_packages

setup(name='videofuzzer',
      version='0.3',
      description='Configurable Video Generator',
      url='https://github.com/nyu-latency-labs/video-fuzzing/',
      author='Vinayak Agarwal',
      author_email='va2083@nyu.edu',
      license='MIT',
      packages=find_namespace_packages(include=['videofuzzer.*']), 
      zip_safe=False)