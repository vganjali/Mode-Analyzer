  # Mode Analyzer
  
  ![alt text](https://github.com/vganjali/Mode-Analyzer/blob/master/screenshots/1.png "GUI")
  
  A GUI program written in Python to analyze optical waveguide mode analysis. It opens popular image file formats i.e. *.JPG, *.TIFF, etc. and analyzes the intensity profiles along a line or averaged in a cross-section box. It's intended to be easy to use to do basic image corrections and analysis on optical mode profiles and MMI pattern analysis both for facet images and fluorescent images.
  
  # Prerequisites
  - Python (>= 3.6, might work with 2.7 not tried!)
  - Numpy (>= 1.13.3)
  - Scipy (>= 1.0.0)
  - Matplotlib (>= 2.1.1)
  - Pillow (>= 5.0.0)
  
  You can install all requirements using **pip install** command. Once installed, just simply cd to the main master folder and call **main.py** file via python (python main.py).
  
  # GUI
  
  ![alt text](https://github.com/vganjali/Mode-Analyzer/blob/master/screenshots/2.png "Main window")
  
  ![alt text](https://github.com/vganjali/Mode-Analyzer/blob/master/screenshots/3.png "Plot window")
  
  The main window consists of three main panels:
  - **Directory**: list of readable image files with datapoint copy and save buttons at the bottom
  - **Image**: Image view and profile plot graph at the bottom
  - **Settings**: Tabs of different analysis parameters
  
  There's a table to show statistics about detected peaks and fitted parameters. Here are the availble metrics for the latest version:
  - **Number of spots**: number of detected peaks based on the parameters set in peak find setting section. For optical profiles and MMI patterns, this number indicates number of bright spots.
  - **Full-Width-Half-Maxima (FWHM)**: FWHM based on extracted σ value from Gaussian fit:
  *FWHM = 2σ√(2 ln(2))*
  - **Peak to Valley**: the gap between average of peaks and valleys for detected peaks
  - **Δx**: the separation between detected peaks
  
  Average and standard deviation of the mentioned metrics are listed in the table.
  
  A pop up window with plot of actual values taken from raw data as well as Gaussian fits to the detected peaks in intensity plot. There are highlighted parts to show *peaks* and *valleys* and dashed lines showing averages of these parameters.
  
  ![alt text](https://github.com/vganjali/Mode-Analyzer/blob/master/screenshots/4.png "Plot window")
  
  
  # Reference
  This program was used to do MMI pattern analysis published in this paper:
  (will be great if you cite it if you find this program helpful in your study)
  
  1. [Stott, Matthew A., **Vahid Ganjalizadeh**, Maclain H. Olsen, Marcos Orfila, Johnny McMurray, Holger Schmidt, and Aaron R. Hawkins. "Optimized ARROW-based MMI waveguides for high fidelity excitation patterns for optofluidic multiplexing." IEEE journal of quantum electronics 54, no. 3 (2018): 1-7.](https://doi.org/10.1109/JQE.2018.2816120)
  
