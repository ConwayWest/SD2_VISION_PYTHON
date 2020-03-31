import cv2
import numpy as np
import tkinter as tk

cap = cv2.VideoCapture(0)

while True:
    _, frame = cap.read()

    greyFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    laplacian = cv2.Laplacian(greyFrame, cv2.CV_64F)
    sobel = cv2.Sobel(greyFrame, cv2.CV_64F, 1, 1, 5)
    edges = cv2.Canny(greyFrame, 50, 50)

    cv2.imshow('Original', frame)
    cv2.imshow('Laplacian', laplacian)
    cv2.imshow('Sobel', sobel)
    cv2.imshow('Edges', edges)

    # press escape key to exit
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
cap.release()
