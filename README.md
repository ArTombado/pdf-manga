# pdf-manga

Um script feito em python para fazer download de mangás através do [mangayabu](https://mangayabu.top/) e converte-los para pdf.

## Instalação

```bash
git clone https://github.com/ArTombado/pdf-manga
cd pdf-manga
pip3 install -r requirements.txt
```

## Uso

```bash
python3 pdf-manga.py --path path/to/folder --make_folder
```

```--path path```: Se usado, os mangás vão ser enviados para o diretório especificado, se não for usado os mangás vão ser enviados para o diretório atual.

```--make_folder```: Se usado, o script vai fazer uma pasta com o nome do mangá para colocar os pdfs.

Após rodar o script, o programa vai perguntar qual mangá você quer baixar

Exemplo:
```
Qual mangá você quer baixar? kimetsu no yaiba
(0): Kimetsu no Yaiba
(1): Kimetsu no Yaiba: Rengoku Kyoujurou Gaiden
(2): Kimetsu no Yaiba: Tomioka Giyuu Gaiden
```
Se o mangayabu tiver algum mangá relacionado ao nome que você colocou, o programa vai mostrar todos os resultados da pesquisa.

Selecione um dos resultados da lista com o numero em parênteses

Após selecionar o mangá que você quer, o programa vai mostrar uma lista com todos os capítulos do mangá, para escolher os capítulos escolha um dos seguintes formatos:

```x```: Baixa o capitulo do numero em parênteses x.

Exemplo:
```10``` Baixa o capitulo 10. 

```x,y,z```: Baixa os capítulos entre virgulas(x, y e z).

Exemplo:
```4,8,15,16```  Baixa os capitulos 4, 8, 15 e 16 .

```x-y```: Baixa do capitulo x até o capitulo y.

Exemplo:
```23-42``` Baixa do capitulo 23 até o capitulo 42.

```todos```: Baixa todos os capítulos disponíveis.

```
(0): Kimetsu no Yaiba #01
(1): Kimetsu no Yaiba #02
(2): Kimetsu no Yaiba #03
(3): Kimetsu no Yaiba #04
(4): Kimetsu no Yaiba #05
...
Selecione o(s) capitulo(s) que você quer baixar(utilize o numero em parenteses): 0-3
```
Após selecionar os capítulos, o programa vai baixar todos os capítulos selecionados e vai converte-los para pdf.

OBS: Em alguns casos o mangayabu aparece como se tivesse o capítulo mas não tem as imagens do capítulo, nesses casos o programa vai ignorar e passar para o próximo capítulo, então sempre fique atento para a numeração dos capítulos que você lê para não pular nenhum capítulo!

# Doações

Aceito doações nas criptomoedas [bitcoin](https://bitcoin.org/) e [nano](https://nano.org/):

BITCOIN: bc1pfe5yj7kp28shfaph5y2ejf0787cnng3r2tkj85h6xfr3kfqxd0fqa0s0jk  

NANO: nano_3o5s1nq7ao39y9w1o45brbamp7ksm8m8heh8y8oe71ta7qkq56ys5fjtrykq
