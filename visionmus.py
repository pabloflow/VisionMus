import cv2
import numpy as np
import os

def detect_numbers_in_roi(roi, folder, threshold=0.75):
    """Procesa un ROI y detecta los números en él"""
    numbers = []

    for i in range(8):
        name_template = f"{folder}/{i}.png"
        template = cv2.imread(name_template, 0)
        if template is None: continue
        res = cv2.matchTemplate(roi, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)
        for pt in zip(*loc[::-1]):
            numbers.append((pt[0], i))
    
    numbers.sort(key=lambda x: x[0])

    #evitar duplicados del mismo numero muy cerca
    resultado_final = []
    if numbers:
        last_x = -100
        for x, num in numbers:
            if abs(x - last_x) > 10: # a mas de 10px del anterior es un nuevo dígito
                resultado_final.append(str(num))
                last_x = x

    return "".join(resultado_final)

def read_image_templates(image, folder):
    img_rgb = cv2.imread(image)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

    # Marcador 1 
    x1_eq1, y1_eq1 = 245, 120   # esquina superior izquierda
    x2_eq1, y2_eq1 = 385, 175   # esquina inferior derecha
    roi_eq1 = img_gray[y1_eq1:y2_eq1, x1_eq1:x2_eq1]

    # Marcador 2 
    x1_eq2, y1_eq2 = 920, 120   
    x2_eq2, y2_eq2 = 1060, 175   
    roi_eq2 = img_gray[y1_eq2:y2_eq2, x1_eq2:x2_eq2]

    # Mostrar los ROIs mientras haces pruebas
    cv2.imshow('ROI Equipo 1', roi_eq1)
    cv2.imshow('ROI Equipo 2', roi_eq2)
    print("Presiona una tecla para continuar...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Procesar ambos ROIs
    puntuacion_eq1 = detect_numbers_in_roi(roi_eq1, folder, threshold=0.75)
    puntuacion_eq2 = detect_numbers_in_roi(roi_eq2, folder, threshold=0.75)

    return puntuacion_eq1, puntuacion_eq2

img = "capturastodas/Screenshot_20251219-195020_Mus Maestro.png"
eq1, eq2 = read_image_templates(img, "plantillasmarcador")
print(f"Equipo 1: {eq1}")
print(f"Equipo 2: {eq2}")
