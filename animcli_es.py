from animeflv_scraper import Animeflv
import os
from colorama import Fore

api = Animeflv()


print("Que anime quieres ver?")
possible_anime_id = api.search(input("Anime:\033[1;36m"))
j=1
print("\nResultados:\n")
for anime in possible_anime_id:
    print(f"[{j}]{anime}")
    j+=1

anime_num = int(input("\033[1;0mSelecciona uno:"))-1
anime_id=possible_anime_id[anime_num]
#print(anime_id)
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

episode_to_watch = int(input("\nSelecciona que episodio ver:"))
episode_links = api.get_links(episode_to_watch)

video_links=episode_links[episode_list[episode_to_watch-1]]
print("\033[1;0m\nElige un proveedor: \033[1;36m")
j=1
for provider in video_links:
    print(f"[{j}]{provider}")
    j+=1
video=episode_links[episode_list[episode_to_watch-1]][int(input("Proveedor: "))-1]
os.system(f"mpv ytdl://{video}")
