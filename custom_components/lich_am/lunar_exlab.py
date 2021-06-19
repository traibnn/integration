""" (c) exlab247@gmail.com """
def __bootstrap__(lunar_file):
   global __bootstrap__, __loader__, __file__
   import sys, pkg_resources, imp
   __file__ = pkg_resources.resource_filename(__name__, lunar_file)
   __loader__ = None; del __bootstrap__, __loader__
   imp.load_dynamic(__name__,__file__)
lunar_file = 'lunar_exlab.so'
__bootstrap__(lunar_file)
