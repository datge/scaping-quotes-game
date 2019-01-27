from bs4 import BeautifulSoup
import requests
from csv import writer, reader, DictReader
import random
from time import sleep

# scaping function
def elaborate_csv():
    with open("scarping_quotes.csv", "w", encoding="utf-8", newline='') as file_object:
        csv_writer = writer(file_object)
        csv_writer.writerow(["autore", "frase", "link_autor"])
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

                link_autori = quote_tag[1].find("a")["href"]
                # print(link_autori)
                # print(frase)
                # print(autore)
                csv_writer.writerow([autore, frase, link_autori])

            page = page + 1
            # print(page)
            # break the infinite loop if there aren't enoymore pages lefts after the current one
            if (soup.find_all(class_="next")) == []:
                break
                quit()

# function for get biografie of autor up to the link saved in the csv
def get_biografie(pagina_autore):
    response = requests.get(pagina_autore)
    soup = BeautifulSoup(response.text, "html.parser")
    born_date = soup.find(class_='author-born-date').get_text()
    born_place = soup.find(class_='author-born-location').get_text()
    biografie = soup.find(class_='author-description').get_text().strip()

    return born_date, born_place, biografie


elaborate_csv() # calling the function for scraping

yes = True
punteggio = 0
while yes:

    with open('scarping_quotes.csv', 'r', encoding="utf-8") as file_object:
        csv_reader = reader(file_object)
        csv_reader = list(csv_reader)
        random_quote = random.randint(2, 101)
        # print(csv_reader[random_quote][0]) #for debugging
        print(csv_reader[random_quote][1])

        pagina_biografia = "http://quotes.toscrape.com" + csv_reader[random_quote][2]
        born_date, born_place, _ = get_biografie(pagina_biografia)
        attemps = 1
        while attemps <= 4: # let the user try again for 4 times
            indovinando = input("\nWho wrote that ?? : ")
            if indovinando.lower() == csv_reader[random_quote][0].lower():
                punteggio = punteggio + 1
                print("Complimenti hai indovinato( Score :{} )\n".format(punteggio))
                break
            else:
                print("\nYou wrong :'( ")
                if attemps == 1:
                    print("The first letter of the name is: " + csv_reader[random_quote][0][0])
                elif attemps == 2:
                    last_name_inital = csv_reader[random_quote][0].split(' ')[-1][0]
                    print(f"The first letter or the name and last name are:  {csv_reader[random_quote][0][0]} {last_name_inital}")
                elif attemps == 3:
                    print("Born: " + born_date, born_place)
                elif attemps == 4:
                    print(f"The answer was: {csv_reader[random_quote][0]}")

            attemps = attemps + 1
        yes = input("\nDo you wanna try again? y/n ") # if n the game end, print the score, and wait 5 secs before close the cmd
        if yes == 'n':
            print("Il tuo punteggio finale è : {}".format(punteggio))
            sleep(5)
            yes = False
