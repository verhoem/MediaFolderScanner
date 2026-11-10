# MediaFolderScanner
Python project to scan your folders for duplicate files, arrange folder struct root/year/month

You gather a lot of media files over the years, from multiple devices but also from relatives etc.
My folder grew large and backing up became more more tedious.

This tool I created to first scan a folder for files with same size (for performance ) and hashes 
the first 100k bytes to compare files indeed equal content wise even if size is equal. 
I choose only to hash 100k for performance. You could adjust this but in my experience media files 
( movies, photos, audio ) 100K is sufficient to catch duplicate files. 

Next is to check location and filename. I decided for structure year/month/file and file name starting with 
yyyymmdd_ related to modification time of file.

If scan runs into files that are not according to this location / naming user is asked to correct them.

Make executable with :

Install the runtime dependency first:

```powershell
py -m pip install -r requirements.txt
```

Then build the executable:

```powershell
py -m pip install pyinstaller
py -m PyInstaller --onefile --windowed --name MediaFolderScanner .\Scan_media_folder.py
```

Alternatively, run the script directly with `py .\Scan_media_folder.py`.

Version 4.0.1: Added help, ttkbootstrap GUI, and improved performance.
