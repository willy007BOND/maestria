import csv
import json
import sys
import os

def csv_to_json(csv_file, json_file=None):
    """
    Convierte un archivo CSV a formato JSON.
    
    Args:
        csv_file: Ruta del archivo CSV de entrada
        json_file: Ruta del archivo JSON de salida (opcional)
    """
    
    # Si no se especifica archivo de salida, usar el mismo nombre con extensión .json
    if json_file is None:
        json_file = os.path.splitext(csv_file)[0] + '.json'
    
    try:
        # Leer el archivo CSV
        with open(csv_file, 'r', encoding='utf-8') as f:
            csv_reader = csv.DictReader(f)
            data = list(csv_reader)
        
        # Escribir el archivo JSON
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        
        print(f"✓ Conversión exitosa!")
        print(f"  Archivo CSV: {csv_file}")
        print(f"  Archivo JSON: {json_file}")
        print(f"  Registros convertidos: {len(data)}")
        
    except FileNotFoundError:
        print(f"✗ Error: No se encontró el archivo '{csv_file}'")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Error durante la conversión: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    # Uso desde línea de comandos
    if len(sys.argv) < 2:
        print("Uso: python csv_to_json.py archivo.csv [salida.json]")
        print("\nEjemplo:")
        print("  python csv_to_json.py datos.csv")
        print("  python csv_to_json.py datos.csv resultado.json")
        sys.exit(1)
    
    csv_input = sys.argv[1]
    json_output = sys.argv[2] if len(sys.argv) > 2 else None
    
    csv_to_json(csv_input, json_output)