git pull
rmdir /S /Q __pycache__
rmdir /S /Q build
rmdir /S /Q dist
del reverse_shell.spec
Rem c:\Python38\Scripts\pyinstaller --onefile --noconsole reverse_shell.py
c:\Python38\Scripts\pyinstaller --onefile reverse_shell.py
cd dist
reverse_shell.exe
cd ..