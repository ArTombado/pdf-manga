import requests.packages.urllib3.util.connection 
import requests, re, aiohttp, asyncio, io, json

from bs4    import BeautifulSoup
from socket import AF_INET
from PIL    import Image
from util   import clear

# force ipv4
requests.packages.urllib3.util.connection.allowed_gai_family = lambda: AF_INET

REGEX_MULTIPLE_CHAPTERS = "^(\d+,?)+$"
REGEX_RANGE_CHAPTERS = "(\d+)-(\d+)"

def list_mangas(manga_name):
    manga_list = []

    all_mangas = requests.get("https://mangayabu.top/api/show3.php")

    if( all_mangas.ok ):
        all_mangas_json = all_mangas.json()

        for manga in all_mangas_json:
            if( manga_name.lower() in manga["title"].lower() ):
                manga_list.append(manga)
    else:
        return None

    return manga_list

def list_manga_chapters(manga_link):
    manga_chapters = requests.get(manga_link)

    if( manga_chapters.ok ):
        soup = BeautifulSoup(manga_chapters.text, "html.parser")

        chapters_list = json.loads(soup.find_all("script", attrs={"id":"manga-info"})[0].contents[0])['allposts']

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
    page = requests.get(url)
    images_url = []

    if( page.ok ):
        soup = BeautifulSoup(page.text, "html.parser")

        for script in soup.find_all("script"):
            if( script.contents and "hatsuna" in script.contents[0] ):
                vars = script.contents[0].replace("var", "").replace(" ", "").replace("true", "True").split(";")[:-1]
                vars = {var.split("=")[0]: var.split("=")[1] for var in vars}
                break

        images_api = requests.get("https://mangayabu.top/chapter.php", params = {"id": vars["hash"], "hatsuna": vars["hatsuna"]})

        if( images_api.ok ):
            images_url = images_api.json()["Miko"]
        else:
            return None

    else:
        return None

    return images_url

async def get_chapter_image(session, url, manga_title, chapter_title, progress_bar_images, progress_bar_chapters):
    r = await session.get(url)
    content = await r.read()

    try:
        i = Image.open(io.BytesIO(content))
        i.load()
        i = i.convert("RGB")
    except:
        return None

    clear()

    progress_bar_images.add()

    print(f"Baixado: {url}")
    progress_bar_images.show()
    print(f"Capitulo: {manga_title} #{chapter_title}")
    progress_bar_chapters.show()

    return i

async def get_chapter_images(images, manga_title, chapter_title, progress_bar_images, progress_bar_chapters):
    session = aiohttp.ClientSession()

    tasks = [asyncio.ensure_future(get_chapter_image(session, image, manga_title, chapter_title, progress_bar_images, progress_bar_chapters)) for image in images]

    r = await asyncio.gather(*tasks)

    await session.close()

    images = [e for e in r if( e != None )]

    return images
