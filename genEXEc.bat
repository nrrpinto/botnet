git pull
rmdir /S /Q __pycache__
rmdir /S /Q build
rmdir /S /Q dist
del reverse_shell.spec
Rem c:\Python38\Scripts\pyinstaller --onefile --noconsole --icon c:\Users\rever\Downloads\Chrome_icon_2.ico reverse_shell.py
Rem c:\Python38\Scripts\pyinstaller --onefile --noconsole --icon c:\Users\rever\Downloads\iconfinder_image_285633.ico reverse_shell.py
c:\Python38\Scripts\pyinstaller --onefile --icon c:\Users\rever\Downloads\iconfinder_image_285633.ico reverse_shell.py
Rem c:\Python38\Scripts\pyinstaller --onefile reverse_shell.py
cd dist
Rem reverse_shell.exe
cd ..