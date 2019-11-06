"""A setuptools based setup module.
See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""

from setuptools import setup

from os import path

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
   name='dash-obj-in-3dmesh',
   version='0.1dev',
   description='Some tools for getting Wavefront OBJ files into a dash 3dmesh graph',
   long_description=open('README.md').read(),
   long_description_content_type='text/markdown', 
   author='Jon',
   author_email='jonrobinson@hotmail.com',
   py_modules=['dash-obj-in-3dmesh.wav_obj_importer', 'dash-obj-in-3dmesh.geometry_tools', 'dash-obj-in-3dmesh._config'],  #same as name
   python_requires='>=3.5',
   install_requires=[
       'numpy', 
       'dash',
       'multimethod'
    ], #external packages as dependencies
)