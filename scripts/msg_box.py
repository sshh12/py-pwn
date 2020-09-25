def main(state, title="Alert", text="", style=1):
    import ctypes

    ctypes.windll.user32.MessageBoxW(0, text, title, style)