import cv2
import numpy as np
import os

def read_image_templates(image, folder):
    img_rgb = cv2.imread(image)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

    x1, y1 = 215, 102  # superior izq
    x2, y2 = 330, 150  # inferior der
    roi = img_gray[y1:y2, x1:x2]
    cv2.imshow('recorte', roi)
    print("Presiona una tecla en la ventana de la imagen para continuar...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    numbers = []

    for i in range(8):
        name_template = f"{folder}/{i}.png"
        template = cv2.imread(name_template, 0)
        if template is None: continue
        w, h = template.shape[::-1]
        res = cv2.matchTemplate(roi, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.75
        loc = np.where(res >= threshold)
        for pt in zip(*loc[::-1]):
            numbers.append((pt[0], i))
    
    numbers.sort(key=lambda x: x[0])

    # Filtro simple para evitar duplicados del mismo número muy cerca (opcional)
    resultado_final = []
    if numbers:
        last_x = -100
        for x, num in numbers:
            if abs(x - last_x) > 10: # Si está a más de 10px del anterior, es un nuevo dígito
                resultado_final.append(str(num))
                last_x = x

    return "".join(resultado_final)

img = "WhatsApp Image 2026-01-03 at 15.45.44 (4).jpeg"
print(read_image_templates(img, "plantillasmarcador"))
