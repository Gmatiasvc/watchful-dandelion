import cv2
from pyzbar.pyzbar import decode
import database
from datetime import datetime

# vars
lastScan = ""
r = (0,0)

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
                
                # execute db query
                r = database.entryAction(dat)

                # highlight qr
            (x, y, w, h) = i.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)


                # draw response
            if r[0] == 0:
                cv2.putText(
                    frame,  # type: ignore
                    str("Salida ya registrada"),
                    (x- 15, y + h + 25),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 0, 255),
                    2,
                )

            elif r[0] == -1:
                cv2.putText(
                    frame,  # type: ignore
                    str(f"Datos no encontrados"),
                    (x- 15, y + h + 25),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (255, 0, 0),
                    2,
                )

            elif r[0] == 1:
                dt = datetime.fromtimestamp(r[1])
                cv2.putText(
                    frame,  # type: ignore
                    str(f"Entrada registrada\n{dt.strftime("%Y-%m-%d %H:%M:%S")}"),
                    (x- 15, y + h + 25),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 0),
                    2,
                )

            elif r[0] == 2:
                dt = datetime.fromtimestamp(r[1])
                cv2.putText(
                    frame,  # type: ignore
                    str(f"Salida registrada\n{dt.strftime("%Y-%m-%d %H:%M:%S")}"),
                    (x- 15, y + h + 25),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 0),
                    2,
                )
        # cv2 show
        cv2.imshow("Scanner", frame)

        # quit
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # cleanup
    cap.release()
    cv2.destroyAllWindows()
