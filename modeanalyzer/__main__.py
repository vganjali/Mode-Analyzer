import sys, os
modpath = os.path.split(__file__)[0]
sys.path.append(modpath)
# os.chdir('./modeanalyzer')
# print(os.getcwd())
from .modeanalyzer import *

app = main()
app.run()
# Run = RunSimulation()
# root = Tk.Tk()
# main_gui = MainWindow(master=root)
# root.read = read_data(f)
# root.mainloop()