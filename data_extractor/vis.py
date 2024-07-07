from data_extractor.vis_files import plot_files
from data_extractor.vis_questions import plot_questions
from data_extractor.vis_timings import plot_timings
from data_extractor.vis_needs import plot_needs
import json
import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.rc('font', **{'sans-serif' : 'Arial',
                         'family' : 'sans-serif'})
mpl.rcParams['font.family'] = 'Arial'
mpl.rcParams['font.size'] = 12
mpl.rcParams['axes.titlesize'] = 14  # Title a little bigger
mpl.rcParams['axes.titleweight'] = 'bold'
mpl.rcParams['axes.labelsize'] = 14
mpl.rcParams['axes.labelweight'] = 'bold'
mpl.rcParams['axes.titlepad'] = 15
mpl.rcParams['axes.labelpad'] = 15

f = open('stats.json')
stats = json.load(f)

#
plot_questions(stats, plt)
# plot_timings(stats, plt)
# plot_files(stats, plt)
# plot_needs(stats, plt)


