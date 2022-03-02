import asyncio, pathvalidate, os, argparse

from functions import *

path = ""

parser = argparse.ArgumentParser()
parser.add_argument("--path", type = lambda x: x if os.path.exists(x) else "")
parser.add_argument("--make_folder", action = "store_true")
options = parser.parse_args()

if( options.path == "" ):
    print("O diretorio que você colocou é invalido ou não existe. Fechando o programa...")
    exit()

if( options.path ):
    path = options.path

print("Bem vindo ao pdf-manga, aqui você poderá baixar uma diversidade de mangás em pdf utilizando o site https://mangayabu.top.")
print("Para cancelar alguma operação apenas aperte enter sem digitar nada.")
print()
print("Aceito doações nas criptomoedas BITCOIN e NANO")
print("BITCOIN: bc1pfe5yj7kp28shfaph5y2ejf0787cnng3r2tkj85h6xfr3kfqxd0fqa0s0jk")
print("NANO: nano_3o5s1nq7ao39y9w1o45brbamp7ksm8m8heh8y8oe71ta7qkq56ys5fjtrykq")
print()

manga_name = input("Qual mangá você quer baixar? ")

if( manga_name == "" ):
    print("Fechando o programa...")
    exit()

manga_list = list_mangas(manga_name)

if( manga_list == None ):
    print("Não foi possivel acessar o mangayabu corretamente, fechando o programa...")
    exit()
elif( manga_list == [] ):
    print("Não foi possivel encontrar este mangá.")
    exit()

print("\n".join(tuple(f"({n}): {manga['title']}" for n, manga in enumerate(manga_list))))

manga_number = input("Escolha qual desses mangás você quer baixar(digite o numero em parenteses): ")

if( manga_number == "" ):
    print("Fechando o programa...")
    exit()

try:
    manga = manga_list[int(manga_number)]
except:
    print(f"A opção \"{manga_number}\" não é valida.")
    exit()

chapters_list = list_manga_chapters(f"https://mangayabu.top/manga/{manga['slug']}")

if( chapters_list == None ):
    print("Não foi possivel acessar o mangayabu corretamente, fechando o programa...")
    exit()

print("\n".join(tuple(f"({n}): {manga['title']} #{chapter['num']}" for n, chapter in enumerate(chapters_list))))

chapter_number = input("Selecione o(s) capitulo(s) que você quer baixar(utilize o numero em parenteses): ")

if( manga_number == "" ):
    print("Fechando o programa...")
    exit()

to_install = get_manga_selection(chapters_list, chapter_number)

if( to_install == None ):
    print("O formato que você usou para pegar os capitulos é invalido. Fechando o programa...")
    exit()

if( options.make_folder ):
    os.mkdir(os.path.join(path, pathvalidate.sanitize_filepath(manga['title'])))

asyncio.get_event_loop().run_until_complete(get_chapters(to_install, manga["title"], options.make_folder, path))

print("Todos os mangás foram baixados com sucesso!")