

# Define global settings

try:
    from local_settings import *
except ImportError:
    print "You must have a local_settings.py"