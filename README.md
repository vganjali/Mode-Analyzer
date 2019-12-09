  # Peak Analyzer
  A GUI program written in Python to analyze optical waveguide mode analysis. It reads famous file formats i.e. *.JPG, *.TIFF, etc and analyze the intensity profiles along a line or averaged in a cross-section box.
  
  # Prerequisites
  - Python (=> 3.6)
  - Numpy (>= 1.13.3)
  - Scipy (>= 1.0.0)
  - Matplotlib (>= 2.1.1)
  - Pillow (>= 5.0.0)
  - PeakUtils (>= 1.1.0)
  
  You can install all requirements using **pip install** command. Once installed, just simply cd to the main master folder and call **main.py** file via python (python main.py).
  
  # GUI
  
  The main window consists of three main panels:
  - File list
  - Image view and profile plot
  - Analysis parameters and setting
  
  ## File list
  Shows all readable image files available in the selected directory. At the bottom part of this panel, there are options to copy all datapoints of the profile plot.
  ## Image View
  Shows the selected image file in actual scale (determined by pixel to micron ratio). User can place the analysis line/box at any place on the image and the results will be immediately updated. At the bottom, the raw profile plot of the selected section is shown.
  ## Settings
  All the required parameters for analysis are grouped into different sections.
