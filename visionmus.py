import cv2
import numpy as np
import os

def read_image_templates(image, folder):
    img_rgb = cv2.imread(image)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

    x1, y1 = 200, 102  # superior izq
    x2, y2 = 380, 170  # inferior der
    roi = img_gray[y1:y2, x1:x2]
    cv2.imshow('recorte', roi)
    cv2.waitKey(0)


img = "WhatsApp Image 2026-01-03 at 15.45.44 (4).jpeg"
read_image_templates(img, "plantillasmarcador")
