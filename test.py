from animeflv_scraper import Animeflv
import os

api = Animeflv()


print("Que anime quieres ver?:")
possible_anime_id = api.search(input("anime:"))
j=1
for anime in possible_anime_id:
    print(f"[{j}]{anime}")
    j+=1

anime_num = int(input("Selecciona uno:"))-1
anime_id=possible_anime_id[anime_num]
#print(anime_id)
animeinfo = api.anime_info(anime_id)

title = api.anime_title()
status = api.anime_status()
summary = api.anime_summary()
episode_list = api.anime_episodes()

print(f"Título:{title}")
print(f"Estado: {status}")
print(f"Resumen: {summary}")

j=1
for episode in episode_list:
    print(f"[{j}]{episode}")
    j+=1
episode_to_watch = int(input("Enter episode to watch:"))
episode_links = api.get_links(episode_to_watch)
video=episode_links[episode_list[episode_to_watch-1]][0]
os.system(f"mpv ytdl://{video}")