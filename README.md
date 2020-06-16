# Compress And Archive

'compressandarchive' is a program that takes a path to a file or folder as an argument and compresses it as a zip file. The path to the archive is hard wired into the program. Nothing special here. But it also generates a log file in case of a folder compression that contains, apart from listing all the compressed files for a quick search, a table (with file extensions, the number of files, and compression factors), the total number of files zipped, total compressed and uncompressed data size, and overall compression factor as well as the zipped data as the percentage of the unzipped state.

An example of the log file contents:

	2020-06-15 01:21:43

	Compressed folder: an archive name

	File                 #               Zip factor (avg.)   
	py                   51              1.97                
	other                3               19.93               
	txt                  2               3.16                
	pyc                  2               2.02                
	iml                  1               1.44                
	xml                  4               2.74                

	Total number of files: 63

	Compression: 1.2 MB --> 314.5 kB (factor: 3.83, percent: 26.14)

	Files:
	...

The program can easily be implemented as a folder action in Automator on an Apple OS X computer.