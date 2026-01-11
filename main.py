from visionmus import read_image_templates
from ocr_cartas import leer_mano
from posicionbaraja import deckposition

def analizar_imagen(image_path):
    """Analiza una imagen y retorna puntuaciones, cartas y posición de baraja"""
    
    rois_baraja = [
        (100, 1391, 50, 50),
        (100, 628, 50, 50),
        (925, 609, 50, 50),
        (915, 1403, 50, 50),       
    ]
    
    # leer puntuaciones (marcadores)
    try:
        eq1, eq2 = read_image_templates(image_path, "plantillasmarcador")
    except Exception as e:
        eq1, eq2 = "Error", "Error"
    
    # leer cartas en mano
    try:
        cartas = leer_mano(image_path)
    except Exception as e:
        cartas = []
    
    # detectar posición de baraja
    try:
        posicion = deckposition(image_path, rois_baraja)
    except Exception as e:
        posicion = "Error"
    

    
    print(f"\n{'='*50}")
    print(f"Equipo 1: {eq1}")
    print(f"Equipo 2: {eq2}")
    print(f"Cartas: {cartas}")
    print(f"Baraja: {posicion if isinstance(posicion, str) else f'Posición {posicion + 1}'}")
    print(f"{'='*50}\n")
    
    return {
        "equipo1": eq1,
        "equipo2": eq2,
        "cartas": cartas,
        "baraja": posicion
    }


if __name__ == "__main__":
   
    resultado = analizar_imagen("capturastodas/capturamas2.png")
