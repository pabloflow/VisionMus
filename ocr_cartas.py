import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def leer_mano(image_path):
    img = cv2.imread(image_path)
    if img is None:
        print("Error: No se pudo cargar la imagen.")
        return []
    
    ROIS = [
        (167, 1535, 50, 55),  
        (355, 1510, 50, 55),  
        (531, 1510, 50, 55),  
        (712, 1509, 50, 55)   
    ]
    numbers_det = []
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    for i , (x,y,w,h) in enumerate(ROIS):
        roi = gray[y:y+h, x:x+w]
        _ , thresh = cv2.threshold(roi, 160, 255, cv2.THRESH_BINARY) 
        config = r'--psm 7 -c tessedit_char_whitelist=0123456789'

        text = pytesseract.image_to_string(thresh, config=config)
        number = text.strip()
        if not number:
            number = "?"
        numbers_det.append(number)
    # debug
        #cv2.imshow(f"Carta {i+1}", thresh)

    #cv2.waitKey(0) 
    #cv2.destroyAllWindows()

    return numbers_det

ruta_imagen = "capturastodas/capturamas2.png"
result = leer_mano(ruta_imagen)
print("Mano detectada:", result)


