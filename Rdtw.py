__author__ = 'Robert Evans'

import numpy as np

# Import R interfaces
from rpy2.robjects.packages import importr
from rpy2 import robjects
import rpy2.robjects.numpy2ri
rpy2.robjects.numpy2ri.activate()

# Import R Dynamic Time Warping library
R = rpy2.robjects.r
DTW = importr('dtw')

def drawGraphs(queryFile, referenceFile):
	with open(queryFile) as fquery:
		query = np.loadtxt(fquery,delimiter=",")
	with open(referenceFile) as freference:
		reference = np.loadtxt(freference,delimiter=",")

	alignment = R.dtw(query, reference, keep=True)

	dist = alignment.rx('distance')[0][0]

	R.X11()
	R.dtwPlotTwoWay(alignment)
	#R.title(main = "DTW distance: %s for %s vs %s" % (dist,queryFile,referenceFile))
	R.title(main = "DTW distance: %s for Horizontal spin vs Vertical spin" % (dist))

	R.X11()
	R.dtwPlotThreeWay(alignment,main="")
	#R.title(main = "DTW distance: %s for %s vs %s" % (dist,queryFile,referenceFile))
	R.title(main = "Warping function for Horizontal spin vs Vertical spin")

	from enableInteractivity import enableInteractivity
	enableInteractivity()

def getDTWdist(queryFile,referenceFile):
	with open(queryFile) as fquery:
		query = np.loadtxt(fquery,delimiter=",")
	with open(referenceFile) as freference:
		reference = np.loadtxt(freference,delimiter=",")
	alignment = R.dtw(query, reference, keep=True)
	dist = alignment.rx('distance')[0][0]
	return dist

if __name__=='__main__':
	import sys
	if (len(sys.argv)!=3):
		print "Usage: Rdtw <query_filename.csv> <reference_filename.csv>"
		sys.exit(0)
	sys.exit(drawGraphs(sys.argv[1],sys.argv[2]))