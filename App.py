
from distutils.log import info
from logging import _STYLES
import numpy as np
import io
from flask import Flask, render_template, request,send_file,make_response
from selenium import webdriver 
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.webdriver.support.ui import Select
import time
import datetime
import sys
sys.stdout.reconfigure(encoding='utf-8')
from tqdm import tqdm
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from MyFunctions import *


app = Flask(__name__,template_folder='templates', static_folder='templates/styles')

# Définir les parametres par défaut :

filtres = ['assist', 'techni', 'conseil', 'etud', 'developp','informati', 'digita', 'data', 'analys', 'strat', 'optimis', 'cloud','logiciel', 'solut', 'plateform']
executable_path = "C:\Program Files\Google\Chrome\Application\chromedriver.exe"

# créer la dataframe :

d = pd.DataFrame()

@app.route('/')
def index():
   return render_template("index.html")

@app.route('/change-path',methods = ['POST'])
def path():
   global filtres
   global executable_path
   if request.method == 'POST':
      # collecter les inputs
      thisform = request.form
      thisdict = thisform.to_dict(flat=True)
      if thisdict['driver'] != "":
         executable_path = thisdict['driver']
         out1 = "your path is\n" + executable_path
      elif thisdict['driver'] == "":
         out1=" "
         executable_path = "C:\Program Files\Google\Chrome\Application\chromedriver.exe"

      if thisdict['filtre'] != "":
         filtres0 = thisdict['filtre']
         out2 ="\n Vous avez choisi les filtres suivants :\n" + filtres0
         filtres1 = preprocessor(filtres0)
         filtres = filtres1.split(" ")
      elif thisdict['filtre'] == "":
         filtres = ['assist', 'techni', 'conseil', 'etud', 'developp','informati', 'digita', 'data', 'analys', 'strat', 'optimis', 'cloud','logiciel', 'solut','plateform']
         out2= "Vous avez choisi d'utiliser les filtres par défaut"
      
   return render_template('display.html',out1 =out1 ,out2 = out2)

@app.route('/',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      service = Service(executable_path=executable_path)
      driver = webdriver.Chrome(service=service)
      heading = ['Procédure\nCatégorie\nPublié le',
               'Référence\nObjet\nAcheteur public',
               "Lots\nLieu d'exécution",
               'Date limite de remise des plis']

      # charger chaque secteur
      def firstly(secteur):
         driver.get("https://www.marchespublics.gov.ma/pmmp/?lang=fr")
         driver.find_element(By.LINK_TEXT, 'Services').click()
         time.sleep(5)
         driver.find_element(By.LINK_TEXT, secteur).click()
         select = Select(driver.find_element(By.ID,"ctl0_CONTENU_PAGE_resultSearch_listePageSizeTop"))
         select.select_by_value('500') 
         return
      
      # extraire les elements
      def loadsect(secteur):  
         data = []
         liens = []
         for tr in driver.find_elements(By.XPATH,"/html/body/form/div[3]/div[2]/div[1]/div[5]/div[1]/div[2]/div[2]/table/tbody"):
            tds = tr.find_elements(By.TAG_NAME,'td')
            for b in tr.find_elements(By.CLASS_NAME,"actions"):
               for a in b.find_elements(By.TAG_NAME, 'a'):
                  liens.append(a.get_attribute('href'))
            if tds: 
               data.append([td.text for td in tds])
         
         data1 = flatten(data)
         data2 = compact(data1)
         n = 4
         data4 = pd.DataFrame ([data2[i:i + n] for i in range(0, len(data2), n)], columns = heading)
         data4['Consultation']= liens[::11]

         print(len(data4)) 
         #data4.to_excel(secteur +'.xlsx', index = False)

         return data4

      # la fonction globale :
      def scrap(secteur):  
         firstly(secteur)

         time.sleep(3)
         l = loadsect(secteur)
         print(secteur,': Done')
         return l
      
      # Extraire les différents secteurs : service
      driver.get("https://www.marchespublics.gov.ma/pmmp/?lang=fr")
      try:
         driver.find_element(By.LINK_TEXT, 'Services').click()
      finally:
         secteurs = []
         for tr in driver.find_elements(By.XPATH,"/html/body/div/div/div[3]/div[2]/div[3]/div[2]/div/div[3]/div/table/tbody"):
            tds = tr.find_elements(By.TAG_NAME,'td')
            if tds:
                  secteurs.append(td.text for td in tds)

      secteurs1 = flatten(secteurs)
      n = 2
      secteurs2 = [secteurs1[i:i + n] for i in range(0, len(secteurs1), n)]
      secteurs3 = pd.DataFrame (secteurs2, columns = ['Secteur','Nombre'])

      # extraire et concatiner les tableaux
      d=scrap(secteurs3['Secteur'][0])
      for secteur in secteurs3['Secteur'][1:]:
         p=scrap(secteur)
         d = pd.concat([d,p],ignore_index=True)

      driver.close()
      print('All Done :) ')
      d.to_excel('notGlobalTable.xlsx', index = False)

      d[['Procédure','Catégorie','Publié le']] = d['Procédure\nCatégorie\nPublié le'].str.split('\n', expand=True)
      d[['Référence','Objet','Acheteur public']] = d['Référence\nObjet\nAcheteur public'].str.split('\n', expand=True)
      d[['Date limite de remise des plis','heure']] = d['Date limite de remise des plis'].str.split('\n', expand=True)
         
      D = pd.concat([d['Consultation'],
      d[['Procédure','Catégorie','Publié le']] , 
      d[['Référence','Objet','Acheteur public']], 
      d["Lots\nLieu d'exécution"], 
      d[['Date limite de remise des plis','heure']]],axis=1)
      print(len(D)) 

      # D.to_excel('GlobalTable.xlsx', index = False)

      print("ALL DONE")

      Sheet1=D
      Sheet1_columns = [col for col in Sheet1.columns if col != 'Procédure']
      Sheet1_columns.insert(0, 'Procédure')
      Sheet1 = Sheet1[Sheet1_columns]
      Sheet1_columns = [col for col in Sheet1.columns if col != 'Publié le']
      Sheet1_columns.insert(8, 'Publié le')
      Sheet1 = Sheet1[Sheet1_columns]
      Sheet1_columns = [col for col in Sheet1.columns if col != 'heure']
      Sheet1_columns.insert(8, 'heure')
      Sheet1 = Sheet1[Sheet1_columns]
      Sheet1_columns = [col for col in Sheet1.columns if col != 'Catégorie']
      Sheet1_columns.insert(0, 'Catégorie')
      Sheet1 = Sheet1[Sheet1_columns]
      Sheet1_columns = [col for col in Sheet1.columns if col != "Lots\nLieu d'exécution"]
      Sheet1_columns.insert(6, "Lots\nLieu d'exécution")
      Sheet1 = Sheet1[Sheet1_columns]
      Sheet1_columns = [col for col in Sheet1.columns if col != 'Référence']
      Sheet1_columns.insert(2, 'Référence')
      Sheet1 = Sheet1[Sheet1_columns]
      Sheet1_columns = [col for col in Sheet1.columns if col != 'Date limite de remise des plis']
      Sheet1_columns.insert(8, 'Date limite de remise des plis')
      Sheet1 = Sheet1[Sheet1_columns]
      Sheet1_columns = [col for col in Sheet1.columns if col != 'heure']
      Sheet1_columns.insert(8, 'heure')
      Sheet1 = Sheet1[Sheet1_columns]
      Sheet1[['Objet-split-0-78jp', 'Objet-split-1-78jp']] = Sheet1['Objet'].str.split('Objet :', -1, expand=True)
      Sheet1 = Sheet1[Sheet1.columns[:7].tolist() + ['Objet-split-0-78jp', 'Objet-split-1-78jp'] + Sheet1.columns[7:-2].tolist()]
      Sheet1.drop(['Objet-split-0-78jp'], axis=1, inplace=True)
      Sheet1.drop(['Objet'], axis=1, inplace=True)
      Sheet1.rename(columns={'Objet-split-1-78jp': 'Objet'}, inplace=True)
      Sheet1[['Acheteur public-split-0-0vz6', 'Acheteur public-split-1-0vz6']] = Sheet1['Acheteur public'].str.split('Acheteur public :', -1, expand=True)
      Sheet1 = Sheet1[Sheet1.columns[:7].tolist() + ['Acheteur public-split-0-0vz6', 'Acheteur public-split-1-0vz6'] + Sheet1.columns[7:-2].tolist()]
      Sheet1.drop(['Acheteur public'], axis=1, inplace=True)
      Sheet1.drop(['Acheteur public-split-0-0vz6'], axis=1, inplace=True)
      Sheet1.rename(columns={'Acheteur public-split-1-0vz6': 'Acheteur public'}, inplace=True)
 
      
      global df
      df= Sheet1
      for i in tqdm(range(df.shape[0])):
         df.loc[i,'data'] = preprocessor(df['Objet'][i])

      df=df[df['data'].apply(lambda val: any(s in str(val) for s in filtres ))]
      df.drop(['data'], axis=1, inplace=True)

      # df.to_excel('GlobalBeforeTable.xlsx')

      t=datetime.datetime.today()
      t= "Appels d'offres " + t.strftime('%m/%d/%Y')+ ".xlsx"
      out = io.BytesIO()
      writer = pd.ExcelWriter(out, engine='xlsxwriter')
      df.to_excel(excel_writer=writer, index=False, sheet_name="Main")

      writer.save()
      writer.close()
      r = make_response(out.getvalue())
      r.headers["Content-Disposition"] = "attachment; filename="+t
      r.headers["Content-type"] = "application/x-xls"
      return r

if __name__ == '__main__':
   app.run(debug = True)
