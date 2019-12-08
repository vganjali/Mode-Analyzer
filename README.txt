Installing prerequisites (x64)
========================================================================================================================================
1- Run Python-3.6.4-amd64.exe and install it (install using custom and check where to install i.e. C:\Program Files\Python36\python.exe)
2- When Python installed on your system, open a powershell as administrator
>> in the prerequisites folder
3- Run these commands in powershell (depending where you have installed python):
	& 'C:\Program Files\Python36\python.exe' -m pip install numpy-1.13.3+mkl-cp36-cp36m-win_amd64.whl scipy-1.0.0-cp36-cp36m-win_amd64.whl matplotlib-2.1.1-cp36-cp36m-win_amd64.whl Pillow-5.0.0-cp36-cp36m-win_amd64.whl
4- cd to PeakUtils-1.1.0 folder and run:
	& 'C:\Program Files\Python36\python.exe' setup.py install
5- Run Main.py