@echo off
pyinstaller --noconsole --onefile --hidden-import=pyscreenshot --hidden-import=pyimgur --hidden-import=cv2 --hidden-import=pyautogui client.py