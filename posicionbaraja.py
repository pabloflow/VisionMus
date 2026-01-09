import cv2
import numpy as np

def deckposition(imagepath, rois):
    img = cv2.imread(imagepath)
    if img is None: return "Error"

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    #red range
    lower1 = np.array([0, 120, 70])
    upper1 = np.array([10, 255, 255])
    lower2 = np.array([170, 120, 70])
    upper2 = np.array([180, 255, 255]) 


    best_roi = -1
    max_red_pixels = 0
    min_red_pixels = 50

    for i, (x, y, w, h) in enumerate(rois):
        roi = hsv[y:y+h, x:x+w]
        mask1 = cv2.inRange(roi, lower1, upper1)
        mask2 = cv2.inRange(roi, lower2, upper2)
        mask = mask1 + mask2
        red_pixels = cv2.countNonZero(mask)
        color_borde = (0, 0, 255)
        if red_pixels > min_red_pixels:
            color_borde = (0, 255, 0)
            if red_pixels > max_red_pixels:
                max_red_pixels = red_pixels
                best_roi = i
        cv2.rectangle(img, (x, y), (x+w, y+h), color_borde, 2)
    if best_roi != -1:
        result = best_roi
    else:
        result = "No se detectó la baraja"
    
    #scale = 0.5  # Reduce la ventana de visualizacion de las zonas
    #img_redimensionada = cv2.resize(img, (int(img.shape[1] * scale), int(img.shape[0] * scale)))
    
    #cv2.imshow("Deteccion Baraja", img_redimensionada)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    
    return result

rois = [
        (100, 1391, 50, 50),
        (100, 628, 50, 50),
        (925, 609, 50, 50),
        (915, 1403, 50, 50),       
]

# print("La mano la tiene:", deckposition("capturastodas/mano1.png", rois))