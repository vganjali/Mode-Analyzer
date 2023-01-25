import sys, os
#from qtconsole.mainwindow import background
if sys.version_info[0] < 3:
	import Tkinter as Tk
	import ttk as Ttk
	from Tkinter import StringVar
else:
	import tkinter as Tk
	import tkinter.ttk as Ttk
import matplotlib
if (10*sys.version_info[0]+sys.version_info[1]) >= 36:
	from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
else:
	from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import matplotlib.patches as patches
from matplotlib.figure import Figure


matplotlib.use('TkAgg')
# print(plt.style.available)

_background_color = '#000000'
_foreground_color = '#FFF'
# _dark_bg = '#0F1F30'
_dark_bg = '#000000'
_dark_fg = '#FFFFFF'
# _dark_border_1 = '#00AA00'
_dark_border_1 = '#AA9900'
_dark_border_2 = '#AAFF00'
_dark_border_3 = '#00FFAA'
_dark_bg_1 = '#333333'
_dark_fg_1 = '#AAAAAA'
# _dark_bg_2 = '#152515'
_dark_bg_2 = '#252515'

class MainWindow(Tk.Frame):
	#plt.style.use('bmh')
	#plt.style.use('Dark.mplstyle')
	Z = []
	FPthresh = []
	FPmindist = []
	def on_tree_select(self, event):
		self.clipboard_clear()
		item_text = self.theDirList.item(self.theDirList.selection(),"value")[0] + "\n"
		for item in self.theResultTable.selection():
			item_text +=  "\t" + self.theResultTable.item(item)["text"]
		item_text += "\n" + "-"*len(item_text) + "\n"
		item_text += "Avg: "
		for item in self.theResultTable.selection():
			item_text += "\t" + str(self.theResultTable.item(item, "value")[1])
		item_text += "\n"
		item_text += "STD: "
		for item in self.theResultTable.selection():
			item_text += "\t" + str(self.theResultTable.item(item, "value")[2])
		item_text += "\n"
		print(item_text)
		self.clipboard_append(item_text)
	
	def create_widgets(self):
		# Panels and frames
		self.theMainPanedWindow = Ttk.Panedwindow(self, orient=Tk.HORIZONTAL)
		self.theDirFrame = Ttk.Frame(self.theMainPanedWindow, width=300)
		self.thePlotFrame = Ttk.Frame(self.theMainPanedWindow, width=300)
		self.thePanelFrame = Ttk.Frame(self.theMainPanedWindow, width=208)
		self.theMainPanedWindow.add(self.theDirFrame, weight=1)
		self.theMainPanedWindow.add(self.thePlotFrame, weight=3)
		self.theMainPanedWindow.add(self.thePanelFrame, weight=1)

		self.theTab = Ttk.Notebook(self.thePanelFrame, width=220, height=200)
		self.thePanel = Ttk.Frame(self.theTab, width=100)
		self.theCS = Ttk.Frame(self.theTab, width=100)
		self.theScan = Ttk.Frame(self.theTab, width=100)
		self.theTab.add(self.thePanel, text='Plot')
		self.theTab.add(self.theCS, text='Cross Section')
		self.theTab.add(self.theScan, text=u'\u03bb Scan Plot')
		self.theDir = Ttk.LabelFrame(self.theDirFrame, text=' Directory ', labelanchor=Tk.N)
		self.theBatchSave = Ttk.LabelFrame(self.theDirFrame, text=' Save Data ', labelanchor=Tk.N)
		self.theImage = Ttk.LabelFrame(self.thePlotFrame, text=' Image ', labelanchor=Tk.N)
		self.thePlot = Ttk.LabelFrame(self.thePlotFrame, text=' Field Plot ',
								width=800, height=200)
		self.theStatusBar = Ttk.Frame(self.master, height=20, borderwidth=0)
		self.theStatus = Ttk.Label(self.theStatusBar, text="Idle")
		self.theProgressbar = Ttk.Progressbar(self.theStatusBar,
										 value=50, maximum=100, length=200)
		self.theStatusMsg = Ttk.Label(self.theStatusBar, text="Error")
		
		
		self.Pixel2um = Tk.StringVar()
		self.GridSize = Tk.StringVar()
		self.FPthresh = Tk.StringVar()
		self.FPmindist = Tk.StringVar()
		self.FitAmpBoundL = Tk.StringVar()
		self.FitAmpBoundU = Tk.StringVar()
		self.FitMuBoundL = Tk.StringVar()
		self.FitMuBoundU = Tk.StringVar()
		self.FitSigmaBoundL = Tk.StringVar()
		self.FitSigmaBoundU = Tk.StringVar()
		self.ValleyOffset = Tk.StringVar()
		self.Rotation = Tk.StringVar()
		self.PlotMode = Tk.StringVar()
		self.Normalize = Tk.IntVar()
		self.PFMethod = Tk.StringVar()
		self.CSWidth = Tk.StringVar()
		self.CSHeight = Tk.StringVar()
		self.ScanFrom = Tk.StringVar()
		self.ScanTo = Tk.StringVar()
		self.Pixel2um.set("4")
		self.GridSize.set("100")
		self.FPthresh.set("0.4")
		self.FPmindist.set("5")
		self.FitAmpBoundL.set("0.5")
		self.FitAmpBoundU.set("1.0")
		self.FitMuBoundL.set("-3")
		self.FitMuBoundU.set("3")
		self.FitSigmaBoundL.set("0.1")
		self.FitSigmaBoundU.set("3")
		self.ValleyOffset.set("1")
		self.Rotation.set("0")
		self.CSWidth.set("100")
		self.CSHeight.set("10")
		self.ScanFrom.set("430")
		self.ScanTo.set("670")
		self.fig1 = Figure(figsize=(5, 2), dpi=100, facecolor=_dark_bg)
		self.fig1.subplots_adjust(left=0.08,right=.99,bottom=.17,top=0.99)
		self.ax1 = self.fig1.add_subplot(111)
		self.ax1.set_xlabel('X [$\mu$m]')
		self.ax1.set_ylabel('Intensity [a.u.]')
		self.ax1.set_xlim(auto=True)
		self.ax1.set_ylim(auto=True)
		self.ax1.Line0, = self.ax1.plot([], 'y-')
		# ax.set_title('Title Here')
		self.fig2 = Figure(figsize=(2, 3), dpi=100, facecolor=_dark_bg)
		self.fig2.subplots_adjust(left=0.15,right=0.95,bottom=.17,top=0.99)
		self.ax2 = self.fig2.add_subplot(111)
		self.ax2.set_xlabel('X [$\mu$m]')
		self.ax2.set_ylabel('Y [$\mu$m]')
		self.ax2.grid(True, which='both')
		self.ax2.minorticks_on()
		#self.ax2.axis('off')
		#self.ax2.axis('image')
		#plt.rc('xtick', color='r', labelsize='medium', direction='out')
		self.ax2.Line0, = self.ax2.plot([], 'r-')
		self.ax2.Line1, = self.ax2.plot([], 'y:')
		self.ax2.Line2, = self.ax2.plot([], 'v')
		self.ax2.Line3, = self.ax2.plot([], 'o')
		self.ax2.Line4, = self.ax2.plot([])
		self.ax2.sl, = self.ax2.plot([], 'm-.')
		self.ax2.cs = self.ax2.add_patch(patches.Rectangle((0.0, 0.0), 0.0, 0.0, 
														   hatch='xx', fill=False, alpha=0.7, 
														   facecolor='none', edgecolor='Magenta',
														   linestyle='dashed'))
		self.ax2.set_xlim(auto=True)
		self.ax2.set_ylim(auto=True)
		
		self.theButtonRead = Ttk.Button(self.thePanel,text="Read", width=10,
										   command=lambda: {})
		self.theButtonConnect = Ttk.Button(self.thePanel,text="Connect", width=10,
										command=lambda: self.theProgressbar.grid())
		self.theButtonSetCS = Ttk.Button(self.theCS,text="Set", width=5,
										command=lambda: {})
		self.theButtonScan = Ttk.Button(self.theScan,text="Make Plot", width=12,
										   command=lambda: {})
		self.theButtonSaveAsImage = Ttk.Button(self.theBatchSave,text="Image", width=10,
										   command=lambda: {})
		self.theButtonSaveAsText = Ttk.Button(self.theBatchSave,text="Text", width=10,
										   command=lambda: {})
		self.theButtonCopy = Ttk.Button(self.theBatchSave,text="Copy", width=10,
										   command=lambda: {}) 
		self.theButtonCopyWavelet = Ttk.Button(self.theBatchSave,text="Copy", width=10,
										   command=lambda: {}) 
		self.theButtonBrowse = Ttk.Button(self.theDir,text="Browse", width=10,
										   command=lambda: {})
		self.theDirList = Ttk.Treeview(self.theDir, selectmode='browse', show='headings')
		self.theDirListScrollbar = Ttk.Scrollbar(self.theDir, orient=Tk.VERTICAL, command=self.theDirList.yview)
		self.theDirList['columns'] = ('Filename')
		self.theDirList.column('Filename', width=200, minwidth=8, anchor='w')
		self.theDirList.heading('Filename', text='Directory', anchor=Tk.W)
		self.theDirList.tag_configure('odd', background=_dark_bg_2)
		
		self.theLbl_saveas = Ttk.Label(self.theBatchSave, text=" Save as: ")
		self.theLbl_copydatapoints = Ttk.Label(self.theBatchSave, text=" Copy data points: ")
		self.theLbl_copyaswavelet = Ttk.Label(self.theBatchSave, text=" Copy as wavelet: ")
		self.theLbl_choosedir = Ttk.Label(self.theDir, text=" Choose a directory: ")
		self.theLbl_p2u = Ttk.Label(self.thePanel, text=u" Pixel to \u03bcm ratio: ")
		self.thePixel2umInput = Ttk.Entry(self.thePanel, textvariable=self.Pixel2um, width=8)
		self.theLbl_gridsize = Ttk.Label(self.thePanel, text=u" Grid size [\u03bcm]: ")
		self.theGridSizeInput = Ttk.Entry(self.thePanel, textvariable=self.GridSize, width=8)
		self.theLbl_rotangle = Ttk.Label(self.thePanel, text=" Rotation angle: ")
		self.theRotationInput = Ttk.Entry(self.thePanel, textvariable=self.Rotation, width=8)
		self.theLbl_peakfindsetting = Ttk.Label(self.thePanel, text="Peak find settings", background=_dark_bg_2, anchor=Tk.CENTER)
		self.theLbl_peaksthresh = Ttk.Label(self.thePanel, text=" Threshold: ")
		self.theFPThreshInput = Ttk.Entry(self.thePanel, textvariable=self.FPthresh, width=8)
		self.theLbl_peaksmindist = Ttk.Label(self.thePanel, text=u" Min distance [\u03bcm]: ")
		self.theFPMinDistInput = Ttk.Entry(self.thePanel, textvariable=self.FPmindist, width=8)
		self.theLbl_fittingmethod = Ttk.Label(self.thePanel, text=" Method: ")
		self.theLbl_plotmode = Ttk.Label(self.thePanel, text=" Plot mode: ")
		self.thePlotMode = Ttk.Combobox(self.thePanel, textvariable=self.PlotMode, width=16)
		self.thePlotMode['values'] = ('Single Line', 'Integral over Box')
		self.thePlotMode.set(self.thePlotMode['values'][0])
		self.theNormalizeCheck = Ttk.Checkbutton(self.thePanel, text=" Normalize ", variable=self.Normalize)
		self.thePeakFinderMethod = Ttk.Combobox(self.thePanel, textvariable=self.PFMethod, width=16)
		self.thePeakFinderMethod['values'] = ('Dominant Peak', 'First Derivative', 'Second Derivative')
		self.thePeakFinderMethod.set(self.thePeakFinderMethod['values'][0])
		self.theLbl_curvefitsetting = Ttk.Label(self.thePanel, text="Curve fit settings", image=self.GaussImg, compound='bottom', background=_dark_bg_2, anchor=Tk.CENTER)
		self.theLbl_fitampboundl = Ttk.Label(self.thePanel, text=" a lower bound [relative]: ")
		self.theFitAmpBoundLInput = Ttk.Entry(self.thePanel, textvariable=self.FitAmpBoundL, width=8)
		self.theLbl_fitampboundu = Ttk.Label(self.thePanel, text=" a upper bound [relative]: ")
		self.theFitAmpBoundUInput = Ttk.Entry(self.thePanel, textvariable=self.FitAmpBoundU, width=8)
		self.theLbl_fitmuboundl = Ttk.Label(self.thePanel, text=u" \u03bc lower bound [\u03bcm]: ")
		self.theFitMuBoundLInput = Ttk.Entry(self.thePanel, textvariable=self.FitMuBoundL, width=8)
		self.theLbl_fitmuboundu = Ttk.Label(self.thePanel, text=u" \u03bc upper bound [\u03bcm]: ")
		self.theFitMuBoundUInput = Ttk.Entry(self.thePanel, textvariable=self.FitMuBoundU, width=8)
		self.theLbl_fitsigmaboundl = Ttk.Label(self.thePanel, text=u" \u03c3 lower bound [\u03bcm]: ")
		self.theFitSigmaBoundLInput = Ttk.Entry(self.thePanel, textvariable=self.FitSigmaBoundL, width=8)
		self.theLbl_fitsigmaboundu = Ttk.Label(self.thePanel, text=u" \u03c3 upper bound [\u03bcm]: ")
		self.theFitSigmaBoundUInput = Ttk.Entry(self.thePanel, textvariable=self.FitSigmaBoundU, width=8)
		self.theLbl_valleyoffset = Ttk.Label(self.thePanel, text=u" Valley offset [\u00B1\u03bcm]: ")
		self.theValleyOffsetInput = Ttk.Entry(self.thePanel, textvariable=self.ValleyOffset, width=8)
		
		self.theResultTable = Ttk.Treeview(self.thePanelFrame, selectmode='extended', show='headings', height=6)
		self.theLbl_cswidth = Ttk.Label(self.theCS, text=u" Width [\u03bcm]: ")
		self.theCSWidthInput = Ttk.Entry(self.theCS, textvariable=self.CSWidth, width=10)
		self.theLbl_csheight = Ttk.Label(self.theCS, text=u" Height [\u03bcm]: ")
		self.theCSHeightInput = Ttk.Entry(self.theCS, textvariable=self.CSHeight, width=10)
		self.theLbl_csorigin = Ttk.Label(self.theCS, text=" Origin [left-bottom]: ")
		
		self.theLbl_scan = Ttk.Label(self.theScan, text=" Scan Wavelength (from - to): ")
		self.theScanFromInput = Ttk.Entry(self.theScan, textvariable=self.ScanFrom, width=8)
		self.theScanToInput = Ttk.Entry(self.theScan, textvariable=self.ScanTo, width=8)

		self.theResultTable['columns'] = ('Parameter', 'Average', 'STD')
		self.theResultTable.column('Parameter', width=116, minwidth=116, anchor='w')
		self.theResultTable.column('Average', width=50, minwidth=50, anchor='center')
		self.theResultTable.column('STD', width=50, minwidth=50, anchor='center')
#         self.theResultTable.heading('#0', text='Parameter')
		self.theResultTable.heading('Parameter', text='Parameter')
		self.theResultTable.heading('Average', text='Average')
		self.theResultTable.heading('STD', text='STD')
		self.theResultTable.insert('', 'end', text='Spots', values=('Number of Spots', '-', '-'), tags='odd')
		self.theResultTable.insert('', 'end', text='FWHM', values=('FWHM', '-', '-'), tags='even')
		self.theResultTable.insert('', 'end', text='P2V', values=('Peak to Valley', '-', '-'), tags='odd')
		self.theResultTable.insert('', 'end', text=u'\u0394X', values=(u'\u0394X', '-', '-'), tags='even')
		self.theResultTable.insert('', 'end', text='SNR', values=('SNR', '-', '-'), tags='odd')
#         self.theResultTable.insert('', 'end', text='Listbox', values=('', ''), tags='even')
		self.theResultTable.tag_configure('odd', background=_dark_bg_2)
		self.theResultTable.bind("<<TreeviewSelect>>", self.on_tree_select)
		self.theResultTable.bind("<ButtonRelease-3>", self.on_tree_select)
#         self.theHSeparator = Ttk.Separator(self.thePanel, orient=Tk.HORIZONTAL)
		self.theDirList.configure(yscrollcommand= self.theDirListScrollbar.set)
		self.canvas1 = FigureCanvasTkAgg(self.fig1, master=self.thePlot)
		self.canvas1.draw()
		self.canvas1.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
		if (10*sys.version_info[0]+sys.version_info[1]) >= 36:
			self.toolbar1 = NavigationToolbar2Tk(self.canvas1, self.thePlot)
		else:
			self.toolbar1 = NavigationToolbar2TkAgg(self.canvas1, self.thePlot)
		
		self.canvas2 = FigureCanvasTkAgg(self.fig2, master=self.theImage)
		self.canvas2.draw()
		self.canvas2.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
		if (10*sys.version_info[0]+sys.version_info[1]) >= 36:
			self.toolbar2 = NavigationToolbar2Tk(self.canvas2, self.theImage)
		else:
			self.toolbar2 = NavigationToolbar2TkAgg(self.canvas2, self.theImage)
		
		# Arrange Widgets
		Ttk.Sizegrip(self.master).grid(row=1, column=1, sticky=Tk.SE)
		self.grid(row=0, columnspan=2, sticky=Tk.NSEW)
		self.rowconfigure(0, minsize=200, weight=1)
		self.columnconfigure(0, weight=1)
		# self.columnconfigure(0, minsize=200, weight=0)
		# self.columnconfigure(1, minsize=300, weight=1)
		# self.columnconfigure(2, minsize=208, weight=0)
		self.theDirFrame.rowconfigure(0, minsize=300, weight=1)
		self.theDirFrame.rowconfigure(1, minsize=100, weight=0)
		self.theDirFrame.columnconfigure(0, minsize=100, weight=1)
		self.thePlotFrame.rowconfigure(0, minsize=200, weight=3)
		self.thePlotFrame.rowconfigure(1, minsize=200, weight=1)
		self.thePlotFrame.columnconfigure(0, weight=1)
		self.thePanelFrame.rowconfigure(0, minsize=400, weight=1)
		self.thePanelFrame.rowconfigure(1, minsize=100, weight=0)
		self.thePanelFrame.columnconfigure(0, minsize=100, weight=1)
		# self.theDirFrame.grid(row=0, column=0, padx=2, pady=1, sticky=Tk.NSEW)
		# self.thePlotFrame.grid(row=0, column=1, padx=2, pady=1, sticky=Tk.NSEW)
		# self.thePanelFrame.grid(row=0, column=2, padx=2, pady=1, sticky=Tk.NS)
		self.theTab.grid(row=0, column=0, columnspan=2, padx=0, pady=2, sticky=Tk.NSEW)
		self.theDir.grid(row=0, column=0, padx=0, pady=1, sticky=Tk.NSEW)
		self.theBatchSave.grid(row=1, column=0, padx=0, pady=1, sticky=Tk.NSEW)
		# self.theImage.grid(row=0, column=0, padx=2, pady=1, sticky=Tk.NSEW)
		# self.thePlot.grid(rowspan=2, column=0, padx=4, pady=2, sticky=Tk.NSEW)
		self.theImage.grid(row=0, column=0, padx=2, pady=1, sticky=Tk.NSEW)
		self.thePlot.grid(row=1, column=0, padx=4, pady=2, sticky=Tk.NSEW)
		self.theMainPanedWindow.grid(row=0, column=0, padx=2, pady=1, sticky=Tk.NSEW)
#         self.thePlot.grid_remove()
		self.theStatusBar.grid(row=1, column=0, padx=4, sticky=Tk.NSEW)
#         self.theHSeparator.grid(row=1, sticky=Tk.EW)
		self.theStatus.grid(row=0, column=1)
		self.theProgressbar.grid(row=0, column=0)
		self.theProgressbar.grid_remove()
		#self.theButtonRead.grid(row=0, column=1, padx=4, pady=4)
		#self.theButtonConnect.grid(row=0, column=3, padx=4, pady=4)
#        self.theButtonSaveAsImage.grid(row=1, column=2, padx=4, pady=4)
		self.theLbl_saveas.grid(row=0, columnspan=3, sticky=Tk.W)
		self.theButtonSaveAsText.grid(row=0, column=3, padx=4, ipady=2, pady=2, sticky=Tk.EW)
		self.theLbl_copydatapoints.grid(row=1, columnspan=3, sticky=Tk.W)
		self.theButtonCopy.grid(row=1, column=3, padx=4, ipady=2, pady=2, sticky=Tk.EW)
		self.theLbl_copyaswavelet.grid(row=2, columnspan=3, sticky=Tk.W)
		self.theButtonCopyWavelet.grid(row=2, column=3, padx=4, ipady=2, pady=2, sticky=Tk.EW)
		self.theLbl_choosedir.grid(row=1, columnspan=3, sticky=Tk.W)
		self.theButtonBrowse.grid(row=1, column=3, columnspan=3, padx=4, ipady=2, pady=4, sticky=Tk.EW)
		self.theDir.grid_rowconfigure(2, weight=1)
		self.theDirList.grid(row=2, columnspan=4, pady=2, sticky=Tk.NSEW)
		self.theDirListScrollbar.grid(row=2, column=4, pady=2, sticky=Tk.NS)
		self.theLbl_p2u.grid(row=1, columnspan=4, sticky=Tk.W)
		self.thePixel2umInput.grid(row=1, column=4, padx=4, pady=2)
		self.theLbl_gridsize.grid(row=2, columnspan=4, sticky=Tk.W)
		self.theGridSizeInput.grid(row=2, column=4, padx=4, pady=2)
		self.theLbl_rotangle.grid(row=3, columnspan=4, sticky=Tk.W)
		self.theRotationInput.grid(row=3, column=4, padx=4, pady=2)   
		self.theLbl_peakfindsetting.grid(row=4, columnspan=5, sticky=Tk.EW)
		self.theLbl_peaksthresh.grid(row=5, columnspan=4, sticky=Tk.W)
		self.theFPThreshInput.grid(row=5, column=4, padx=4, pady=2)
		self.theLbl_peaksmindist.grid(row=6, columnspan=4, sticky=Tk.W)
		self.theFPMinDistInput.grid(row=6, column=4, padx=4, pady=2)     
		self.theLbl_plotmode.grid(row=7, columnspan=2, sticky=Tk.W)
		self.thePlotMode.grid(row=7, columnspan=6, sticky=Tk.E, padx=4, pady=2)
		self.theNormalizeCheck.grid(row=8, columnspan=2, sticky=Tk.W, padx=4, pady=2)
		#self.theLbl_fittingmethod.grid(row=8, columnspan=2, sticky=Tk.W)
		#self.thePeakFinderMethod.grid(row=8, columnspan=6, sticky=Tk.E, padx=4, pady=2)
		self.theLbl_curvefitsetting.grid(row=9, columnspan=5, sticky=Tk.EW)
		self.theLbl_fitampboundl.grid(row=10, columnspan=4, sticky=Tk.W)
		self.theFitAmpBoundLInput.grid(row=10, column=4, padx=4, pady=2)   
		self.theLbl_fitampboundu.grid(row=11, columnspan=4, sticky=Tk.W)
		self.theFitAmpBoundUInput.grid(row=11, column=4, padx=4, pady=2)
		self.theLbl_fitmuboundl.grid(row=12, columnspan=4, sticky=Tk.W)
		self.theFitMuBoundLInput.grid(row=12, column=4, padx=4, pady=2)
		self.theLbl_fitmuboundu.grid(row=13, columnspan=4, sticky=Tk.W)
		self.theFitMuBoundUInput.grid(row=13, column=4, padx=4, pady=2)
		self.theLbl_fitsigmaboundl.grid(row=14, columnspan=4, sticky=Tk.W)
		self.theFitSigmaBoundLInput.grid(row=14, column=4, padx=4, pady=2)
		self.theLbl_fitsigmaboundu.grid(row=15, columnspan=4, sticky=Tk.W)
		self.theFitSigmaBoundUInput.grid(row=15, column=4, padx=4, pady=2)
		self.theLbl_valleyoffset.grid(row=16, columnspan=4, sticky=Tk.W)
		self.theValleyOffsetInput.grid(row=16, column=4, padx=4, pady=2)
		
		self.theLbl_cswidth.grid(row=0, columnspan=2, sticky=Tk.W)
		self.theCSWidthInput.grid(row=0, column=2, padx=4, pady=2)
		self.theLbl_csheight.grid(row=1, columnspan=2, sticky=Tk.W)
		self.theCSHeightInput.grid(row=1, column=2, padx=4, pady=2)
		self.theLbl_csorigin.grid(row=3, columnspan=2, sticky=Tk.W)
		self.theButtonSetCS.grid(row=3, column=2, padx=4, pady=2, sticky=Tk.EW)
		
		self.theLbl_scan.grid(row=0, columnspan=3, sticky=Tk.W)
		self.theScanFromInput.grid(row=1, column=0, padx=4, pady=2)
		self.theScanToInput.grid(row=1, column=1, padx=4, pady=2)
		self.theButtonScan.grid(row=1, column=2, padx=4, pady=2)
#         self.theHSeparator.grid(row=6, sticky=Tk.EW)
		self.theResultTable.grid(row=1, column=0, sticky=Tk.NSEW)
		self.thePanel.grid_columnconfigure(0, weight=1)
		self.theCS.grid_columnconfigure(0, weight=1)
		self.theScan.grid_columnconfigure(0, weight=1)
		self.theDir.grid_columnconfigure(0, weight=1)
		self.theBatchSave.grid_columnconfigure(0, weight=1)
		
#         self.thePeakFinderMethod.bind('<<ComboboxSelected>>', function)
		
	# create main window frame
	def __init__(self,master=None):
		Tk.Frame.__init__(self, master)
		master.title('MMI Pattern Analyzer')
		program_directory=sys.path[0]
		self.GaussImg = Tk.PhotoImage( \
		file=os.path.join(program_directory,'gauss.gif'))
		imgicon = Tk.PhotoImage(file=os.path.join(program_directory,'icon.gif'))
		master.tk.call('wm', 'iconphoto', master._w, imgicon)
		#master.iconbitmap(os.path.join(program_directory, "icon.ico"))
#        master.iconbitmap('icon.ico')
		master.configure(background=_dark_bg)
		master.minsize(860, 640)
		master.rowconfigure(0, minsize=600, weight=1)
		master.rowconfigure(1, minsize=20, weight=0)
		master.columnconfigure(0, minsize=780, weight=1)
		master.columnconfigure(1, minsize=20, weight=0)
		# Style
		MainStyle = Ttk.Style()
        # MainStyle.theme_use('clam')
		MainStyle.theme_create("Dark", parent="clam", settings={
		".": {
			"configure": {"background": _dark_bg,
						  "foreground": _dark_fg_1,
						  "lightcolor": _dark_bg,
						  "darkcolor": _dark_bg,
						  "bordercolor": _dark_border_1},
			"map":       {"background": [("disabled", _dark_bg_1),
										 ("selected", _dark_border_1)],
						  "foreground": [("disabled", _dark_fg),
										 ("selected", _dark_fg),
										 ("active", _dark_fg)]
						  }
			},
		"TNotebook": {
			"configure": {"tabmargins": [1, 5, 1, 0] } },
		"TNotebook.Tab": {
			"configure": {"background": _dark_bg_1,
						  "foreground": _dark_fg_1,
						  "padding": [5, 2]},
			"map":       {"background": [("selected", _dark_bg),
										 ("active", _dark_bg_1)],
						  "foreground": [("selected", _dark_fg)],
						  "expand": [("selected", [1, 1, 1, 0])] } },
		"TButton": {
			"configure": {"background": _dark_bg_1,
						  "foreground": _dark_fg,
						  "anchor": Tk.CENTER,
						  "borderwidth": 1,
						  "heighlightthickness": 20},
			"map":       {"background": [("disabled", _dark_bg_1),
										 ("pressed", "!focus", _dark_bg),
										 ("active", _dark_bg)],
						  "foreground": [("disabled", _dark_fg),
										 ("pressed", _dark_fg_1),
										 ("active", _dark_fg)],
						  "highlightcolor": [("focus", _dark_bg_1),
										 ("!focus", _dark_bg)],
						  "relief": [("pressed", 'groove'),
										 ("!pressed", 'ridge')]
						  }},
		"TLabel": {
			"configure": {"background": _dark_bg,
						  "foreground": _dark_border_1}
						  },
		"TLabelframe": {
			"configure": {"background": _dark_bg,
						  "foreground": _dark_fg,
						  "borderwidth": 1,
						  "relief": 'ridge'}
						  },
		"TLabelframe.Label": {
			"configure": {"background": _dark_bg,
						  "foreground": _dark_fg,
						  "lightcolor": _dark_bg,
						  "darkcolor": _dark_bg}
						  },
		"Horizontal.TProgressbar": {
			"configure": {"background": _dark_border_1,
						  "troughcolor": _dark_bg}
						  },
		"TSizegrip": {
			"configure": {"background": _dark_bg}
						  },
		"TSeparator": {
			"configure": {"background": _dark_bg}},
		"TEntry": {
			"configure": {"background": _dark_bg,
						  "foreground": _dark_fg,
						  "fieldbackground": _dark_bg,
						  "selectbackground": _dark_border_1,
						  "insertcolor": _dark_border_1,
						  "insertwidth": 2}},
		"TCheckbutton": {
			"configure": {"background": _dark_bg_1,
						  "foreground": _dark_border_1,
						  "highlightcolor": _dark_bg,
						  "selectcolor": _dark_bg,
						  "activebackground": _dark_border_1,
						  "activeforeground": _dark_bg},
			"map":       {"background": [("disabled", _dark_bg_1),
										 ("selected", _dark_border_1),
										 ("pressed", "!focus", _dark_bg),
										 ("active", _dark_bg)],
						  "foreground": [("disabled", _dark_fg),
										 ("selected", _dark_bg),
										 ("pressed", _dark_fg_1),
										 ("active", _dark_fg)],
						  "highlightcolor": [("focus", _dark_bg_1),
										 ("!focus", _dark_bg)],
						  "relief": [("active", 'groove'),
										 ("pressed", 'sunken')]
						  }},
		"TCombobox": {
			"configure": {"background": _dark_bg,
						  "foreground": _dark_fg,
						  "fieldbackground": _dark_bg,
						  "selectbackground": _dark_border_1,
						  "arrowcolor": _dark_border_1,
						  "insertcolor": _dark_border_1,
						  "insertwidth": 2},
			"map":       {"background": [("disabled", _dark_bg_1),
										 ("selected", _dark_border_1)],
						  "foreground": [("disabled", _dark_fg),
										 ("selected", _dark_fg),
										 ("active", _dark_bg),
										 ("focus", _dark_fg)],
						  "relief": [('active','groove'),
									 ('pressed','sunken')]
						  }},
		"Treeview": {
			"configure": {"background": _dark_bg,
						  "foreground": _dark_fg,
						  "fieldbackground": _dark_bg,
						  "relief": 'flat'},
			"map":       {"background": [("disabled", _dark_bg_1),
										 ("selected", _dark_border_1)],
						  "foreground": [("disabled", _dark_fg),
										 ("selected", _dark_fg),
										 ("active", _dark_fg),
										 ("focus", 'red')],
						  "relief": [('active','groove'),
									 ('pressed','sunken')]
						  }},
		"Treeview.Item": {
			"configure": {"focuscolor": _dark_border_1}},
		"Treeview.Heading": {
			"configure": {"background": _dark_bg_1,
						  "foreground": _dark_fg,
						  "focusforeground": 'red'}}
																  
																  
																} )
		# Main_Theme=Ttk.Style()
		MainStyle.theme_use('Dark')
		# MainStyle.theme_use('clam')
		self.configure(background=_dark_bg)
		self.create_widgets()
