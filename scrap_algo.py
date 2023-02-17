from bs4 import BeautifulSoup
import requests
import csv
# import pandas as pd


def main():
   for page in range(1, 5):
      # choisir les filtres
      brand = "Mercedes"
      year_min = 2017
      year_max = 2023
      fuel = ""
      url = """https://www.lacentrale.fr/listing?energies={fuel}&makesModelsCommercialNames={brand}&options=&page={page}&yearMax={year_max}&yearMin={year_min}""".format(
      brand=brand,fuel=fuel, page=page, year_min=year_min, year_max=year_max,)

      print("voila l'url :", url, end='\n''\n')


      # Faire une demande GET à l'URL
      response = requests.get(url)

      # Créer un objet BeautifulSoup à partir de la réponse HTML
      soup = BeautifulSoup(response.text, 'html.parser')

      # Trouver tous les éléments dans les searchCard
      elements = soup.find_all(class_='searchCard')   

      # Liste pour stocker les données
      data_scrap = []

      for results in elements:
         brand = results.find("h3")
         model = results.find("h3")
         motor = results.find(class_="Text_Text_text Vehiculecard_Vehiculecard_subTitle Text_Text_body2")
         price = results.find(class_="Text_Text_text Vehiculecard_Vehiculecard_price Text_Text_subtitle2")
         year = results.find(class_="Text_Text_text Vehiculecard_Vehiculecard_characteristicsItems Text_Text_body2")
         fuel = results.find_all(class_="Text_Text_text Vehiculecard_Vehiculecard_characteristicsItems Text_Text_body2")
         if len(fuel) > 3:
            fuel = fuel[3].text
         else:
            fuel = "N/A"      
         mileage = results.find_all(class_="Text_Text_text Vehiculecard_Vehiculecard_characteristicsItems Text_Text_body2")[1]
         
         # split et join
         if results:
            brand_text = brand.text.split()[0]
            model_text = " ".join(model.text.split()[1:])

            print(model.text, motor.text,'\n', "Year : ", year.text,'\n', "Mileage : ", mileage.text,'\n', "Price :", price.text, "Fuel : ", fuel, '\n''\n')
            

            # Convertir les chaînes de caractères en entiers
            price_str = price.text.strip().replace(" ", "").replace("€", "")
            price_int = int(price_str.replace("\xa0",""))
            year_int = int(year.text)
            mileage_str = mileage.text.strip().replace("\xa0", "").replace("km", "")
            mileage_int = int(mileage_str)

            # Ajouter les données converties à la liste data_scrap
            data_scrap.append([brand_text, model_text, motor.text, year_int, price_int, fuel, mileage_int])

         

      # Écrire les données dans un fichier CSV
      with open("mercedes.csv", "w") as fd:
         writer = csv.writer(fd)
         writer.writerow(["brand" ,"model", "motor", "year", "price", "fuel", "mileage"]) # Écrire les en-têtes
         for row in data_scrap:
            writer.writerow(row)


if __name__ == "__main__" :
   main()
