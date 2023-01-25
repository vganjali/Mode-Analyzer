import sys
from find_peaks import *
if sys.version_info[0] < 3:
	import Tkinter as Tk
	import tkFileDialog as TkFD
else:
	import tkinter as Tk
	import tkinter.filedialog as TkFD
import numpy as np 
#import scipy as sp
from scipy import ndimage
import matplotlib
matplotlib.use('TkAgg')
# matplotlib.use('Agg')
print (f'Python Version: {sys.version_info[0]}.{sys.version_info[1]}.{sys.version_info[2]}')
from gui_mpl import *
#import cv2
from PIL import Image
import os, os.path
from re import compile, split

Dir = []
Image_List = []
Image_original = []
Image_rotated = []
Image_gray = []
Image_Shape= []
pixel_to_um = 0
dx = 1
ydata_fit =[]
number_of_peaks = []

class main(Tk.Tk):
	def __init__(self):
		# threading.Thread.__init__(self)
		self.root = Tk.Tk()
		# self.start()
		# self.run()
		
	def callback(self):
		self.root.quit()

	def run(self):
		self.main_gui = MainWindow(master=self.root)
		self.main_gui.theButtonBrowse.config(command=lambda: self.Browse())
		self.main_gui.theButtonSetCS.config(command=lambda: self.SetCS())
		self.main_gui.theButtonCopy.config(command=lambda: self.Copy_data_points())
		self.main_gui.theButtonCopyWavelet.config(command=lambda: self.Copy_as_wavelet())
		self.main_gui.theButtonScan.config(command=lambda: self.Make_Scan_Plot())
		self.main_gui.theDirList.bind("<<TreeviewSelect>>", self.theDirList_select)
		self.main_gui.thePixel2umInput.bind("<Return>", (lambda event: self.Update_Image(add=0)))
		self.main_gui.theGridSizeInput.bind("<Return>", (lambda event: self.Update_Image(add=0)))
		self.main_gui.theRotationInput.bind("<Return>", (lambda event: self.Update_Image(add=1)))
		self.main_gui.theFPThreshInput.bind("<Return>", (lambda event: self.Update_Image(add=0)))
		self.main_gui.theFPMinDistInput.bind("<Return>", (lambda event: self.Update_Image(add=0)))
		self.main_gui.theFitAmpBoundLInput.bind("<Return>", (lambda event: self.Update_Image(add=0)))
		self.main_gui.theCSWidthInput.bind("<Return>", (lambda event: self.Update_Image(add=0)))
		self.main_gui.theFitAmpBoundUInput.bind("<Return>", (lambda event: self.Update_Image(add=0)))
		self.main_gui.theFitMuBoundLInput.bind("<Return>", (lambda event: self.Update_Image(add=0)))
		self.main_gui.theFitMuBoundUInput.bind("<Return>", (lambda event: self.Update_Image(add=0)))
		self.main_gui.theFitSigmaBoundLInput.bind("<Return>", (lambda event: self.Update_Image(add=0)))
		self.main_gui.theFitSigmaBoundUInput.bind("<Return>", (lambda event: self.Update_Image(add=0)))
		self.main_gui.theValleyOffsetInput.bind("<Return>", (lambda event: self.Update_Image(add=0)))
		self.main_gui.theCSHeightInput.bind("<Return>", (lambda event: self.Update_Image(add=0)))
		self.main_gui.thePlotMode.bind("<<ComboboxSelected>>", (lambda event: self.Update_Image(add=0)))
		self.main_gui.theNormalizeCheck.config(command=lambda: self.Update_Image(add=0))
		self.root.protocol("WM_DELETE_WINDOW", self.callback)
		self.root.mainloop()
	def Browse(self):
		global Dir, Image_List
		Dir = TkFD.askdirectory(initialdir=Dir)
		if (Dir == ''):
			return
		else:
			self.main_gui.theDirList.delete(*self.main_gui.theDirList.get_children())
			Image_List = []
			self.main_gui.theDirList.heading("#1", text=Dir)
			valid_images = [".jpg",".gif",".png",".bmp",".tif",".tiff"]
			self.main_gui.theStatus.config(text="Loading...")
			self.main_gui.update()
			for f in os.listdir(Dir):
				ext = os.path.splitext(f)[1]
				if ext.lower() not in valid_images:
					continue
				#imgs.append(Image.open(os.path.join(Dir,f))
				Image_List.append(f)
			dre = compile(r'(\d+)')
			Image_List.sort(key=lambda l: [int(s) if s.isdigit() else s.lower() for s in split(dre, l)])
			for i,f in enumerate(Image_List):
				self.main_gui.theDirList.insert('', 'end', values=([f]), tags=['even', 'odd'][i%2])
			self.main_gui.theStatus.config(text="Idle")
	def theDirList_select(self, event):
		global Image_original, Image_rotated
		item_text = self.main_gui.theDirList.item(self.main_gui.theDirList.selection(),"value")
		Image_original = Image.open(os.path.join(Dir,item_text[0]))
		#self.main_gui.ax2.set_extent()
		#self.main_gui.ax2.autoscale_view(tight=None, scalex=True, scaley=True)
		#self.main_gui.fig2.show()
		self.Update_Image(add=1)
			
	def Update_Image(self, add, Scan=False):
		global Image_rotated, Image_gray, Image_Shape, pixel_to_um
		pixel_to_um = float(self.main_gui.Pixel2um.get())
		self.main_gui.theStatus.config(text="Updating...")
		self.main_gui.update()
		if (Scan):
			Image_rotated = ndimage.rotate(Image_original, float(self.main_gui.Rotation.get()))
			#Image_rotated = Image_original.rotate(float(self.main_gui.Rotation.get()))
			Image_Shape = Image_rotated.shape
			xlim, ylim = (-0.5,Image_Shape[1]+0.5), (-0.5,Image_Shape[0]+0.5)
			try:
				self.main_gui.ax2.Image.remove()
			except:
				pass
			if(len(Image_Shape) > 2):
				Image_gray = np.asarray(Image.fromarray(Image_rotated[:,:,:min(3,Image_Shape[2])]).convert('L'))
				self.main_gui.ax2.Image = self.main_gui.ax2.imshow(Image_rotated, origin='upper')
			else:
				Image_gray = np.asarray(Image.fromarray(Image_rotated))
				self.main_gui.ax2.Image = self.main_gui.ax2.imshow(Image_rotated, origin='upper', cmap='gray')
			return self.Update_Plot(Scan=True)
		else:
			if (add!=1):
				xlim, ylim = self.main_gui.ax2.get_xlim(), self.main_gui.ax2.get_ylim()
			else:
				Image_rotated = ndimage.rotate(Image_original, float(self.main_gui.Rotation.get()))
				#Image_rotated = Image_original.rotate(float(self.main_gui.Rotation.get()))
				Image_Shape = Image_rotated.shape
				xlim, ylim = (-0.5,Image_Shape[1]+0.5), (-0.5,Image_Shape[0]+0.5)
				try:
					self.main_gui.ax2.Image.remove()
				except:
					pass
				if(len(Image_Shape) > 2):
					Image_gray = np.asarray(Image.fromarray(Image_rotated[:,:,:min(3,Image_Shape[2])]).convert('L'))
					self.main_gui.ax2.Image = self.main_gui.ax2.imshow(Image_rotated, origin='upper')
				else:
					Image_gray = np.asarray(Image.fromarray(Image_rotated))
					self.main_gui.ax2.Image = self.main_gui.ax2.imshow(Image_rotated, origin='upper', cmap='gray')
			#self.main_gui.ax2.cla()
				
			self.main_gui.ax2.cs.set_width(int(float(self.main_gui.CSWidth.get())*pixel_to_um))
			self.main_gui.ax2.cs.set_height(int(float(self.main_gui.CSHeight.get())*pixel_to_um))
			xticks = np.arange(0,int(Image_Shape[1]/pixel_to_um),int(self.main_gui.GridSize.get()))
			yticks = np.arange(0,int(Image_Shape[0]/pixel_to_um),int(self.main_gui.GridSize.get()))
			self.main_gui.ax2.set_xticks(xticks*pixel_to_um)
			self.main_gui.ax2.set_xticklabels(xticks.astype(str))
			self.main_gui.ax2.set_yticks(yticks*pixel_to_um)
			self.main_gui.ax2.set_yticklabels(yticks.astype(str))
			if (add!=1):
				self.main_gui.ax2.set_xlim(xlim)
				self.main_gui.ax2.set_ylim(ylim)
			else:
				self.main_gui.ax2.relim()
			#self.main_gui.ax2.set_xlim(xlim)
			#self.main_gui.ax2.set_ylim(ylim)
			#self.main_gui.ax2.axis('image')
			if (self.main_gui.PlotMode.get() == 'Single Line'):
				self.main_gui.ax2.cs.set_hatch(None)
				self.main_gui.ax2.sl.set_data([\
				self.main_gui.ax2.cs.get_xy()[0], \
				self.main_gui.ax2.cs.get_xy()[0] + \
				self.main_gui.ax2.cs.get_width()], \
				[self.main_gui.ax2.cs.get_xy()[1] + \
				self.main_gui.ax2.cs.get_height() / 2, \
				self.main_gui.ax2.cs.get_xy()[1] + \
				self.main_gui.ax2.cs.get_height() / 2])
			else:
				self.main_gui.ax2.cs.set_hatch('xx')
				self.main_gui.ax2.sl.set_data([],[])
			self.main_gui.canvas2.draw()
			self.Update_Plot()
			self.main_gui.theStatus.config(text="Idle")
			self.main_gui.update()
	
	def Update_Plot(self, Scan=False):
		global pixel_to_um, dx, ydata_fit, number_of_peaks
		pixel_to_um = pixel_to_um
		xlim, ylim = self.main_gui.ax2.get_xlim(), self.main_gui.ax2.get_ylim()
		if (self.main_gui.PlotMode.get() == 'Single Line'):
			Data = Image_gray[int(self.main_gui.ax2.cs.get_y() + self.main_gui.ax2.cs.get_height()/2),
								 range(int(self.main_gui.ax2.cs.get_x()),
									   int(self.main_gui.ax2.cs.get_x() + self.main_gui.ax2.cs.get_width()))].astype(float)
		else:
			Data = np.sum(Image_gray[np.ix_(range(int(self.main_gui.ax2.cs.get_y()),
										   int(self.main_gui.ax2.cs.get_y() + self.main_gui.ax2.cs.get_height())),
								 range(int(self.main_gui.ax2.cs.get_x()),
									   int(self.main_gui.ax2.cs.get_x() + self.main_gui.ax2.cs.get_width())))], axis=0, dtype=float)
		if (self.main_gui.Normalize.get() == 1):
			Data = Data - np.amin(Data)
			Data = Data / np.amax(Data)
			self.main_gui.ax1.set_ylabel('Normalized Intensity')
		else:
			self.main_gui.ax1.set_ylabel('Intensity [a.u.]')
		self.main_gui.ax1.cla()
		self.main_gui.ax1.Line0, = self.main_gui.ax1.plot([], 'y-')
		self.main_gui.ax1.Line0.set_data(np.linspace(0,Data.shape[0]/pixel_to_um,Data.shape[0]), Data)
		self.main_gui.ax1.axis('auto')
		self.main_gui.ax1.relim()
		self.main_gui.ax1.autoscale()
		self.main_gui.canvas1.draw()
		if (not Scan):
			self.main_gui.theStatus.config(text="Analyzing peaks...")
			self.main_gui.update()
			Idx, Idx_xdata, FWHM, FWHM_STD, Peak_to_Valley, Peak_to_Valley_STD, Delta_X, Delta_X_STD, ydata_fit = find_peaks(
				Data, float(self.main_gui.CSWidth.get()), float(self.main_gui.ValleyOffset.get()), \
				FindPeak_thresh=float(self.main_gui.FPthresh.get()), FindPeak_mindist=float(self.main_gui.FPmindist.get()), \
				CurveFit_a_bounds=(float(self.main_gui.FitAmpBoundL.get()), float(self.main_gui.FitAmpBoundU.get())), \
				CurveFit_mu_bounds=(float(self.main_gui.FitMuBoundL.get()), float(self.main_gui.FitMuBoundU.get())), \
				CurveFit_sigma_bounds=(float(self.main_gui.FitSigmaBoundL.get()), float(self.main_gui.FitSigmaBoundU.get())))
			self.main_gui.theResultTable.item(self.main_gui.theResultTable.get_children()[0], values=('Number of Spots', len(FWHM), '0'))
			self.main_gui.theResultTable.item(self.main_gui.theResultTable.get_children()[1], values=('FWHM', str("%.3f" % np.mean(FWHM)), str("%.3f" % np.mean(FWHM_STD))))
			self.main_gui.theResultTable.item(self.main_gui.theResultTable.get_children()[2], values=('Peak to Valley', str("%.3f" % np.mean(Peak_to_Valley)), str("%.3f" % np.mean(Peak_to_Valley_STD))))
			self.main_gui.theResultTable.item(self.main_gui.theResultTable.get_children()[3], values=(u'\u0394X', str("%.3f" % np.mean(Delta_X)), str("%.3f" % np.mean(Delta_X_STD))))
			#self.main_gui.theResultTable.item(self.main_gui.theResultTable.get_children()[4], values=('SNR', str("%.3f" % (np.mean(Data[Idx])/(np.mean(Data[Idx]) - np.mean(Peak_to_Valley)))), '0'))
			dx = np.mean(Delta_X)*pixel_to_um
			number_of_peaks = len(FWHM)
		return Data

	def Copy_data_points(self):
		self.main_gui.theStatus.config(text=" Collecting data points...")
		self.main_gui.update()
		self.main_gui.clipboard_clear()
		Xdata = self.main_gui.ax1.Line0.get_xdata()
		Ydata = self.main_gui.ax1.Line0.get_ydata()
		X = 'X_data, Y_data\n'
		self.main_gui.theProgressbar.grid()
		self.main_gui.theProgressbar['maximum'] = len(Xdata)/100
		for n in range(len(Xdata)):
			X += str(Xdata[n]) + ', ' + str(Ydata[n]) + '\n'
			if (n%100)==0:
				self.main_gui.theProgressbar['value'] = n/100
				self.main_gui.theProgressbar.update()
		self.main_gui.clipboard_append(X)
		self.main_gui.theProgressbar.grid_remove()
		self.main_gui.theStatus.config(text="Idle")
		self.main_gui.update()
		
	def Copy_as_wavelet(self):
		global dx, ydata_fit, number_of_peaks
		self.main_gui.theStatus.config(text=" Collecting data points...")
		self.main_gui.update()
		self.main_gui.clipboard_clear()
		X = str(number_of_peaks)+': '+str(dx)+': '
		self.main_gui.theProgressbar.grid()
		self.main_gui.theProgressbar['maximum'] = len(ydata_fit)/100
		for n,y in enumerate(ydata_fit):
			X += str(y)+', '
			if (n%100)==0:
				self.main_gui.theProgressbar['value'] = n/100
				self.main_gui.theProgressbar.update()
		X = X[:-2]
		self.main_gui.clipboard_append(X)
		self.main_gui.theProgressbar.grid_remove()
		self.main_gui.theStatus.config(text="Idle")
		self.main_gui.update()

	def CSonclick(self,event):
		global pixel_to_um
		if (event.button == 1):
			ix, iy = event.xdata, event.ydata
			self.main_gui.ax2.cs.set_xy((ix, iy - float(self.main_gui.CSHeight.get()) * pixel_to_um))
			self.Update_Image(add=0)
			self.main_gui.theStatus.config(text="Left click to set the CS origin / Right click to exit")
		else:
			self.main_gui.canvas2.mpl_disconnect(self.cid2)
			self.main_gui.theStatus.config(text="Idle")
		
	def SetCS(self):
		self.main_gui.theStatus.config(text="Left click to set the CS origin / Right click to exit")
		self.cid2 = self.main_gui.canvas2.mpl_connect('button_press_event', self.CSonclick)

	def Make_Scan_Plot(self):
		global Image_original, Image_rotated, pixel_to_um
		Xdata = self.main_gui.ax1.Line0.get_xdata()
		Ydata = self.main_gui.ax1.Line0.get_ydata()
		Scan_Array = np.ndarray((len(Ydata),len(self.main_gui.theDirList.get_children())))
		i = 0
		self.main_gui.clipboard_clear()
		self.main_gui.theProgressbar.grid()
		self.main_gui.theProgressbar['maximum'] = len(self.main_gui.theDirList.get_children())
		for item in self.main_gui.theDirList.get_children():
			item_text = self.main_gui.theDirList.item(item,"value")
			Image_original = Image.open(os.path.join(Dir,item_text[0]))
			#self.main_gui.ax2.set_extent()
			#self.main_gui.ax2.autoscale_view(tight=None, scalex=True, scaley=True)
			#self.main_gui.fig2.show()
			Ydata = self.Update_Image(add=1, Scan=True)
			Scan_Array[:,i] = Ydata
			X = ''
			for n in range(len(Ydata)):
				X += str(Ydata[n]) + ','
			X = X[0:-1:1]
			X += '\n'
			self.main_gui.clipboard_append(X)
			self.main_gui.theProgressbar['value'] = i
			self.main_gui.theProgressbar.update()
			i += 1
		self.main_gui.ax1.cla()
		self.main_gui.ax1.imshow(Scan_Array, extent=[float(self.main_gui.ScanFrom.get()), float(self.main_gui.ScanTo.get()), \
					0, len(Ydata)/pixel_to_um])
		self.main_gui.ax1.axis('tight')
		self.main_gui.canvas1.draw()
		self.main_gui.theProgressbar.grid_remove()
		self.main_gui.theStatus.config(text="Idle")
		self.main_gui.update()
		
# def on_closing():
# #    threading.current_thread().cancel()
# 	try:
# #        app.root.quit()
# 		if app.is_alive():
# 			app.root.quit()
# 			sys.exit()
# 		else:
# 			sys.exit()
# 	except:
# 		return
