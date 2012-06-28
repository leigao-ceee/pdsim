from distutils.core import setup, Extension
from Cython.Build import cythonize
from Cython.Distutils import build_ext
from Cython.Distutils.extension import Extension as CyExtension
import sys,shutil,os

if len(sys.argv)==1:
    sys.argv+=['build_ext','--inplace','install']
    #sys.argv+=['build_ext','install']
    
import Cython

#This will generate HTML to show where there are still pythonic bits hiding out
Cython.Compiler.Options.annotate = True

#Get the numpy include folder
import numpy

#Each of the Pure-Python or PYX files in this list will be compiled to a python module       
pyx_list = [
            "PDSim/misc/scipylike.pyx",
            "PDSim/flow/flow_models.py",
            "PDSim/flow/_sumterms.pyx",
            "PDSim/flow/_flow.pyx",
            "PDSim/scroll/scroll_geo.py",
            "PDSim/misc/_listmath.pyx",
            "PDSim/core/_core.pyx",
            ]

# Try to remove the generated files in the source tree 
# if you are doing an install to the normal location
if '--inplace' not in sys.argv:
    for pyx_file in pyx_list:
        f_root = pyx_file.rsplit('.',1)[0]
        for ending in ['.pyd','.so']:
            fname = f_root+ending
            try:
                os.remove(fname)
                print 'removed',fname
            except OSError:
                pass

ext_module_list = []
for pyx_file in pyx_list:
    sources = [pyx_file]
    #Try to find a PXD backpack if possible
    pxd_file = pyx_file.rsplit('.',1)[0]+'.pxd'
    if os.path.exists(pxd_file):
        sources+=[pxd_file]
    
    #Build an extension with the sources
    ext_name = pyx_file.rsplit('.',1)[0].replace('/','.')

    ext_module_list.append(CyExtension(ext_name,sources,language='c++'))
       
setup(
  name = 'PDSim',
  version = '0.0.1',
  author = "Ian Bell",
  author_email='ian.h.bell@gmail.com',
  url='http://pdsim.sourceforge.net',
  description = """A flexible open-source framework for the quasi-steady-state simulation of positive displacement machines including compressors and expanders""",
  packages = ['PDSim','PDSim.core','PDSim.flow','PDSim.plot','PDSim.scroll','PDSim.misc','PDSim.recip'],
  cmdclass={'build_ext': build_ext},
  ext_modules = ext_module_list,
  include_dirs = [numpy.get_include()]
)
