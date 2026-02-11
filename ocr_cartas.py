import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def rotar_imagen(imagen, angle):
    (h, w) = imagen.shape[:2]
    centro = (w // 2, h // 2)

    M = cv2.getRotationMatrix2D(centro, angle, 1.0)
    rotada = cv2.warpAffine(imagen, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_CONSTANT, borderValue=(255, 255, 255))
    return rotada

def preprocesar_roi(roi, angulo_rotacion):
    
    roi_rotada = rotar_imagen(roi, angulo_rotacion)
    
    _, thresh = cv2.threshold(roi_rotada, 160, 255, cv2.THRESH_BINARY)
    
    scale_percent = 200 
    width = int(thresh.shape[1] * scale_percent / 100)
    height = int(thresh.shape[0] * scale_percent / 100)
    dim = (width, height)
    thresh_resized = cv2.resize(thresh, dim, interpolation=cv2.INTER_LINEAR)
    
    thresh_final = cv2.copyMakeBorder(thresh_resized, 10, 10, 10, 10, cv2.BORDER_CONSTANT, value=[255, 255, 255])
    
    return thresh_final

def leer_mano(image_path):
    img = cv2.imread(image_path)
    if img is None:
        print("Error: No se pudo cargar la imagen.")
        return []
    
    ROIS = [
        (167, 1535, 44, 43),  
        (355, 1510, 50, 47),  
        (531, 1510, 50, 47),  
        (712, 1515, 50, 47)   
    ]
    ANGULOS = [-10, -5, 0, 10]
    numbers_det = []
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    for i , (x,y,w,h) in enumerate(ROIS):
        roi = gray[y:y+h, x:x+w]
        img_para_ocr = preprocesar_roi(roi, ANGULOS[i])
        #_ , thresh = cv2.threshold(roi, 160, 255, cv2.THRESH_BINARY) 
        config = r'--psm 7 -c tessedit_char_whitelist=0123456789'

        text = pytesseract.image_to_string(img_para_ocr, config=config)
        number = text.strip()
        if not number:
            number = "?"
        numbers_det.append(number)
    # debug
        cv2.imshow(f"Carta {i+1}", img_para_ocr)

    cv2.waitKey(0) 
    cv2.destroyAllWindows()

    return numbers_det

# ruta_imagen = "capturastodas/capturamas2.png"
# result = leer_mano(ruta_imagen)
# print("Mano detectada:", result)


