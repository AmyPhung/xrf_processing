from gui import XRFWindow

if __name__=="__main__":
    window = XRFWindow()
    while True:
        window.update()
        if window.send_data:
            print("Sending XRF data!")
            window.send_data = False
