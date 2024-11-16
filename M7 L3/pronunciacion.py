import speech_recognition as speech_recog
import random
import time
import difflib

niveles = {
    "facil": {
        "español": ["perro", "gato", "sol"],
        "ingles": ["apple", "dog", "house"],
        "frances": ["pomme", "chien", "maison"],
        "japones": ["りんご (ringo)", "犬 (inu)", "家 (ie)"],
        "ruso": ["яблоко (yabloko)", "собака (sobaka)", "дом (dom)"]
    },
    "medio": {
        "español": ["programación", "internet", "ordenador"],
        "ingles": ["bye", "algorithm", "bed"],
        "frances": ["au revoir", "algorithme", "lit"],
        "japones": ["さようなら (sayōnara)", "アルゴリズム (arugorizumu)", "ベッド (beddo)"],
        "ruso": ["до свидания (do svidaniya)", "алгоритм (algoritm)", "кровать (krovat')"]
    },
    "dificil": {
        "español": ["computadora cuántica", "algoritmo genético", "inteligencia emocional"],
        "ingles": ["neural network", "machine learning", "artificial intelligence"],
        "frances": ["réseau neuronal", "apprentissage automatique", "intelligence artificielle"],
        "japones": ["ニューラルネットワーク (nyu-raru nettowāku)", "機械学習 (kikai gakushuu)", "人工知能 (jinkou chinou)"],
        "ruso": ["нейронная сеть (neyronnaya set')", "машинное обучение (mashinnoye obucheniye)", "искусственный интеллект (iskusstvennyy intellekt)"]
    }
}

pronunciaciones = {
    "perro": ["pe·rro"],
    "gato": ["ga·to"],
    "sol": ["sol"],
    "apple": ["ˈæpəl"],
    "dog": ["dɔɡ"],
    "house": ["haʊs"],
    "pomme": ["pɔm"],
    "chien": ["ʃjɛ̃"],
    "maison": ["mɛzɔ̃"],
    "りんご (ringo)": ["rinɡo"],
    "犬 (inu)": ["inu"],
    "家 (ie)": ["ie"],
    "яблоко (yabloko)": ["jablɒkə"],
    "собака (sobaka)": ["sɒbəkə"],
    "дом (dom)": ["dom"],
    "programación": ["pro·gra·ma·ción"],
    "internet": ["in·ter·net"],
    "ordenador": ["or·de·na·dor"],
    "bye": ["baɪ"],
    "algorithm": ["ˈælɡəˌrɪðəm"],
    "bed": ["bɛd"],
    "au revoir": ["oʁəvwaʁ"],
    "algorithme": ["alɡɔʁitm"],
    "lit": ["li"],
    "neural network": ["ˈnʊrəl ˈnɛtwɜːrk"],
    "machine learning": ["məˈʃiːn ˈlɜːnɪŋ"],
    "artificial intelligence": ["ɑːtɪˈfɪʃəl ɪnˈtɛlɪdʒəns"],
    "réseau neuronal": ["ʁezo nœʁɔnal"],
    "apprentissage automatique": ["aprɑ̃tisaʒ otomatik"],
    "intelligence artificielle": ["ɛ̃tɛlɛʒɑ̃s aʁtifiθjɛl"],
    "ニューラルネットワーク (nyu-raru nettowāku)": ["nyu-raru nettowāku"],
    "機械学習 (kikai gakushuu)": ["kikai gakushuu"],
    "人工知能 (jinkou chinou)": ["dʒinkou tʃinou"],
    "нейронная сеть (neyronnaya set')": ["neyronnaya set'"],
    "машинное обучение (mashinnoye obucheniye)": ["mashinnoye obucheniye"],
    "искусственный интеллект (iskusstvennyy intellekt)": ["iskusstvennyy intellekt"]
}

# Función para reconocer la voz del usuario
def speech(language="es-ES"):
    recog = speech_recog.Recognizer()
    mic = speech_recog.Microphone()

    try:
        with mic as audio_file:
            recog.adjust_for_ambient_noise(audio_file)
            print("Por favor, di la palabra... 😋")
            audio = recog.listen(audio_file, timeout=5)  # Tiempo máximo para hablar 5s
            return recog.recognize_google(audio, language=language)
    except speech_recog.UnknownValueError:
        print("No se entendió nada, intenta de nuevo. 😥")
        return None
    except speech_recog.RequestError:
        print("Error con el servicio de reconocimiento de voz. 😯")
        return None
    except speech_recog.WaitTimeoutError:
        print("No has dicho nada a tiempo. 🫤")
        return None

# Función para elegir el idioma y nivel por texto
def elegir_idioma_y_nivel():
    idioma = input("Por favor, elige el idioma ('español', 'ingles', 'frances', 'japones', 'ruso'): ").lower()
    if idioma not in ["español", "ingles", "frances", "japones", "ruso"]:
        print("Idioma no reconocido. Por favor, selecciona uno de los siguientes: español, ingles, frances, japones, ruso.")
        return elegir_idioma_y_nivel()

    nivel = input("Ahora, elige el nivel de dificultad ('facil', 'medio', 'dificil'): ").lower()
    if nivel not in ["facil", "medio", "dificil"]:
        print("Nivel no reconocido. Por favor, selecciona uno de los siguientes: facil, medio, dificil.")
        return elegir_idioma_y_nivel()

    return idioma, nivel

# Función para comparar la respuesta con la palabra usando difflib
def comparar_respuesta(respuesta, palabra, umbral=0.8):
    ratio = difflib.SequenceMatcher(None, respuesta.lower(), palabra.lower()).ratio()
    return ratio >= umbral  # Si la similitud es mayor al umbral (80%)

def play_game():
    idioma, nivel = elegir_idioma_y_nivel()
    
    idioma_map = {
        "español": "es-ES",
        "ingles": "en-EN",
        "frances": "fr-FR",
        "japones": "ja-JP",
        "ruso": "ru-RU"
    }

    palabras = niveles[nivel][idioma]
    language = idioma_map.get(idioma, "es-ES")  # Usamos el idioma seleccionado para el reconocimiento

    score = 0
    intentos_totales = 3 

    for palabra in palabras:
        intentos = intentos_totales
        while intentos > 0:
            print(f"Tienes {intentos} intentos para decir: '{palabra}'")
            inicio = time.time()
            respuesta = speech(language)  # Llamamos a la función de reconocimiento de voz
            tiempo_transcurrido = time.time() - inicio

            if tiempo_transcurrido > 5:
                print("¡Se acabó el tiempo! No has respondido a tiempo. 😕")
                break

            if respuesta is None:
                intentos -= 1  # Si no se entendió nada, perdemos un intento
            elif comparar_respuesta(respuesta, palabra):
                print("¡Correcto! 😜")
                score += 1
                break  # Si la palabra fue correcta, pasamos a la siguiente palabra
            else:
                print("Incorrecto. Inténtalo de nuevo. 🙌")
                intentos -= 1  # Si la palabra es incorrecta, perdemos un intento

        if intentos == 0:
            print(f"No lograste decir '{palabra}' correctamente. 🤐")

    if score == len(palabras):
        if nivel == "dificil":
            print("🎉¡Felicidades, ganaste el juego en el nivel difícil!🎉")
        else:
            print("🎊¡Has pasado al siguiente nivel!🎊")
    else:
        print("¡Inténtalo de nuevo! Puedes mejorar tu puntuación. 🫡")
    
    print(f"Puntuación final: {score}/{len(palabras)} 👌")

# Ejecutar el juego
if __name__ == "__main__":
    play_game()
