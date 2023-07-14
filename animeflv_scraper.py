import requests
import re
from bs4 import BeautifulSoup
class Animeflv(object):

    def search(self,query):

        http = requests.get(f"https://m.animeflv.net/browse?q={query}").text
        matches=re.findall(r"href=['\"]\/anime\/(.*?)['\"]",http)
        return matches

    def anime_info(self,anime_id):
        
        http= requests.get(f"https://m.animeflv.net/anime/{anime_id}").text
        try:
            self.title=re.findall(r"h1 class=\"Title\"[>](.*?)[<]",http)[0]
        except:
            self.title=anime_id
        try:
            self.status=re.findall(r'<p><strong>Estado:<\/strong> <strong class="[^"]*">(.*?)<\/strong>',http)[0]
        except:
            self.status="Not Found"
        try:
            self.summary=re.findall(r"<p><strong>Sinopsis:<\/strong>([\s\S]*?)<",http)[0]
        except:
            self.summary="Not Found"
        self.episodes=re.findall(r'href="/ver/([^"]+)"',http)
    

    def get_links(self,episode_to_watch):
        episodes = self.episodes[episode_to_watch-1]
        episode_links = {}
        if type(episodes)==str:
            http_fragment = requests.get(f"https://m.animeflv.net/ver/{episodes}").text
            url_pattern = r"https:\\\/\\\/ok.ru\\\/videoembed\\\/.*?\"|https:\\\/\\\/www.yourupload.com\\\/embed\\\/.*?\""

            links = re.findall(url_pattern, http_fragment)
            for i in range(len(links)):
                links[i] = links[i].replace("\\","").strip('"')
                episode_links[episodes] = links            
        else:
            for episode in episodes:
                http_fragment = requests.get(f"https://m.animeflv.net/ver/{episode}").text
                url_pattern = r"https:\\\/\\\/ok.ru\\\/videoembed\\\/.*?\"|https:\\\/\\\/www.yourupload.com\\\/embed\\\/.*?\""

                links = re.findall(url_pattern, http_fragment)
                for i in range(len(links)):
                    links[i] = links[i].replace("\\","").strip('"')
                    episode_links[episode] = links
        return episode_links
    
    def anime_title(self):
        return self.title

    def anime_status(self):
        return self.status
    
    def anime_summary(self):
        return self.summary
    
    def anime_episodes(self):
        return self.episodes

