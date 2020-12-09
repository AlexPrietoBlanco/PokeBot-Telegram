#Import cool libraries
import json
import requests
from prettytable import PrettyTable

TOKEN = 'Token here'
URLBOT = "https://api.telegram.org/bot" + TOKEN + "/"

def update(offset):
    #Llamar al metodo getUpdates del bot, utilizando un offset
    respuesta = requests.get(URLBOT + "getUpdates" + "?offset=" + str(offset) + "&timeout=" + str(100))
 
 
    #Decodificar la respuesta recibida a formato UTF8
    mensajes_js = respuesta.content.decode("utf8")
 
    #Convertir el string de JSON a un diccionario de Python
    mensajes_diccionario = json.loads(mensajes_js)
 
    #Devolver este diccionario
    return mensajes_diccionario
 
def info_mensaje(mensaje):
 
    #Comprobar el tipo de mensaje
    if "text" in mensaje["message"]:
        tipo = "texto"
    elif "sticker" in mensaje["message"]:
        tipo = "sticker"
    elif "animation" in mensaje["message"]:
        tipo = "animacion" #Nota: los GIF cuentan como animaciones
    elif "photo" in mensaje["message"]:
        tipo = "foto"
    else:
        # Para no hacer mas largo este ejemplo, el resto de tipos entran
        # en la categoria "otro"
        tipo = "otro"
 
    #Recoger la info del mensaje (remitente, id del chat e id del mensaje)
    persona = mensaje["message"]["from"]["first_name"]
    id_chat = mensaje["message"]["chat"]["id"]
    id_update = mensaje["update_id"]
 
    #Devolver toda la informacion
    return tipo, id_chat, persona, id_update
 
def leer_mensaje(mensaje):
 
    #Extraer el texto, nombre de la persona e id del último mensaje recibido
    texto = mensaje["message"]["text"]
 
    #Devolver las dos id, el nombre y el texto del mensaje
    return texto
 
def enviar_mensaje(idchat, texto):
    #Llamar el metodo sendMessage del bot, passando el texto y la id del chat
    requests.get(URLBOT + "sendMessage?text=" + texto + "&chat_id=" + str(idchat))

def get_abilities(pokemon):
    url = 'https://pokeapi.co/api/v2/pokemon/'
    response = requests.get(url+pokemon)

    if response.status_code == 200:
        response_json = response.json()
        abilities = response_json['abilities']
        abilities_list = []
        texto=""

        for ability in abilities:
            url_ability = ability.get('ability').get('url')
            response_ability = requests.get(url_ability)
            response_ability_json = response_ability.json()
            effect = response_ability_json['effect_entries']

            abilities_list.append("\n\n-->" + ability.get('ability').get('name').upper() + "\n")
            abilities_list.append(effect[1].get('effect'))

        for line in abilities_list:
            texto = texto + line

        texto = texto.replace("\\n\\n", "")
        return texto

    return False

def get_basic_info(pokemon):
    url = 'https://pokeapi.co/api/v2/pokemon/'
    response = requests.get(url+pokemon)
    texto=""

    if response.status_code == 200:
        response_json = response.json()
        nombre = response_json['name']
        base_exp = response_json['base_experience']
        height = response_json['height']/10
        weight = response_json['weight']/10
        id = response_json['id']

        texto = nombre.capitalize() + " is the Pokémon number " + str(id) + ". You will gain " + str(base_exp) + "XP points for defeating this Pokémon. It's weight is " + str(weight) + " Kg and it's height is " + str(height) + " m."
        return texto

    return False    

def get_types(pokemon):
    url = 'https://pokeapi.co/api/v2/pokemon/'
    response = requests.get(url+pokemon)

    if response.status_code == 200:
        response_json = response.json()
        types = response_json['types']
        texto=""

        for poke_type in types:
            name = poke_type.get('type').get('name')
            texto = texto + str(name).capitalize() + " "

        return texto

    return False       

def get_general_info(pokemon):
    basic = get_basic_info(pokemon)
    types = get_types(pokemon)
    abilities = get_abilities(pokemon)

    if basic and types and abilities:
        return "BASIC INFORMATION:\n" + basic + "\n\nTYPES: \n" + types + "\n\nABILITIES:" + abilities

    return False



#Variable para almacenar la ID del ultimo mensaje procesado
ultima_id = 0

while(True):
    mensajes_diccionario = update(ultima_id)
    for i in mensajes_diccionario["result"]:
 
        #Guardar la informacion del mensaje
        tipo, idchat, nombre, id_update = info_mensaje(i)
 
        #Generar una respuesta dependiendo del tipo de mensaje
        if tipo == "texto":
            texto = leer_mensaje(i)

            if get_general_info(texto.lower()):
                texto_respuesta = str(get_general_info(texto.lower()))
            else:
                texto_respuesta = "No data about this pokémon"    

        if id_update > (ultima_id-1):
            ultima_id = id_update + 1
 
        #Enviar la respuesta
        enviar_mensaje(idchat, texto_respuesta)
 
    #Vaciar el diccionario
    mensajes_diccionario = []    
