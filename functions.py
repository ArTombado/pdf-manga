import requests.packages.urllib3.util.connection 
import requests, re, aiohttp, asyncio, io, json, pathvalidate, os, shutil, gc, time

from bs4    import BeautifulSoup
from socket import AF_INET
from PIL    import Image
from util   import *

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

        chapters_list_names = []
        chapters_list_final = []

        for chapter in chapters_list:
            if( chapter["num"] in chapters_list_names ): continue

            chapters_list_names.append(chapter["num"])
            chapters_list_final.append(chapter)
    else:
        return None

    return chapters_list_final

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

        image_id = 0

        while( soup.find_all("img", attrs={"id": str(image_id)}) != [] ):
            images_url.append(soup.find_all("img", attrs={"id": str(image_id)})[0]["data-src"])
            image_id += 1

    else:
        return None

    return images_url

async def get_chapter_image(session, url, manga_title, chapter_title, path, make_folder, progress_bar_images_dict):
    r = await session.get(url)
    content = await r.read()

    dir_name = pathvalidate.sanitize_filepath(os.path.join(path, manga_title if( make_folder ) else "", "temp", chapter_title, url.split("/")[-1]), platform = "auto")

    try:
        i = Image.open(io.BytesIO(content))
        i.load()
        i = i.convert("RGB")
    except:
        return None

    i.save(dir_name)

    del i

    gc.collect()

    progress_bar_images_dict[f"{manga_title} #{chapter_title}"].add()

    return dir_name

async def get_chapter_images(session, images, manga_title, chapter_title, make_folder, path, progress_bar_images_dict, progress_bar_chapters):

    os.mkdir(os.path.join(path, manga_title if( make_folder ) else "", "temp", chapter_title))

    tasks = tuple(asyncio.ensure_future(get_chapter_image(session, image, manga_title, chapter_title, path, make_folder, progress_bar_images_dict)) for image in images)

    r = await asyncio.gather(*tasks)

    images = tuple(e for e in r if( e != None ))

    progress_bar_chapters.add()

    return images

async def get_chapters(chapters_list, manga_title, make_folder, path):
    session = aiohttp.ClientSession()

    os.mkdir(os.path.join(path, manga_title if( make_folder ) else "", "temp"))

    tasks = []

    progress_bar_chapters = ProgressBar(len(chapters_list))
    chapters_filenames = []

    for i in range(0, len(chapters_list), 5):
        images_bars = {}

        for chapter in chapters_list[i : i + 5]:

            images = get_chapter_images_url(chapter["id"])

            if( images ):
                images_bars[f"{manga_title} #{chapter['num']}"] = ProgressBar(len(images))

                tasks.append(asyncio.ensure_future(get_chapter_images(session, images, manga_title, chapter["num"], make_folder, path, images_bars, progress_bar_chapters)))

        results = await asyncio.gather(*(tasks[i : i + 5]), asyncio.ensure_future(print_bars(tasks[i : i + 5], progress_bar_chapters, images_bars)))
        chapters_filenames += results[:-1]

        time.sleep(10)

    await session.close()

    gc.collect()

    clear()

    progress_bar_pdfs = ProgressBar(len(chapters_filenames))

    for n, filenames in enumerate(chapters_filenames):
        pdf = tuple(Image.open(filename) for filename in filenames)

        pdf[0].save(f"{os.path.join(path, pathvalidate.sanitize_filepath(manga_title) if( make_folder ) else '', pathvalidate.sanitize_filename('{} #{}'.format(manga_title, chapters_list[n]['num'])))}.pdf", save_all = True, append_images = pdf[1:])

        del pdf
        gc.collect()

        progress_bar_pdfs.add()

        clear()

        print("Gerando pdfs...")
        print(f"Progresso: {progress_bar_pdfs.show()}")

    shutil.rmtree(os.path.join(path, manga_title if( make_folder ) else "", "temp"))

    clear()

async def print_bars(tasks, progress_bar_chapters, progress_bar_images_dict):
    while( True ):
        clear()

        for chapter in progress_bar_images_dict:
            print(f"{chapter}: {(max([len(c) for c in progress_bar_images_dict]) - len(chapter)) * ' '}{progress_bar_images_dict[chapter].show()}")

        print()

        print(f"Progresso: {progress_bar_chapters.show()}")

        if( all([task.done() for task in tasks]) ): break

        await asyncio.sleep(5)
