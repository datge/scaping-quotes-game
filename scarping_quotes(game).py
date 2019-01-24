from bs4 import BeautifulSoup
import requests
from csv import writer, reader, DictReader
import random
def elaborate_csv():
    with open("scarping_quotes.csv", "w", encoding="utf-8", newline='') as file_object :
        csv_writer = writer(file_object)
        csv_writer.writerow(["autore", "frase","link_autor"])
        page = 1
        while True:

            pagina = "http://quotes.toscrape.com/page/{}/".format(page)
            response = requests.get(pagina)
            soup = BeautifulSoup(response.text, "html.parser")

            quotes = soup.find_all(class_="quote")

            for quote in quotes:
                quote_tag = quote.find_all("span")

                frase = quote_tag[0].get_text().strip()
                autore = quote_tag[1].get_text()
                autore = autore[3:-8].strip()

                link_autori= quote_tag[1].find("a")["href"]
                # print(link_autori)
                # print(frase)
                # print(autore)
                csv_writer.writerow([autore,frase,link_autori])
            
      
            page = page +1
            # print(page)

            if (soup.find_all(class_="next")) == [] :
                break
                quit()
def get_biografie(pagina_autore):
    response =  requests.get(pagina_autore)
    soup = BeautifulSoup(response.text, "html.parser")
    born_date = soup.find(class_ = 'author-born-date').get_text()
    born_place = soup.find(class_ = 'author-born-location').get_text()
    biografie = soup.find(class_='author-description').get_text().strip()

    return born_date, born_place, biografie


elaborate_csv()
yes = True
while yes:

    with open('scarping_quotes.csv', 'r', encoding="utf-8") as file_object:
        csv_reader = reader(file_object)
        csv_reader = list(csv_reader)
        random_quote = random.randint(2,101)
        print(csv_reader[random_quote][0]) #for debugging
        print(csv_reader[random_quote][1])

        pagina_biografia = "http://quotes.toscrape.com" + csv_reader[random_quote][2]
        born_date, born_place, _ = get_biografie(pagina_biografia)
        
      
        attemps = 1
        while attemps <=4:
            indovinando = input("\nWho wrote that ?? : ")
            if indovinando == csv_reader[random_quote][0]:
                print("Complimenti hai indovinato\n")
                break
            else :
                print("\nYou wrong :'( ")
                if attemps == 1 :
                    print("The first letter of the name is: " + csv_reader[random_quote][0][0])
                elif attemps == 2 : 
                    print("The first two letter of the nam are: " + csv_reader[random_quote][0][:2])
                elif attemps == 3 : 
                    print("Born: "+ born_date,born_place)

            attemps  = attemps + 1
        yes = input("\nDo you wanna try again? y/n ")
        if yes == 'n':
            yes = False

        
            



