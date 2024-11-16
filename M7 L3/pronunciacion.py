import speech_recognition as speech_recog
import random
import time

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

def speech(language="es-ES"):
    recog = speech_recog.Recognizer()
    mic = speech_recog.Microphone()

    try:
        with mic as audio_file:
            recog.adjust_for_ambient_noise(audio_file)
            print("Por favor, di la palabra... 😋")
            audio = recog.listen(audio_file, timeout=5) 
            return recog.recognize_google(audio, language=language)
    except speech_recog.UnknownValueError:
        print("Intenta de nuevo. 😥")
        return None
    except speech_recog.WaitTimeoutError:
        print("No has dicho nada a tiempo. 🫤")
        return None

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
    language = idioma_map.get(idioma, "es-ES") 

    score = 0
    intentos_totales = 3 

    for palabra in palabras:
        intentos = intentos_totales
        while intentos > 0:
            print(f"Tienes {intentos} intentos para decir: '{palabra}'")
            inicio = time.time()
            respuesta = speech(language)  
            tiempo_transcurrido = time.time() - inicio

            if tiempo_transcurrido > 5:
                print("¡Se acabó el tiempo! No has respondido a tiempo. 😕")
                break

            if respuesta is None:
                intentos -= 1  
            elif respuesta.lower() == palabra.lower():
                print("¡Correcto! 😜")
                score += 1
                break  
            else:
                print("Incorrecto. Inténtalo de nuevo. 🙌")
                intentos -= 1 

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

if __name__ == "__main__":
    play_game()
