from bs4 import BeautifulSoup as bs
from playwright.sync_api import sync_playwright

class Scraper_Master():
    def __init__(self,arquivo):
        self.arquivo = arquivo
        self.arquivo.write("nome,posicao,nascionalidade,idade,clube,melhor_marca_da_carreira,ultima_alteracao,valor_de_mercado\n")

        self.cont = 1

    def scraper(self,link):
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(link)
            conteudo = page.content()
            page.close()
        return conteudo
    

    def start(self):
        print(f"Iniciando o arquivo {self.arquivo.name}")
        print("Fazendo Scrap da pagina 1 do site")
        fist_scrap = self.scraper("https://www.transfermarkt.com.br/campeonato-brasileiro-serie-a/marktwerte/wettbewerb/BRA1/ajax/yw1/pos//detailpos/0/altersklasse/alle/plus/1")
        scrap = bs(fist_scrap,'html.parser')
        self.scrap_jogadores(fist_scrap)
        a = scrap.find_all("li", {"class":"tm-pagination__list-item tm-pagination__list-item--icon-last-page"})[0].find("a").get("href").split("/")
        for i in range(2,int(a[-1])+1):
            link_base = "/".join(a[:-1])
            print(f"Fazendo Scrap da Pagina {i} do site")
            print("https://www.transfermarkt.com.br"+link_base+"/"+str(i))
            self.scrap_jogadores(self.scraper("https://www.transfermarkt.com.br"+link_base+"/"+str(i)))
            print("#"*25)
            print(f"Arquivo {self.arquivo.name} foi terminado.")
    def scrap_jogadores(self,scrap_content):
        scrap = bs(scrap_content,'html.parser')
        jogadores = scrap.find_all("tbody")[1].find_all("tr")
        infos = [info.find_all("td") for info in jogadores]
        print(f"separando dados e escrevendo no {self.arquivo.name}")
        for filter in infos:
            if len(filter) == 11:
                nome = filter[1].find_all("a")[0].text
                posicao = filter[1].find_all("td")[2].text
                nacionalidade = filter[5].find("img").get("title")
                idade = filter[6].text
                clube = filter[7].find("a").get("title")
                melhor_marca_da_carreira = filter[8].text
                ultima_alteracao = filter[9].text
                valor_de_mercado = filter[10].find("a").text
                self.arquivo.write(f"{self.cont}-{nome},{posicao},{nacionalidade},{idade},{clube},{melhor_marca_da_carreira},{ultima_alteracao},{valor_de_mercado}\n")
                self.cont +=1
            else:
                continue

file = open('Jogadores.txt',"w")
Scraper_Master(file).start()
file.close()