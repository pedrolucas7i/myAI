import speech_recognition as sr
import pywhatkit
import webbrowser
import pyautogui
import time
import subprocess
import os
from llamaapi import LlamaAPI
import json
from gtts import gTTS

llama = LlamaAPI("LL-74vx4n9A2DMUkNemnLyTrXHcHbK1cPMwTTOoJYvowylU5gNPfv1WAxIJIvRNlbos")

recognizer = sr.Recognizer()

comandos = """
1 - Assistente                               (Verifica se está ouvindo)
2 - Pesquisa(r) no Google <pesquisa>         (Efetua uma pesquisa no Google)
3 - Pesquisa(r) no Youtube <vídeo/musica>    (Mostra vídeos/musicas relacionado(a)s)
4 - Pesquisa(r) imagem/imagens de <conteudo> (Pesquisa imagens no Pixabay)
5 - Toca(r) uma música                       (Toca todas as músicas da pasta MUSIC de forma aleatória)
6 - Objeto 3d de <objeto>                    (Pesquisa objetos 3d relacionados no Thingiverse)
7 - Abre a ferramenta 3d                     (Abre a ferramenta 3D Tinkercad)
8 - Modo inteligência/inteligente artificial (AI)
"""


def speak(response):
    language = "pt"
    file = gTTS(text=response, lang=language, slow=False)
    file.save("resposta.mp3")
    os.system("play resposta.mp3")


def recognize():
    try:
        with sr.Microphone() as source:
            print("\033[0;32;40m" + comandos + "\033[m")
            print("Escutando...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
            comando = recognizer.recognize_google(audio, language="pt")
            comando = comando.lower()
            return comando
    except sr.UnknownValueError:
        print("Não Entendi")
        return ""


def search_on_youtube(content):
    pywhatkit.playonyt(content)
    speak("A redirecionar")
    time.sleep(3)
    pyautogui.press("space")


def search_images(content):
    webbrowser.open("https://pixabay.com/pt/images/search/" + content)
    speak("A redirecionar")


def search_google(content):
    webbrowser.open("https://www.google.com/search?q=" + content)
    speak("A redirecionar")


def play_music():
    speak("A tocar a playlist")
    subprocess.call("mpg123 -Z ./MUSIC/*", shell=True)


modo = False
while True:
    command = recognize().lower()
    print(command)

    if "assistente" in command:
        speak("Sim Mestre")

    elif "pesquisar no google" in command:
        search_google(command.replace("pesquisar no google", ""))

    elif "pesquisa no google" in command:
        search_google(command.replace("pesquisa no google", ""))

    elif "pesquisar no youtube" in command:
        search_on_youtube(command.replace("pesquisar no youtube", ""))

    elif "pesquisa no youtube" in command:
        search_on_youtube(command.replace("pesquisa no youtube", ""))

    elif "pesquisar imagem de" in command:
        search_images(command.replace("pesquisar imagem de", ""))

    elif "pesquisa imagem de" in command:
        search_images(command.replace("pesquisa imagem de", ""))

    elif "pesquisar imagens de" in command:
        search_images(command.replace("pesquisar imagens de", ""))

    elif "pesquisa imagens de" in command:
        search_images(command.replace("pesquisa imagens de", ""))

    elif "tocar uma música" in command:
        play_music()

    elif "toca uma música" in command:
        play_music()

    elif "objeto 3d de" in command:
        webbrowser.open(
            "https://www.thingiverse.com/search?q="
            + command.replace("objeto 3d de", "")
        )
        speak("A redirecionar")

    elif "abre a ferramenta 3d" in command:
        webbrowser.open("https://www.tinkercad.com/dashboard")
        speak("A redirecionar")

    elif (
        "modo inteligente artificial" in command
        or "modo inteligência artificial" in command
    ):
        modo = True
        speak("Modo IA ativado!")
        while modo:
            command = recognize().lower()
            print(command)
            if "sair" in command:
                modo = False
            else:
                content = command
                api_request_json = {
                    "model": "llama3-70b",
                    "messages": [
                        {"role": "user", "content": content},
                    ],
                }
                response = llama.run(api_request_json)
                if response.status_code == 200:
                    response_json = response.json()
                    if "choices" in response_json:
                        speak(response_json["choices"][0]["message"]["content"])
                else:
                    speak("Desculpe, ocorreu um erro na solicitação.")
