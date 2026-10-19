import random
import string
import requests

API_URL = "http://library.demo.local/api/v1/books"

# Configuración con tu API Key
HEADERS = {
    "Content-Type": "application/json",
    "x-api-key": "cisco|NPfbWvuegUI6gQJyTv8sVBmm9uX5X7t6ihYJ1w5VUHU"
}

autores = ["Gabriel Garcia", "Isabel Allende", "Jorge Luis", "Mario Vargas", "Pablo Neruda"]
temas = ["Redes Avanzadas", "Ciberseguridad", "Python Scripting", "Cloud Computing", "DevOps Integracion", "Sistemas Distribuidos"]

# Generación e inserción de 50 libros (IDs del 8 al 57)
for i in range(8, 58):
    payload = {
        "id": i,
        "title": f"{random.choice(temas)} Vol. {random.randint(1, 10)}",
        "author": f"{random.choice(autores)} {random.randint(100, 999)}",
        "isbn": "".join(random.choices(string.digits, k=9))
    }

    try:
        response = requests.post(API_URL, json=payload, headers=HEADERS)
        print(f"Libro ID {i} -> Estado HTTP: {response.status_code} | Respuesta: {response.text}")
    except Exception as e:
        print(f"Error al enviar el libro {i}: {e}")import urllib.parse
import requests

# URLs base de la API de Graphhopper
route_url = "https://graphhopper.com/api/1/route?"
loc1_url = "https://graphhopper.com/api/1/geocode?"

# Coloca aquí tu token/API Key de Graphhopper
KEY = "TU_GRAPHPOPPER_API_KEY"

def geocodificar(localizacion, key):
    while localizacion == "":
        localizacion = input("Por favor, ingrese una ubicación válida: ")
   
    url = loc1_url + urllib.parse.urlencode({"q": localizacion, "limit": "1", "key": key})
    respuesta = requests.get(url)
    estado = respuesta.status_code
    datos = respuesta.json()

    if estado == 200 and len(datos["hits"]) != 0:
        lat = datos["hits"][0]["point"]["lat"]
        lng = datos["hits"][0]["point"]["lng"]
        nombre = datos["hits"][0]["name"]
        estado_region = datos["hits"][0].get("state", "")
        pais = datos["hits"][0].get("country", "")

        nombre_completo = nombre
        if estado_region:
            nombre_completo += f", {estado_region}"
        if pais:
            nombre_completo += f", {pais}"

        return estado, lat, lng, nombre_completo
    else:
        print(f"Error: No se encontró la ubicación '{localizacion}'.")
        return estado, None, None, localizacion

while True:
    print("\n" + "=" * 45)
    print("      SOFTWARE DE GEOLOCALIZACIÓN Y RUTAS      ")
    print("=" * 45)
    print("Escriba 's' o 'salir' en cualquier momento para finalizar.")

    origen_input = input("\nIngrese la ciudad de origen: ").strip()
    if origen_input.lower() in ["s", "salir"]:
        print("¡Programa finalizado!")
        break

    destino_input = input("Ingrese la ciudad de destino: ").strip()
    if destino_input.lower() in ["s", "salir"]:
        print("¡Programa finalizado!")
        break

    estado_origen, lat1, lng1, nombre_origen = geocodificar(origen_input, KEY)
    estado_destino, lat2, lng2, nombre_destino = geocodificar(destino_input, KEY)

    if estado_origen == 200 and estado_destino == 200 and lat1 and lat2:
        puntos = f"&point={lat1}%2C{lng1}&point={lat2}%2C{lng2}"
       
        # 'locale': 'es' asegura la narrativa del viaje en español desde la API
        parametros_ruta = urllib.parse.urlencode({
            "key": KEY,
            "vehicle": "car",
            "locale": "es"
        })
       
        url_ruta = route_url + parametros_ruta + puntos
        res_ruta = requests.get(url_ruta)
        estado_ruta = res_ruta.status_code
        datos_ruta = res_ruta.json()

        if estado_ruta == 200:
            distancia_m = datos_ruta["paths"][0]["distance"]
            tiempo_ms = datos_ruta["paths"][0]["time"]

            distancia_km = distancia_m / 1000
            tiempo_min = tiempo_ms / 1000 / 60
            tiempo_hrs = tiempo_min / 60

            print("\n" + "-" * 45)
            print(f"Origen:  {nombre_origen}")
            print(f"Destino: {nombre_destino}")
            # Formato con máximo de dos decimales (:.2f)
            print(f"Distancia total: {distancia_km:.2f} km")
            print(f"Tiempo estimado: {tiempo_min:.2f} minutos ({tiempo_hrs:.2f} horas)")
            print("-" * 45)
            print("\nNarrativa del viaje (Instrucciones paso a paso):")

            instrucciones = datos_ruta["paths"][0]["instructions"]
            for i, paso in enumerate(instrucciones, 1):
                dist_paso = paso["distance"] / 1000
                print(f"{i}. {paso['text']} ({dist_paso:.2f} km)")
        else:
            print(f"Error al calcular la ruta. Código HTTP: {estado_ruta}")
