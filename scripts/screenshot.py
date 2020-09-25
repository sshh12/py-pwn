def main(state):
    from PIL import ImageGrab
    import pyimgur
    import os

    save_fn = "temp.png"

    im = ImageGrab.grab()
    im.save(save_fn)
    imgur = pyimgur.Imgur(state["imgur_key"])
    uploaded_image = imgur.upload_image(save_fn, title="...")
    os.remove(save_fn)
    state["result"] = uploaded_image.link