#
# Post-process data using VisIt. Generates data files of
# - the spatial average of the square of the difference between the solution at t and t=0.
#
# Usage:
#    visit -nowin -cli -s /path/to/pp_aux_vars.py
#

# ========================================================================
#
# Imports
#
# ========================================================================
import sys
import subprocess as sp


# ========================================================================
#
# Function definitions
#
# ========================================================================
def save_curve(plotnum, fname):
    """Save curve data"""
    SetActivePlots(plotnum)
    HideActivePlots()
    SaveWindowAtts = SaveWindowAttributes()
    SaveWindowAtts.outputToCurrentDirectory = 1
    SaveWindowAtts.outputDirectory = "."
    SaveWindowAtts.fileName = fname
    SaveWindowAtts.family = 0
    SaveWindowAtts.format = SaveWindowAtts.CURVE
    SaveWindowAtts.width = 1024
    SaveWindowAtts.height = 1024
    SaveWindowAtts.screenCapture = 0
    SaveWindowAtts.saveTiled = 0
    SaveWindowAtts.quality = 80
    SaveWindowAtts.progressive = 0
    SaveWindowAtts.binary = 0
    SaveWindowAtts.stereo = 0
    SaveWindowAtts.compression = SaveWindowAtts.None
    SaveWindowAtts.forceMerge = 0
    # NoConstraint, EqualWidthHeight, ScreenProportions
    SaveWindowAtts.resConstraint = SaveWindowAtts.ScreenProportions
    SaveWindowAtts.advancedMultiWindowSave = 0
    SetSaveWindowAttributes(SaveWindowAtts)
    SaveWindow()
    HideActivePlots()


# ========================================================================
#
# Main
#
# ========================================================================

# Get the list of data
return_code = sp.call('ls -1v plt*/Header | tee movie.visit', shell=True)

# Open files
OpenDatabase("localhost:movie.visit", 0)

# Define expressions
DefineScalarExpression("error2",
                       "sqr(conn_cmfe(<[0]i:x_velocity>, <Mesh>)-x_velocity)")

# Integrate on the whole domain
AddPlot("Pseudocolor", "error2", 1, 1)
DrawPlots()
SetQueryFloatFormat("%g")
QueryOverTimeAtts = GetQueryOverTimeAttributes()
QueryOverTimeAtts.timeType = QueryOverTimeAtts.DTime  # Cycle, DTime, Timestep
QueryOverTimeAtts.startTimeFlag = 0
QueryOverTimeAtts.startTime = 0
QueryOverTimeAtts.endTimeFlag = 0
QueryOverTimeAtts.endTime = 1
QueryOverTimeAtts.strideFlag = 0
QueryOverTimeAtts.stride = 1
QueryOverTimeAtts.createWindow = 1
QueryOverTimeAtts.windowId = 2
SetQueryOverTimeAttributes(QueryOverTimeAtts)
SetActivePlots(0)
QueryOverTime("Weighted Variable Sum", do_time=1)

# Hide all curve plots
SetActiveWindow(2)
SetActivePlots(0)

HideActivePlots()
SetActivePlots(1)

# Save the square of the magnitude of velocity
save_curve(0, "error2")

sys.exit()
