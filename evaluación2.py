import urllib.parse
import requests

ROUTE_URL = "https://graphhopper.com/api/1/route"
GEOCODE_URL = "https://graphhopper.com/api/1/geocode"

API_KEY = "ef529776-da3b-46c4-8bf0-0ed54366ad13"


def obtener_coordenadas(ubicacion):
    """
    Función para obtener latitud, longitud y nombre oficial de una ciudad o dirección.
    """
    url = f"{GEOCODE_URL}?q={urllib.parse.quote(ubicacion)}&locale=es&key={API_KEY}"
    respuesta = requests.get(url)

    if respuesta.status_code == 200:
        datos = respuesta.json()
        if datos.get("hits"):
            punto = datos["hits"][0]["point"]
            nombre = datos["hits"][0]["name"]
            return punto["lat"], punto["lng"], nombre

    return None, None, None


def main():
    print("==================================================")
    print("   SISTEMA DE GEOLOCALIZACIÓN Y PLANIFICACIÓN")
    print("   BIBLIOTECA NACIONAL")
    print("==================================================")
    print("Nota: Escriba 's' o 'salir' para cerrar la aplicación.\n")

    while True:
        # --- REQUERIMIENTOS 1 y 3: Solicitud en español y opción de salida ---
        origen_input = input("Ingrese la ciudad/punto de origen: ").strip()
        if origen_input.lower() in ["s", "salir"]:
            print("\n¡Gracias por utilizar el sistema de geolocalización! Hasta luego.")
            break

        destino_input = input("Ingrese la ciudad/punto de destino: ").strip()
        if destino_input.lower() in ["s", "salir"]:
            print("\n¡Gracias por utilizar el sistema de geolocalización! Hasta luego.")
            break

        print("\nObteniendo datos de ubicación...")
        lat_origen, lng_origen, nombre_origen = obtener_coordenadas(origen_input)
        lat_destino, lng_destino, nombre_destino = obtener_coordenadas(destino_input)

        if not lat_origen or not lat_destino:
            print(" Error: No se encontraron coordenadas para una o ambas ubicaciones. Intente de nuevo.\n")
            continue

        # --- REQUERIMIENTO 4: Configurar locale="es" para obtener narrativa en español ---
        params = {
            "point": [f"{lat_origen},{lng_origen}", f"{lat_destino},{lng_destino}"],
            "vehicle": "car",
            "locale": "es",
            "key": API_KEY,
            "instructions": "true"
        }

        respuesta = requests.get(ROUTE_URL, params=params)

        if respuesta.status_code == 200:
            datos_ruta = respuesta.json()
            ruta = datos_ruta["paths"][0]

            # Conversión de valores numéricos
            distancia_km = ruta["distance"] / 1000.0          # Convertir metros a kilómetros
            tiempo_min = ruta["time"] / (1000.0 * 60.0)      # Convertir milisegundos a minutos
            tiempo_horas = tiempo_min / 60.0                 # Convertir minutos a horas

            # --- REQUERIMIENTOS 1 y 2: Respuesta en español y formato a 2 decimales (.2f) ---
            print("\n" + "=" * 55)
            print(f" RESUMEN DEL VIAJE: {nombre_origen} -> {nombre_destino}")
            print(f"Distancia total: {distancia_km:.2f} km")
            print(f"Tiempo estimado: {tiempo_min:.2f} minutos ({tiempo_horas:.2f} horas)")
            print("=" * 55)

            # --- REQUERIMIENTO 4: Narrativa e instrucciones paso a paso en español ---
            print("\n NARRATIVA DEL VIAJE (PASO A PASO EN ESPAÑOL):")
            instrucciones = ruta.get("instructions", [])

            for idx, paso in enumerate(instrucciones, 1):
                texto_paso = paso.get("text", "Siga la vía")
                dist_paso_km = paso.get("distance", 0) / 1000.0
                print(f"  {idx}. {texto_paso} ({dist_paso_km:.2f} km)")

            print("=" * 55 + "\n")
        else:
            print(f" Error en la consulta a la API de Graphhopper (Código HTTP: {respuesta.status_code})\n")


if __name__ == "__main__":
    main()