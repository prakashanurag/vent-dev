#coding=utf-8

# vent4us 15/04/20
# The MIT License (MIT)
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import numpy           as     np
import backend

'''
 These are for one particular mode only:
 * PC-BIPAP mode
 * PC-APRV
 ...
 TODO: Convert these to a dictionary or a dictionary read from a json files
 Thus on the system when someone changes the mode corresponding display is
 triggered. For now only one mode is displayed.
'''
__MODES__ = ['PC-BIPAP', 'PC-AC', 'PC-APRV', 'VC-MMV', 'ATC', 'SPN-PPS']

### PC-BIPAP
__XRANGE__  = (0, 10*np.pi)
__YRANGE__  = (-100, 100)
__SIZE__    = 400
__CADENCE__ = 100 # Every __CADENCE__ milliseconds
__PLOTS__ = [
    { 'name': 'Flow mBar', 'callback' : backend.plot_sine, 'xrange':__XRANGE__, 'yrange':__YRANGE__ },
    { 'name': 'Flow L/min', 'callback' : backend.plot_cosine, 'xrange':__XRANGE__, 'yrange':__YRANGE__ },
    { 'name': 'Volume mL', 'callback' : backend.plot_normal_dist, 'xrange':__XRANGE__, 'yrange':__YRANGE__ },
    { 'name': 'CPU util %', 'callback' : backend.get_cpu_stats, 'xrange':__XRANGE__, 'yrange':__YRANGE__ },
    #{ 'name': 'Memory MB', 'callback' : backend.get_mem_stats, 'xrange':__XRANGE__, 'yrange':__YRANGE__ },
]
__RT_VALUES__ = [ 'PEEP mBar', 'PIP mBar', 'PMean mBar', 'VTo mL', 'MVe L/min']
__CONFIG_VALUES__ = [ 'Valve', 'Alarms', 'Get Healthy', 'Good Heart', 'Feel Good', 'Likes', 'Airy', 'Light', 'Fast']
# Last value must be '' since the row and column overlap
__DIAL_VALUES__ = [ 'Valve', 'Alarms', 'Get Healthy', 'Good Heart', 'Feel Good', 'Likes', '']

### PC-APRV
'''
__XRANGE__ = (0, 10*np.pi)
__YRANGE__ = (-5, 6)
__SIZE__   = 200
__CADENCE__ = 100 # Every __CADENCE__ milliseconds
__PLOTS__ = [
    { 'name': 'Flow mBar', 'callback' : backend.plot_sine, 'xrange':__XRANGE__, 'yrange':__YRANGE__ },
    { 'name': 'Flow L/min', 'callback' : backend.plot_cosine, 'xrange':__XRANGE__, 'yrange':__YRANGE__ },
    { 'name': 'Volume mL', 'callback' : backend.plot_normal_dist, 'xrange':__XRANGE__, 'yrange':__YRANGE__ }
]
__RT_VALUES__ = [ 'PEEP mBar', 'PIP mBar', 'PMean mBar', 'VTo mL', 'MVe L/min']
__CONFIG_VALUES__ = [ 'Valve', 'Alarms', 'Get Healthy', 'Good Heart', 'Feel Good', 'Likes', 'Airy', 'Light', 'Fast']
__DIAL_VALUES__ = [ 'Valve', 'Alarms', 'Get Healthy', 'Good Heart', 'Feel Good', 'Likes', 'Airy']
'''
