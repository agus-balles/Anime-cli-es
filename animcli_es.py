#!/usr/sbin/python3

from animeflv_scraper import Animeflv
import os

api = Animeflv()


def watch_video(episode_list, episode_index,provider=0,passive=False):
    episode_links = api.get_links(episode_index+1)
    provider_string = episode_links[episode_list[episode_index]][provider][:14]
    if passive ==True:
        for i in range(len(episode_list)-episode_index):
            episode_links = api.get_links(episode_index+i+1)
            video_links=episode_links[episode_list[episode_index+i]]
            video= [link for link in video_links if provider_string in link][0]
            print(f"Episodio {episode_index+i+1}:\n{video}")
            os.system(f"mpv ytdl://{video}")
    else:
        video_links=episode_links[episode_list[episode_index]]
        video= [link for link in video_links if provider_string in link][0]
        print(f"Episodio {episode_index+1}:\n{video}")
        os.system(f"mpv ytdl://{video}")

        


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
episode_list = api.anime_episodes()

print(f"\033[1;92m \nTítulo: \033[1;0m{title}")
print(f"\033[1;92mEstado: \033[1;0m{status}")
print(f"\033[1;92m \nResumen: \033[1;0m{summary}")

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

passive_choice = input("Desea activar la reproducción automática?(y/N): ")
if passive_choice in ("Yy") and passive_choice!="":
    passive=True
else:
    passive = False
#    video=episode_links[episode_list[episode_index]][provider]
#    os.system(f"mpv ytdl://{video}")

watch_video(episode_list,episode_index,provider,passive)

