from abc import ABC, abstractmethod
import re
import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import json
import os


# DECORATORS

def log_json(callable):
    def wrapper(*args, **kwargs):
        res: dict = callable(*args, **kwargs)
        with open(f"{callable.__name__}.json", "w") as file:
            file.write(json.dumps(res))
        return res
    return wrapper

def log_text(callable):
    def wrapper(*args, **kwargs):
        res: str = callable(*args, **kwargs)
        with open(f"{callable.__name__}.txt", "w") as file:
            file.write(res)
        return res
    return wrapper


# ABSTRACT CLASSES

class Controller(ABC):
    """Responsible for controlling the application"""

    @abstractmethod
    def run(self) -> None:
        """Runs the application."""
        pass

    @abstractmethod
    def _get_user_date(self) -> str:
        """Gets desired date from user"""
        pass

    @abstractmethod
    def _fetch_song_lists(self, date: str = "YYYY-MM-DD") -> list[str]:
        """Fetches the 100 bests songs of a given date"""
        pass

    @abstractmethod
    def _create_spotify_playlist(self, song_list: list[str]) -> str: 
        """Creates the spotify playlist and returns a link"""
        pass


class Spotify(ABC):
    """Responsible for connecting and managing the spotify api."""

    @abstractmethod
    def create_playlist(self, song_list: list[str]) -> str:
        """Creates a playlist given a list of songs. Returns the link for that playlist."""
        pass


class Billboard(ABC):
    """Responsible for connecting and managing the webscrapping of the billboard application"""

    @abstractmethod
    def _fetch_page(self, date: str) -> str:
        """Fetches the billboard 100 page for a given date"""
        pass

    @abstractmethod
    def _parse_song_names(self, page_html: str) -> list[str]:
        """Given a content page, fetches all the song names and returns them in a list."""
        pass

    def fetch_songs(self, date: str) -> list[str]:
        """Method to be accessed by the controller to fetch the songs list given a date."""
        return self._parse_song_names(page_html=self._fetch_page(date=date))


# IMPLEMENTATIONS

class MyController(Controller):
    """Implementation of the controller class."""

    def __init__(self, billboard: Billboard, spotify: Spotify) -> None:
        self.billboard = billboard
        self.spotify = spotify

    def run(self) -> None:
        """Runs the application."""
        user_date: str = self._get_user_date()
        song_list: list[str] = self._fetch_song_lists(date=user_date)
        playlist_link: str = self._create_spotify_playlist(song_list=song_list, date=user_date)
        print(f"Your desired playlist is in the following link: \n\t {playlist_link}")

    def _get_user_date(self) -> str:
        """Gets desired date from user"""
        user_input: str  = input("Please input a date in the format YYYY-MM-DD: ")

        while not re.match("^[0-9]{4}-[0-9]{2}-[0-9]{2}$", user_input):
            user_input: str  = input("Please input the date in the desired format: ")

        return user_input

    def _fetch_song_lists(self, date: str = "YYYY-MM-DD") -> list[str]:
        """Fetches the 100 bests songs of a given date"""
        return self.billboard.fetch_songs(date=date)

    def _create_spotify_playlist(self, song_list: list[str], date:str) -> str: 
        """Creates the spotify playlist and returns a link"""
        return self.spotify.create_playlist(song_list=song_list, date=date)


class MySpotify(Spotify):
    """Responsible for connecting and managing the spotify api."""

    def __init__(self) -> None:
        self.man = spotify = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                scope="playlist-modify-public",
                redirect_uri="https://example.com",
                client_id=os.environ["SPOTIPY_CLIENT_ID"],
                client_secret=os.environ["SPOTIPY_CLIENT_SECRET"],
                show_dialog=True,
                cache_path="token.txt"
            ),
        )
    
    @log_text
    def create_playlist(self, song_list: list[str], date: str) -> str:
        """Creates a playlist given a list of songs. Returns the link for that playlist."""
        songs_uri: list[str] = [self._get_song_link(song_name=song) for song in song_list]

        playlist_data: dict = self.man.user_playlist_create(user=self.man.me()["id"], name=f"The Best Of   {date}")

        self.man.playlist_add_items(
            playlist_id=playlist_data["id"],
            items=songs_uri
        )

        return playlist_data["external_urls"]["spotify"]

    def _get_song_link(self, song_name: str) -> str:
        """Returns a song link(uri) given a song name."""
        response: dict = self.man.search(q=song_name, limit=1, type="track")
        try:
            song_uri: str = response["tracks"]["items"][0]["uri"]
        except IndexError:
            song_uri: str = "spotify:track:4cOdK2wGLETKBW3PvgPWqT" # this returns "never gonna give you up as exception"

        return song_uri


class MyBillboard(Billboard):
    """Responsible for connecting and managing the webscrapping of the billboard application"""

    def __init__(self, url: str = "https://www.billboard.com/charts/hot-100/") -> None:
        self.base_url: str = url

    def _fetch_page(self, date: str) -> str:
        """Fetches the billboard 100 page for a given date"""
        return requests.get(self.base_url + date).text

    def _parse_song_names(self, page_html: str) -> list[str]:
        """Given a content page, fetches all the song names and returns them in a list."""
        soup: BeautifulSoup = BeautifulSoup(page_html, "html.parser")
        tag_list: list = soup.select(".chart-element__information__song")
        song_names_list: list[str] = list(map(lambda tag: tag.string, tag_list))
        return song_names_list

    def fetch_songs(self, date: str) -> list[str]:
        """Method to be accessed by the controller to fetch the songs list given a date."""
        return self._parse_song_names(page_html=self._fetch_page(date=date))




def main() -> None:
    MyController(
        billboard=MyBillboard(), 
        spotify=MySpotify()
        ).run()

if __name__ == "__main__":
    main()