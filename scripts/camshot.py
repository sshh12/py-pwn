def main(state):
    from cv2 import VideoCapture, imwrite
    import pyimgur
    import os

    save_fn = "temp.png"

    cam = VideoCapture(0)
    ret, img = cam.read()
    if ret:
        imwrite(save_fn, img)
        imgur = pyimgur.Imgur(state["imgur_key"])
        uploaded_image = imgur.upload_image(save_fn, title="...")
        os.remove(save_fn)
        state["result"] = uploaded_image.link