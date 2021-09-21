from constants import HOST_IP, HOST_PORT, WEBCAM_HEIGHT, WEBCAM_WIDTH
import socket
import threading
import pickle
from zlib import compress
import cv2


def startServer():
    """
    Starts and configures the server
    """

    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.bind((HOST_IP, HOST_PORT))
    soc.listen()

    # Accept clients
    while True:
        clientSocket, _ = soc.accept()
        threading.Thread(target=shareWebCam, args=(
            clientSocket,)).start()


def shareWebCam(soc):
    """
    Shares the web camera

    param 1: the socket connection
    param 1 type: socket.socket
    """

    # Send some initiation things

    # Sends the Width and Height of the screen sharing
    soc.send(f"{WEBCAM_HEIGHT} {WEBCAM_WIDTH}".encode())

    cam = cv2.VideoCapture(0)  # Gets the camera on the index 0
    # Starts sends frames
    while True:
        frame = getFrame(cam)
        sendFrame(soc, frame)


def sendFrame(sock, frame):
    """
    Sends the frame to the client

    param 1: the socket connection
    param 2: the frame to send

    param 1 type: socket.socket
    param 2 type: mss.screenshot.Screenshot

    How the sending is done:

    Dumps the frame pixels via [pickle]  
    Compresses the dumped pixels
    Computes the length of the compressed pixels bytes array
    Computes how much bits needed to presents the length of the compressed pixels bytes array

    Sends the bits number
    Sends the actual length of the pixels
    Sends the actual pixels
    """

    dumped_frame = pickle.dumps(frame)

    # Compressed the pixels of the image
    compressedImg = compress(dumped_frame, 6)

    # Send the size of the pixels length

    # The len of the [compressedImg] bytes array
    compressedPixelsLen = len(compressedImg)
    # How much bits needed to presents [compressedPixelsLen]
    # TODO: check the + 7 // 8 meaning
    compressedPixelsLen_bitsLen = (compressedPixelsLen.bit_length() + 7) // 8
    # Sends [compressedPixelsLen_bitsLen]
    sock.send(bytes([compressedPixelsLen_bitsLen]))

    # Send the actual pixels length
    size_bytes = compressedPixelsLen.to_bytes(
        compressedPixelsLen_bitsLen, 'big')
    sock.send(size_bytes)

    # Send pixels
    sock.sendall(compressedImg)


def getFrame(cam):
    """
    Captures frame from the web camera and returns that
    """

    s, img = cam.read()
    return img


def main():
    startServer()


if __name__ == "__main__":
    main()
