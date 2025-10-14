import cv2
from pyzbar.pyzbar import decode


# vars
lastScan = ""

# main
if __name__ == "__main__":
    
    # vid cap
    cap = cv2.VideoCapture(0)
    
    while True:
    
        # works
        ret, frame = cap.read()
        if not ret:
            break

        
        # decode qr
        decoded = decode(frame)

        # use the info decoded
        for i in decoded:
            dat = i.data.decode("utf-8")
            
            # send only one signal
            if lastScan != dat:
                lastScan = dat
                print(dat)

            # highlight qr
            (x, y, w, h) = i.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # cv2 show
        cv2.imshow("Scanner", frame)

        # quit
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    
    # cleanup
    cap.release()
    cv2.destroyAllWindows()
