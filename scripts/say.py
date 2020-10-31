def main(state, msg="Hello"):
    import win32com.client

    speaker = win32com.client.Dispatch("SAPI.SpVoice")
    speaker.Speak(msg)