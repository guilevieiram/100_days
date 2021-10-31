from bs4 import BeautifulSoup
import requests
from dataclasses import dataclass
from requests_html import HTMLSession

@dataclass
class Arcticle:
    name: str
    link: str
    score: int

    def __repr__ (self) -> str:
        return f"({self.score}) {self.name}  |  {self.link} \n"

    def __gt__ (self, other) -> bool:
        return  self.score > other.score

@dataclass
class Film:
    name: str
    position: int

    def __repr__ (self) -> str:
        return f"{self.position}) {self.name}"

    def __gt__(self, other) -> bool:
        return self.position > other.position

def log(path: str, tag_list: list = [], string_list: list[str] = [] ) -> None:
    content_list: list[str]

    if tag_list:
        content_list = parse_tag_list(tag_list)
    elif string_list:
        content_list = string_list
    with open(path, "w") as file:
        file.write("\n".join(content_list))

def parse_tag_list(tag_list) -> list[str]:
    return list(map(lambda x: x.string, tag_list))

class Scrapper:
    def __init__ (self, document_path: str = None, document_link: str = None, parser: str = "html.parser")  -> None:
        """initializes our scrapper"""

        content: str
        if document_path:
            content = self.load_file(path=document_path)
        elif document_link:
            content = self.download_file(link=document_link)

        self.soup = BeautifulSoup(content, parser)

    def load_file (self, path: str) -> str:
        """Load local html file"""
        with open(path, "r", encoding="utf-8") as file:
            return file.read()

    def download_file (self, link: str) -> str:
        """Download webpage"""
        return requests.get(link).text

    def parce_votes(self) -> list[Arcticle]:
        """Parses the articles on the news page in a list of dataclasses"""
        names: list = list(self.soup.select(".titlelink"))
        scores: list = list(self.soup.select(".score"))
        links: list = list(map(lambda tag: tag["href"], names))

        names = parse_tag_list(names)
        scores = parse_tag_list(scores)
        scores = list(map(lambda x: int(x.replace(" points", "")), scores))
        articles_list: list[Arcticle] = [
            Arcticle(name, link, score)
            for (name, link, score) in zip(names, links, scores)
        ]
        articles_list.sort(reverse=True)
        log("arcticles.txt", string_list=list(map(lambda x: x.__repr__(), articles_list)))
        
        return articles_list


    def find_contents_by_name(self, name: str) -> list:
        content = self.soup.find_all(name=name)
        return list(map(lambda x: x.string, content))

def main() -> None:
    scrapper: scrapper = Scrapper(document_link="https://news.ycombinator.com/news")
    articles_list = scrapper.parce_votes()


if __name__ == "__main__":
    main()
