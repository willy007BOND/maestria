#!/usr/bin/env python3
"""
Script para corregir la estructura del archivo act-2-companies.json

Problema identificado:
- El archivo contiene múltiples objetos JSON separados por líneas (formato NDJSON)
- No es un array JSON válido (falta [ ] y comas entre objetos)

Solución:
- Leer cada línea como un objeto JSON independiente
- Combinar todos los objetos en un array JSON válido
- Guardar el resultado en un archivo corregido
"""

import json
import sys

def fix_json_structure(input_file, output_file):
    """
    Convierte un archivo NDJSON (JSON Lines) a un array JSON válido

    Args:
        input_file: Ruta al archivo de entrada con formato NDJSON
        output_file: Ruta al archivo de salida con formato JSON array
    """
    companies = []
    line_count = 0
    error_count = 0

    print(f"Leyendo archivo: {input_file}")

    with open(input_file, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:  # Saltar líneas vacías
                continue

            try:
                # Parsear cada línea como un objeto JSON
                company = json.loads(line)
                companies.append(company)
                line_count += 1

                if line_count % 1000 == 0:
                    print(f"  Procesadas {line_count} empresas...")

            except json.JSONDecodeError as e:
                error_count += 1
                print(f"  ERROR en línea {line_num}: {e}")

    print(f"\nTotal de empresas procesadas: {line_count}")
    print(f"Errores encontrados: {error_count}")

    # Escribir el array JSON válido
    print(f"\nEscribiendo archivo corregido: {output_file}")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(companies, f, indent=2, ensure_ascii=False)

    print(f"✓ Archivo corregido guardado exitosamente")
    print(f"✓ Estructura: Array JSON con {len(companies)} objetos")

    return len(companies), error_count

if __name__ == "__main__":
    input_file = "/Users/willdev/github/UNIR/maestria/actividad_2/act-2-companies.json"
    output_file = "/Users/willdev/github/UNIR/maestria/actividad_2/act-2-companies-fixed.json"

    try:
        total, errors = fix_json_structure(input_file, output_file)
        print(f"\n{'='*60}")
        print(f"RESUMEN:")
        print(f"  - Objetos procesados: {total}")
        print(f"  - Errores: {errors}")
        print(f"  - Archivo original: {input_file}")
        print(f"  - Archivo corregido: {output_file}")
        print(f"{'='*60}")

    except Exception as e:
        print(f"\n❌ Error fatal: {e}", file=sys.stderr)
        sys.exit(1)
