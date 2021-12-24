import requests.packages.urllib3.util.connection 
import requests, urllib, re, random, aiohttp, asyncio, io

from bs4    import BeautifulSoup
from socket import AF_INET
from PIL    import Image
from util   import clear

# force ipv4
requests.packages.urllib3.util.connection.allowed_gai_family = lambda: AF_INET

REGEX_MULTIPLE_CHAPTERS = "^(\d+,?)+$"
REGEX_RANGE_CHAPTERS = "(\d+)-(\d+)"

def list_mangas(manga_name):
    manga_name = urllib.parse.quote(manga_name)
    manga_list = []

    manga_list_page = requests.get(f"https://mangayabu.top/?s={manga_name}")

    if( manga_list_page.ok ):
        soup = BeautifulSoup(manga_list_page.text, "html.parser")

        for a in soup.find_all("a"):
            if( a.get("href", "").startswith("https://mangayabu.top/manga/") ):
                manga_list.append(a)
    else:
        return None

    return manga_list

def list_manga_chapters(manga_link):
    manga_chapters = requests.get(manga_link)
    chapters_list = []

    if( manga_chapters.ok ):
        soup = BeautifulSoup(manga_chapters.text, "html.parser")

        for a in soup.find_all("a"):
            if( a.get("href", "").startswith("https://mangayabu.top/ler/") ):
                chapters_list.append(a)

        chapters_list.reverse()
    else:
        return None

    return chapters_list

def get_manga_selection(chapters_list, selection):

    to_install = []

    if( re.search(REGEX_MULTIPLE_CHAPTERS, selection) ):
        splited = selection.split(",")

        if( max([int(s) for s in splited]) > len(chapters_list) - 1 ):
            return None

        for n in splited:
            to_install.append(chapters_list[int(n)])

    elif( re.search(REGEX_RANGE_CHAPTERS, selection) ):
        splited = selection.split("-")

        if( int(splited[0]) < 0 or int(splited[1]) > len(chapters_list) - 1 ):
            return None

        to_install = chapters_list[int(splited[0]):int(splited[1]) + 1]

    elif( selection == "todos" ):
        to_install = chapters_list

    else:
        return None

    return to_install

def get_chapter_images_url(url):
    page = requests.get(f"{url}?cachebuster={random.random()}")
    images_url = []

    if( page.ok ):
        soup = BeautifulSoup(page.text, "html.parser")

        for img in soup.find_all("img"):
            if( img.get("class") ):
                objclass = img.get("class")
                chapter_images = soup.find_all('img', attrs = {'class': objclass})
                images_url = [image["src"] for image in chapter_images]
                break

    else:
        return None

    return images_url

async def get_chapter_image(session, url, chapter_title, progress_bar_images, progress_bar_chapters):
    r = await session.get(url)
    content = await r.read()

    try:
        i = Image.open(io.BytesIO(content))
        i.load()
    except:
        return None

    clear()

    progress_bar_images.add()

    print(f"Baixado: {url}")
    progress_bar_images.show()
    print(f"Capitulo: {chapter_title}")
    progress_bar_chapters.show()

    return i

async def get_chapter_images(images, chapter_title, progress_bar_images, progress_bar_chapters):
    session = aiohttp.ClientSession()

    tasks = [asyncio.ensure_future(get_chapter_image(session, image, chapter_title, progress_bar_images, progress_bar_chapters)) for image in images]

    r = await asyncio.gather(*tasks)

    await session.close()

    images = []

    for e in r:
        if( e ):
            images.append(e)

    return images