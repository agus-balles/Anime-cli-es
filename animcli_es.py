#!/usr/sbin/python3

from animeflv_scraper import Animeflv
import os
import argparse

api = Animeflv()

parser=argparse.ArgumentParser(description="Mira anime subtitulado en español.")

parser.add_argument("-A","--anime", type=str, help="Titulo del Anime")
parser.add_argument("-C","--capitulo",type=int,help="Capitulo del Anime")
parser.add_argument("-R","--reproduccion_automatica",action="store_true",help="Reproduce los siguientes episodios automáticamente.")
parser.add_argument("-D","--descarga",action="store_true",help="Descarga este episodio, y si se selecciona, los subsiguientes")

args=parser.parse_args()

def watch_video(anime,episode_list, episode_index,provider=0,passive=False):
    episode_links = api.get_links(episode_index+1)
    provider_string = episode_links[episode_list[episode_index]][provider][:14]
    if passive ==True:
        for i in range(len(episode_list)-episode_index):
            episode_links = api.get_links(episode_index+i+1)
            video_links=episode_links[episode_list[episode_index+i]]
            video= [link for link in video_links if provider_string in link][0]
            print(f"\033[1;36mEpisodio {episode_index+i+1}:\n{video}")
            os.system(f"mpv ytdl://{video} --force-media-title=\"{anime} - Episodio: {episode_index+1}\"")
    else:
        video_links=episode_links[episode_list[episode_index]]
        video= [link for link in video_links if provider_string in link][0]
        print(f"Episodio {episode_index+1}:\n{video}")
        os.system(f"mpv ytdl://{video} --force-media-title=\"{anime} - Episodio {episode_index+1}\"")

def download_video(anime_id,episode_list,episode_index,provider=0,download_following=False):
    if not os.path.isdir(anime_id):
        os.mkdir(anime_id)
    episode_links = api.get_links(episode_index+1)
    provider_string = episode_links[episode_list[episode_index]][provider][:14]
    if download_following ==True:
        for i in range(len(episode_list)-episode_index):
            episode_links = api.get_links(episode_index+i+1)
            video_links=episode_links[episode_list[episode_index+i]]
            video= [link for link in video_links if provider_string in link][0]
            print(f"\033[1;36mDescargando Episodio {episode_index+i+1}:\n{video}")
            os.system(f"yt-dlp -N 8 {video} -o {anime_id}\/{episode_list[episode_index+i]} ")
    else:
        video_links=episode_links[episode_list[episode_index]]
        video= [link for link in video_links if provider_string in link][0]
        print(f"\033[1;36mDescargando episodio {episode_index+1}:\n{video}")
        os.system(f"yt-dlp -N 8 {video} -o {anime_id}\/{episode_list[episode_index]}")

if args.anime:
    anime_id = api.search(args.anime)[0]
    animeinfo = api.anime_info(anime_id)
    title = api.anime_title()

else:
    print("Que anime quieres ver?")
    possible_anime_id = api.search(input("Anime:\033[1;36m"))

    j=1
    print("\nResultados:\n")
    for anime in possible_anime_id:
        print(f"[{j}]{anime}")
        j+=1
    anime_num = int(input("\033[1;0mSelecciona uno:"))-1

    anime_id=possible_anime_id[anime_num]

    animeinfo = api.anime_info(anime_id)

    title = api.anime_title()
    status = api.anime_status()
    summary = api.anime_summary()
    

    print(f"\033[1;92m \nTítulo: \033[1;0m{title}")
    print(f"\033[1;92mEstado: \033[1;0m{status}")
    print(f"\033[1;92m \nResumen: \033[1;0m{summary}")

episode_list = api.anime_episodes()

if args.anime and args.capitulo:
    episode_index = args.capitulo - 1
elif args.capitulo and not args.anime:
    parser.error("No se puede especificar el capitulo sin especificar el anime.")
else:
    j=1
    print("\033[1;32m\nEpisodios:\033[1;35m")
    for episode in episode_list:
        print(f"[{j}]{episode}")
        j+=1

    episode_index = int(input("\nSelecciona que episodio ver:")) - 1

    
episode_links = api.get_links(episode_index+1)

video_links=episode_links[episode_list[episode_index]]

print("\033[1;0m\nElige un proveedor: \033[1;36m")
j=1
for provider in video_links:
    print(f"[{j}]{provider}")
    j+=1
provider = int(input("Proveedor: "))-1

if args.descarga and args.reproduccion_automatica:
    parser.error("No se puede ver y descargar el anime al mismo tiempo")


if args.descarga:
    dw_all = input("Descargar tambien los siguientes episodios?(y/N): ")
    if dw_all in ("Yy") and dw_all!="":
        download_video(anime_id,episode_list,episode_index,provider,True)
    else:
        download_video(anime_id,episode_list,episode_index,provider,False)
else:
    if args.reproduccion_automatica:
        passive = True
    else:
        passive_choice = input("Desea activar la reproducción automática?(y/N): ")
        if passive_choice in ("Yy") and passive_choice!="":
            passive=True
        else:
            passive = False
    watch_video(title,episode_list,episode_index,provider,passive)

