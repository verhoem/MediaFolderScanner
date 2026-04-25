# This code is generated using PyUIbuilder: https://pyuibuilder.com

import os
import pathlib
import tkinter as tk
from os.path import getsize
from tkinter import filedialog
from tkinter import messagebox
from operator import itemgetter
# from Source_folder import Source_folder
# from Dest_folder import Dest_folder
import datetime
import hashlib
import sys
import threading


def getTimeStampNow():
    __current_timestamp = datetime.now()
    formatted_timestamp = __current_timestamp.strftime("%Y%m%d%H%M%S")
    return formatted_timestamp


def buttonFolderAScan():
    global gl_folder_a_consistent
    global gl_list_folder_a
    gl_list_folder_a = []
    gl_folder_a_consistent = False
    buttonCheckConsistencyFolderA.config(bg="#E4E2E2", fg="#000")
    textFolderA.delete(1.0, "end")
    __folderA = entrySrcFolderA.get()
    print(f"Scanning Folder {__folderA}")
    __textBox = f"Scanning Folder  {__folderA}\n"
    textFolderA.insert("end", __textBox)
    __nrFilesInFolder = 0
    __nrSubdirsInFolder = 0
    __ScannedFiles = []
    __ScannedFile = []
    for root, directories, files in os.walk(__folderA):
        for file in files:
            fileName, fileExtension = os.path.splitext(file)
            __nrFilesInFolder += 1
            # print(f"{__nrFilesInFolder}:{directories}:{file}")
            # print(f"filename:{fileName} Extension:{fileExtension}")
            __fullPath = os.path.join(root, file)
            #if isAllowedFileType(fileExtension):
            #     __filesToAnalyse.append(__fullPath)\
            __size = getsize(os.path.join(__fullPath))
            #print(f"folderA:{__folderA}")
            __relativePath = os.path.relpath(__fullPath, __folderA)
            if DEBUG:
                print(f"{__nrFilesInFolder}:{__relativePath}:{__size}")
            __ScannedFile = [__relativePath, __size, "00000000000000000000000000000000"]
            __ScannedFiles.append(__ScannedFile)
            #print(f"{__nrFilesInFolder}:{__fullPath}:{__size}")
        for folder in directories:
            __nrSubdirsInFolder += 1
            # print(f"{folder}")
    print(f"NR files found: {__nrFilesInFolder}" )
    print(f"NR subdirs found: {__nrSubdirsInFolder}" )
    print(f"NR files in ScannedFiles: {len(__ScannedFiles)}")
    __SortedBySize = sorted(__ScannedFiles, key=itemgetter(1))
    # To find duplicate files first find files same sizes before hashing for performance
    __index = 0
    __listSizes = []
    while __index < len(__SortedBySize):
        # print(f"{__index + 1}:{__SortedBySize[__index][0]}:{__SortedBySize[__index][1]}:{__SortedBySize[__index][2]}")
        __listSizes.append(__SortedBySize[__index][1])
        __index += 1
    textFolderA.insert("end", f"NR files found: {__nrFilesInFolder} \n")
    textFolderA.insert("end", f"NR subdirs found: {__nrSubdirsInFolder} \n")
    if len(__listSizes) > 0:
        if DEBUG:
            print(f"DEBUG:__listSizes\nDEBUG:{__listSizes}")
    __dupSizes = []
    __uniSizes = []
    for ele in __listSizes:
        if ele not in __uniSizes:
            __uniSizes.append(ele)
        elif ele not in __dupSizes:
            __dupSizes.append(ele)
    if len(__dupSizes) > 0:
        if DEBUG:
            print(f"DEBUG:__dupSizes\n{__dupSizes}")
    textFolderA.insert("end", f"NR duplicate sizes found: {len(__dupSizes)} \n")
    textFolderA.insert("end", f"Expecting no duplicate files to be found\n")
    for size in __dupSizes:
        __indexSorted = 0
        while __indexSorted < len(__SortedBySize):
            if __SortedBySize[__indexSorted][1] == size:
                if DEBUG:
                    print(f"{__indexSorted}:{size}:{__SortedBySize[__indexSorted][0]}")
                __filePath = os.path.join(__folderA, __SortedBySize[__indexSorted][0])
                with open(__filePath, "rb") as f:
                    bytes = f.read(100000)  # read file as bytes
                    __hashFile = hashlib.md5(bytes).hexdigest()
                if DEBUG:
                    print(f"{__filePath}:{__hashFile}")
                # set hash of file in __SortedBySize if size is equal
                __SortedBySize[__indexSorted][2] = __hashFile
            __indexSorted += 1
    __listHashes = []
    __index = 0
    while __index < len(__SortedBySize):
        # if __index == 0:
        # print(f"index:{__index}:{__SortedBySize[__index][2]}:{type(__SortedBySize[__index][2])}")
        if __SortedBySize[__index][2] != "00000000000000000000000000000000":
            if DEBUG:
                print(f"DEBUG:{__index}:{__SortedBySize[__index][0]}:{__SortedBySize[__index][1]}:{__SortedBySize[__index][2]}:{type(__SortedBySize[__index][2])}")
            __listHashes.append(__SortedBySize[__index][2])
        __index += 1
    if DEBUG:
        print(f"DEBUG:__listHashes:{__listHashes}")
    __uniHashes = []
    __dupHashes = []
    for ele in __listHashes:
        if ele not in __uniHashes:
            __uniHashes.append(ele)
        elif ele not in __dupHashes:
            __dupHashes.append(ele)
    if len(__dupHashes) > 0:
        if DEBUG:
            print(f"duplicate hashes found:\n{__dupHashes}")
        pathDH = os.path.join(os.getcwd(), "Scan_Media_Folder_duplicate_hashes.txt")
        fDH = open(pathDH, "w")
        dtNow = datetime.datetime.now()
        fDH.write(f"Folder scanned:{__folderA}\n")
        fDH.write(f"Scan date:{dtNow}\n")
        fDH.write(f"Duplicate hashes found:{len(__dupHashes)}\n")
        for __hash in __dupHashes:
            __index = 0
            while __index < len(__SortedBySize):
                if __SortedBySize[__index][2] == __hash:
                    __filePathTmp = os.path.join(__folderA, __SortedBySize[__index][0])
                    print(f"Duplicate:{__filePathTmp}:{__hash}")
                    fDH.write(f"{__filePathTmp}:{__hash}\n")
                __index += 1
        textFolderA.insert("end", f"Duplicate hashes found in Folder A Exiting!!\n")
        fDH.close()
        gl_folder_a_consistent = True
        return
    else:
        print(f"No duplicate hashes found in Folder A {__folderA}")
        textFolderA.insert("end", f"No duplicate hashes found in Folder A {__folderA}\n")
        gl_folder_a_consistent = True
        gl_list_folder_a = __SortedBySize
    textFolderA.insert("end", f"Checking files correct Year Month location\n")
    __index = 0
    __incorrectYearLocations = []
    __incorrectMonthLocations = []
    __incorrectNamingLocations = []
    while __index < len(__SortedBySize):
        if __SortedBySize[__index][0][:3] != "PHM":
            __locYear = __SortedBySize[__index][0][:4]
            __locMonth = __SortedBySize[__index][0][5:7]
            __locFileName = __SortedBySize[__index][0][8:]
            filePath = os.path.join(__folderA, __SortedBySize[__index][0])
            t1 = os.path.getmtime(filePath)
            t = datetime.datetime.fromtimestamp(t1)
            __fromOsYear = t.strftime("%Y")
            __fromOsMonth = t.strftime("%m")
            __fromOsDay = t.strftime("%d")
            # self.day = t.strftime("%d")
            # self.time = t.strftime("%H%M%S")
            if __locYear != __fromOsYear:
                if DEBUG:
                    print(f"DEBUG:{__index}:Incorrect Year location !!")
                    print(f"DEBUG:index:{__index}:{__SortedBySize[__index][0]}:From OS:{__fromOsYear}:{__fromOsMonth}")
                # print(f"index:{__index}:{__SortedBySize[__index][0]}")
                # print(f"index:{__locYear}:{__locMonth}:{__locFileName}")
                # print(f"From OS:{__fromOsYear}:{__fromOsMonth}")
                __incorrectYearLocation = []
                __incorrectYearLocation.append(__SortedBySize[__index][0])
                __incorrectYearLocation.append(__fromOsYear)
                __incorrectYearLocation.append(__fromOsMonth)
                __incorrectYearLocations.append(__incorrectYearLocation)
            elif __locMonth != __fromOsMonth:
                if DEBUG:
                    print(f"DEBUG:{__index}:Incorrect Month location !!")
                    print(f"DEBUG:index:{__index}:{__SortedBySize[__index][0]}:From OS:{__fromOsYear}:{__fromOsMonth}")
                # print(f"index:{__locYear}:{__locMonth}:{__locFileName}")
                # print(f"From OS:{__fromOsYear}:{__fromOsMonth}")
                __incorrectMonthLocation = []
                __incorrectMonthLocation.append(__SortedBySize[__index][0])
                __incorrectMonthLocation.append(__fromOsYear)
                __incorrectMonthLocation.append(__fromOsMonth)
                __incorrectMonthLocations.append(__incorrectMonthLocation)
                #__strYearMonth = __fromOsYear + __fromOsMonth
                # print(f"__strYearMonth:{__strYearMonth}")
                #print(f"")
            __strYearMonth = __fromOsYear + __fromOsMonth
            __strYearMonthDay = __fromOsYear  + __fromOsMonth + __fromOsDay
            __locYearMonth = __locYear + __locMonth
            if __strYearMonth != __locYearMonth:
                if DEBUG:
                    print(f"DEBUG:{__index}:__strYearMonth:{__strYearMonth} != __locYearMonth :{__locYearMonth} file: {filePath}")
            if not __locFileName.startswith(__strYearMonthDay):
                if DEBUG:
                    print(f"DEBUG:{__index}:__strYearMonthDay:{__strYearMonthDay}:Incorrect naming file !!")
                    print(f"DEBUG:index:{__index}:{__SortedBySize[__index][0]}:From OS:{__strYearMonth}")
                __incorrectNamingLocation = []
                __incorrectNamingLocation.append(__SortedBySize[__index][0])
                __strYearMonthDay = __strYearMonth + __fromOsDay
                __incorrectNamingLocation.append(__strYearMonthDay)
                __incorrectNamingLocations.append(__incorrectNamingLocation)
        __index += 1
    # Create file Scan_Media_Folder_Wrong_Location_Years.tx
    PathWLY = os.path.join(os.getcwd(), "Scan_Media_Folder_Wrong_Location_Years.txt")
    fWLY = open(PathWLY, "w")
    dtNow = datetime.datetime.now()
    # fWLY.write(f"Scan date:{getTimeStampNow()}\n")
    fWLY.write(f"Folder scanned:{__folderA}\n")
    fWLY.write(f"Scan date:{dtNow}\n")
    fWLY.write(f"Wrong year locations:{len(__incorrectYearLocations)}\n\n")
    if len(__incorrectYearLocations) > 0:
        textFolderA.insert("end", f"Incorrect Year locations found:{len(__incorrectYearLocations)}\n")
        __index = 0
        while __index < len(__incorrectYearLocations):
            if DEBUG:
                print(f"DEBUG:{__index}:{__incorrectYearLocations[__index]}")
            fWLY.write(f"{__index}:{__incorrectYearLocations[__index]}\n")
            __index += 1
    else:
        print(f"No Incorrect Year location found")
        textFolderA.insert("end", f"No Incorrect Year locations found\n")
    fWLY.close()
    # Create file Scan_Media_Folder_Wrong_Location_Months.txt
    PathWLM = os.path.join(os.getcwd(), "Scan_Media_Folder_Wrong_Location_Months.txt")
    fWLM = open(PathWLM, "w")
    dtNow=datetime.datetime.now()
    fWLM.write(f"Folder scanned:{__folderA}\n")
    fWLM.write(f"Scan date:{dtNow}\n")
    fWLM.write(f"Wrong month locations:{len(__incorrectMonthLocations)}\n")
    if len(__incorrectMonthLocations) > 0:
        textFolderA.insert("end", f"Incorrect Month locations found:{len(__incorrectMonthLocations)}\n")
        __index = 0
        while __index < len(__incorrectMonthLocations):
            if DEBUG:
                print(f"DEBUG:{__index}:{__incorrectMonthLocations[__index]}")
            fWLM.write(f"{__index}:{__incorrectMonthLocations[__index]}\n")
            __index += 1
    else:
        print(f"No Incorrect Month location found")
        textFolderA.insert("end", f"No Incorrect Month locations found\n")
    fWLM.close()
    __lstIncorrectLocations = getListIncorrectLocations(__folderA, __SortedBySize)
    if len(__lstIncorrectLocations) == 0:
        print("No Incorrect Locations [YYYY/MM/File] found")
        textFolderA.insert("end", f"No Incorrect Locations [YYYY/MM/File] found\n")
    if len(__lstIncorrectLocations) > 0:
        if messagebox.askyesno("InfoMV", f"{len(__lstIncorrectLocations)} Incorrect locations [YYYY/MM/File] found , correct ?"):
            __nrCorrectedLocations = 0
            print("User requested to correct locations")
            __index = 0
            while __index < len(__lstIncorrectLocations):
                print(f"{__index}:{__lstIncorrectLocations[__index][0]}:{__lstIncorrectLocations[__index][1]}:{__lstIncorrectLocations[__index][2]}")
                __filePathSrc = os.path.join(__folderA, __lstIncorrectLocations[__index][0])
                __fileNameSrc = os.path.basename(__filePathSrc)
                __filePathDst = os.path.join(__folderA, __lstIncorrectLocations[__index][1], __lstIncorrectLocations[__index][2], __fileNameSrc)
                __answer = messagebox.askyesnocancel("InfoMV",
                                                     f"Move:{__filePathSrc} \nTo: {__filePathDst} ?")
                if __answer == None:
                    print("User aborted to correct locations")
                    textFolderA.insert("end", f"Correcting locations ({__nrCorrectedLocations}/{len(__lstIncorrectLocations)}) aborted by user\n")
                    textFolderA.insert("end", f"Thanks for flying scan media folder\n")
                    return
                else:
                    if __answer:
                        __dstDir = os.path.join(__folderA, __lstIncorrectLocations[__index][1], __lstIncorrectLocations[__index][2])
                        pathlib.Path(__dstDir).mkdir(parents=True, exist_ok=True)
                        if DEBUG:
                            print(f"DEBUG: os.rename({__filePathSrc}, {__filePathDst})")
                        os.rename(__filePathSrc, __filePathDst)
                        __nrCorrectedLocations += 1
                __index += 1
            print("Corrected incorrect locations, please re-run scan")
            return

    __index = 0
    if len(__lstIncorrectLocations) > 0:
        print(f"Incorrect locations found:{len(__lstIncorrectLocations)}")
        while __index < len(__lstIncorrectLocations):
            if DEBUG:
                print(f"DEBUG:__lstIncorrectLocations:{__index}:{__lstIncorrectLocations[__index][0]}:{__lstIncorrectLocations[__index][1]}:{__lstIncorrectLocations[__index][2]}")
            __index += 1
    # Create file Scan_Media_Folder_Wrong_Names.txt
    pathWN = os.path.join(os.getcwd(), "Scan_Media_Folder_Wrong_Names.txt")
    fWN = open(pathWN, "w")
    dtNow = datetime.datetime.now()
    fWN.write(f"Folder scanned:{__folderA}\n")
    fWN.write(f"Scan date:{dtNow}\n")
    fWN.write(f"Wrong naming not starting YYYYMM:{len(__incorrectNamingLocations)}\n")
    if len(__incorrectNamingLocations) > 0:
        textFolderA.insert("end", f"Incorrect Namings found:{len(__incorrectNamingLocations)}\n")
        print(f"Incorrect namings found:{len(__incorrectNamingLocations)}")
        __index = 0
        while __index < len(__incorrectNamingLocations):
            if DEBUG:
                print(f"DEBUG:__incorrectNamingLocations[{__index}]:{__incorrectNamingLocations[__index]}")
            fWN.write(f"{__index}:{__incorrectNamingLocations[__index]}\n")
            __index += 1
    else:
        print(f"No Incorrect Namings [yyyymmdd_filename] found")
        textFolderA.insert("end", f"No Incorrect Namings [yyyymmdd_filename] found\n")
    fWN.close()
    if len(__incorrectNamingLocations) > 0:
        if messagebox.askyesno("InfoMV", f"{len(__incorrectNamingLocations)} Incorrect namings [yyyymmdd_filename] found , correct ?"):
            print("User requested to correct namings")
            __index = 0
            while __index < len(__incorrectNamingLocations):
                __filePath = os.path.join(__folderA, __incorrectNamingLocations[__index][0])
                __fileDir, __fileName = os.path.split(__filePath)
                # Fixing bug , renaming to yearmonth_ , should have been yearmonthday_
                __checkBugNaming = __incorrectNamingLocations[__index][1][:6] + "_"
                if __fileName.startswith(__checkBugNaming):
                    print(f"Found old bug in naming !!")
                    __fileNameNew = __incorrectNamingLocations[__index][1] + "_" + __fileName[7:]
                else:
                    __fileNameNew = __incorrectNamingLocations[__index][1] + "_" + __fileName
                __filePathNew = os.path.join(__fileDir, __fileNameNew)
                if DEBUG:
                    print(f"DEBUG:Renaming index[{__index}]:{__incorrectNamingLocations[__index][0]} to")
                    print(f"DEBUG:Renaming filePath[{__index}]:{__filePath} to")
                    print(f"DEBUG:Renaming fileDir[{__index}]:{__fileDir}")
                    print(f"DEBUG:Renaming fileName[{__index}]:{__fileName} ")
                    print(f"DEBUG:Renaming __checkBugNaming[{__index}]:{__checkBugNaming} ")
                    print(f"DEBUG:Renaming fileNameNew[{__index}]:{__fileNameNew} ")
                    print(f"DEBUG:Renaming filePathNew[{__index}]:{__filePathNew} ")
                __question = f"Rename index[{__index + 1}/{len(__incorrectNamingLocations)}]:{__filePath} to {__filePathNew} ? "
                print(__question)
                __answer = messagebox.askyesnocancel("InfoMV",__question)
                if __answer == None:
                    print("User aborted to correct namings")
                    textFolderA.insert("end", f"Aborted by user\n")
                    textFolderA.insert("end", f"Thanks for flying scan media folder\n")
                    return
                else:
                    if __answer:
                        os.rename(__filePath, __filePathNew)
                    __index += 1
        else:
            print("User aborted to correct namings")
            print("Thanks for flying scan media folder")
            textFolderA.insert("end", f"Aborted by user\n")
            textFolderA.insert("end", f"Thanks for flying scan media folder\n")
    return

def buttonDirDialogFolderA():
    __folder_selected = filedialog.askdirectory()
    entrySrcFolderA.delete(0, tk.END)
    entrySrcFolderA.insert(0, __folder_selected)
    writeLastestCompFolderA(__folder_selected)
    print(f"Scan Folder set to: \n{__folder_selected} \n")
    buttonCheckConsistencyFolderA.config(bg="#E4E2E2", fg="#000")
    textFolderA.delete(1.0, "end")
    textFolderA.insert("end", f"Scan Folder set to: \n{__folder_selected} \n")

def getLastestCompFolderA():
    __latestCompFolderAFile = os.path.join(os.getcwd(), "latest_comp_folder_a.txt")
    __latestCompFolderA = None
    if os.path.exists(__latestCompFolderAFile):
        __latestCompFolderAFp = open(__latestCompFolderAFile, 'r')
        __latestCompFolderA = __latestCompFolderAFp.readline()
        if len(__latestCompFolderA) < 4:
            __latestCompFolderA = None
    return __latestCompFolderA

def writeLastestCompFolderA(CompFolderA):
    __latestCompFolderAFile = os.path.join(os.getcwd(), "latest_comp_folder_a.txt")
    __latestCompFolderA = None
    print(f"writeLastestCompFolderA({CompFolderA})")
    print(f"writeLastestCompFolderA:__latestCompFolderAFile:{__latestCompFolderAFile})")
    if os.path.exists(__latestCompFolderAFile):
        __latestCompFolderAFp = open(__latestCompFolderAFile, 'w')
        __latestCompFolderAFp.write(CompFolderA)
        __latestCompFolderAFp.close()
        print(f"written {CompFolderA} to {__latestCompFolderAFile}")
    return __latestCompFolderA

def getVerion():
    __versionFile = os.path.join(os.getcwd(), "version_media_scan_folder.txt")
    __versionFp = open(__versionFile, 'r')
    __version = __versionFp.readline()
    return __version

def getListIncorrectLocations(rootFolder, sortedList):
    __lstIncorrectLocations = []
    __rootFolder = rootFolder
    __sortedList = sortedList
    __lstIncorrectLocation = []
    if DEBUG:
        print(f"DEBUG:getListIncorrectLocations:rootFolder:{__rootFolder}")
        print(f"DEBUG:getListIncorrectLocations:nr items sortedlist:{len(__sortedList)}")
    __index = 0
    while __index < len(__sortedList):
        if __sortedList[__index][0][:3] != "PHM":
            __locYear = __sortedList[__index][0][:4]
            __locMonth = __sortedList[__index][0][5:7]
            __locFileName = __sortedList[__index][0][8:]
            filePath = os.path.join(__rootFolder, __sortedList[__index][0])
            t1 = os.path.getmtime(filePath)
            t = datetime.datetime.fromtimestamp(t1)
            __fromOsYear = t.strftime("%Y")
            __fromOsMonth = t.strftime("%m")
            __fromOsDay = t.strftime("%d")
            if DEBUG:
                print(f"DEBUG:getListIncorrectLocations:File[{__index}]:{__sortedList[__index][0]}\nDEBUG:FromOsYear:{__fromOsYear}, FromOsMonth:{__fromOsMonth}, FromOSDay:{__fromOsDay}")
            if __fromOsYear + __fromOsMonth == __locYear + __locMonth:
                if DEBUG:
                    print("DEBUG:getListIncorrectLocations:OK")
            else:
                __lstIncorrectLocation = [__sortedList[__index][0], __fromOsYear, __fromOsMonth, __fromOsDay]
                __lstIncorrectLocations.append(__lstIncorrectLocation)
                if DEBUG:
                    print("DEBUG:getListIncorrectLocations:NOK")
        __index += 1
    if DEBUG:
        print(f"DEBUG:getListIncorrectLocations exited with NR items:{len(__lstIncorrectLocations)}")
    return __lstIncorrectLocations



BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEBUG = True
gl_folder_a_consistent = False
gl_folder_b_consistent = False
gl_list_folder_a = []
gl_list_folder_b = []
CheckAFolder = False
CheckBFolder = False
Sorted_Source_list = []
Sorted_Dest_list = []
main = tk.Tk()
__version = getVerion()
main.title(f"Media Folder Scan {__version}")
main.config(bg="#E4E2E2")
main.geometry("900x694")

entrySrcFolderA = tk.Entry(master=main)
entrySrcFolderA.config(bg="#fff", fg="#000")
entrySrcFolderA.place(x=13, y=80, width=275, height=21)

buttonGetFolderA = tk.Button(master=main, text="Media Folder to Scan", command=buttonDirDialogFolderA)
buttonGetFolderA.config(bg="#E4E2E2", fg="#000")
buttonGetFolderA.place(x=170, y=168, height=40)

textFolderA = tk.Text(master=main)
textFolderA.config(bg="#fff", fg="#000")
textFolderA.place(x=13, y=267, width=800, height=340)

buttonCheckConsistencyFolderA = tk.Button(master=main, text="Scan Media Folder", command=lambda:threading.Thread(target=buttonFolderAScan).start())
buttonCheckConsistencyFolderA.config(bg="#E4E2E2", fg="#000")
buttonCheckConsistencyFolderA.place(x=15, y=168, height=40)

if getLastestCompFolderA() is not None:
    entrySrcFolderA.insert(0, getLastestCompFolderA())
else:
    entrySrcFolderA.insert(0, "C:\\Prive\\fotos_unprocessed")

main.mainloop()