"""
Some User Defined Functions
"""
import os, shutil
import tkinter as tk

def clearFolder(myFolder):
    """
    Import: os
    
    Deletes all files in myFolder
    """
    fp = os.path.abspath(myFolder)
    for file in [f for f in os.scandir(fp) if f.is_file()]:
        os.remove(file.path)

    print("All Files Deleted In Folder:")
    print(fp)

def loadFilesFromFolder(
    sourceFolder, destnFolder):
    """
    Import: os, shutil
    
    Copies all files from sourceFolder to destnFolder.

     os.path.abspath(myPath) returns the absolute path
     even if myPath is already absolute. No need to first
     check by os.path.isabs(myPath)
    """
    sp = os.path.abspath(sourceFolder)
    dp = os.path.abspath(destnFolder)

    shutil.copytree(sp, dp, dirs_exist_ok=True)
    print("All Files In Source Folder Copied To:")
    print(dp)

def loadSelectedFiles(destnFolder, fileExtn=""):
    """
    Import: tkinter as tk, os, shutil
    
    Selects files via File Dialog Box and copies to destination
    folder.

    For filter effect, desired file extn, if any, can be passed as
    a string

    For hiding tkinter window:  root.withdraw()
    For showing tkinter window again:  root.deiconify()
    """
    dp = os.path.abspath(destnFolder)
    
    # Close tkinter window. This statement is effective
    # only if placed before the one involving tk.filedialog
    tk.Tk().withdraw()
    
    if len(fileExtn) > 0:
        files = tk.filedialog.askopenfilenames(
            initialdir="/", title="Select Files",
            filetypes=[(fileExtn, fileExtn)])
    else:       
        files = tk.filedialog.askopenfilenames(
            initialdir="/", title="Select Files")

    if not os.path.isdir(dp):
        print("Destination Folder Not Found. Created Afresh:")
        os.makedirs(dp)

    for f in files:
        shutil.copy(f, dp)

    print("Selected Files Copied To:")
    print(dp)

def loadFilesFromSelectedFolder(destnFolder):
    """
    Import: tkinter as tk, shutil, os
    
    On selecting a folder via File Dialog Box, copies all
    its files to destnFolder.

    For hiding tkinter window:  root.withdraw()
    For showing tkinter window again:  root.deiconify()
    """
    dp = os.path.abspath(destnFolder)
    
    # Hide tkinter window
    tk.Tk().withdraw()
     
    sourceFolderPath = tk.filedialog.askdirectory(
        initialdir="/", title="Select Folder")

    shutil.copytree(sourceFolderPath,
        dp, dirs_exist_ok=True)

    print("All Files In Selected Folder Copied To:")
    print(dp)

def listFiles_by_scandir(
            baseFolder=".", fileExtn=""):
    """
    Import: os
    
    Returns a list of files in given folder, matching the given
    fileExtn. It consists of two sub-lists. First sub-list has file
    names, while the second one has file paths.

    Default value of "" for fileExtn gets all files. Default value of "."
    for baseFolderPath gets the files in current working directory.
    """    
    bp = os.path.abspath(baseFolder)
        
    if fileExtn=="":
        fn = [de.name for de in
            os.scandir(bp) if de.is_file()]

        fp = [de.path for de in
            os.scandir(bp) if de.is_file()]
    else:
        fn = [de.name for de in
            os.scandir(bp)
            if de.is_file() and de.name.endswith(fileExtn)]

        fp = [de.path for de in
            os.scandir(bp)
            if de.is_file() and de.name.endswith(fileExtn)]

    return[fn, fp]
