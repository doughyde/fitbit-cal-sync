from trackers.fitbit_tracker import FitbitTracker

__author__ = 'doughyde'


# FitBit connection
f = FitbitTracker()
f.authenticate()
f.get_devices()