import requests
import re

#Uncomment all lines and comment the previous one to each to switch the page from m.animeflv.net tp www1.animeflv.ws in case it gets blocked

class Animeflv(object):

    def search(self,query):

        http = requests.get(f"https://m.animeflv.net/browse?q={query}").text
        #http = requests.get(f"https://www1.animeflv.ws/browse?q={query}").text
        matches=re.findall(r"a href=['\"]\/anime\/(.*?)['\"]",http)
        return matches

    def anime_info(self,anime_id):
        
        http= requests.get(f"https://m.animeflv.net/anime/{anime_id}").text
        #http= requests.get(f"https://www1.animeflv.ws/anime/{anime_id}").text
        try:
            self.title=re.findall(r"h1 class=\"Title\"[>](.*?)[<]",http)[0]
            #self.title=re.findall(r"h2 class=\"Title\"[>](.*?)[<]",http)[0]
        except:
            self.title=anime_id
        try:
            self.status=re.findall(r'<p><strong>Estado:<\/strong> <strong class="[^"]*">(.*?)<\/strong>',http)[0]
            #self.status=re.findall(r'<p class="AnmStts "><span class="fa-tv">([^<]+)</span></p>',http)[0]
        except:
            self.status="Not Found"
        try:
            self.summary=re.findall(r"<p><strong>Sinopsis:<\/strong>([\s\S]*?)<",http)[0]
            #self.summary=re.findall(r"div class=\"Description\"[>](.*?)[<]",http)[0]
        except:
            self.summary="Not Found"
        self.episodes=re.findall(r'href="/ver/([^"]+)"',http)
        #self.episodes=[anime_id + episode for episode in (re.findall(fr'href="/{anime_id}([^"]+)"',http))][::-1]
    

    def get_links(self,episode_to_watch):
        episode = self.episodes[episode_to_watch-1]
        episode_links = {}
        http_fragment = requests.get(f"https://m.animeflv.net/ver/{episode}").text
        #http_fragment = requests.get(f"https://www1.animeflv.ws/{episode}").text

        url_pattern = r"https:\\\/\\\/ok.ru\\\/videoembed\\\/.*?\"|https:\\\/\\\/www.yourupload.com\\\/embed\\\/.*?\"|https:\\\/\\\/streamwish.to\\\/e\\\/.*?\""
        #url_pattern = r"https:\/\/ok.ru\/videoembed\/.*?\"|https:\/\/www.yourupload.com\/embed\/.*?\"|https:\/\/streamwish.to\/e\/.*?\"|https:\/\/wishembed.pro\/e\/.*?\""

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

