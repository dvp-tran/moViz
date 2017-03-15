# -*- coding: utf-8 -*-
import urllib2
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import time
from socket import timeout
import timeout_decorator #pip install timeout-decorator
import os
import re




@timeout_decorator.timeout(45)
def get_top100(year,path):
    #Generate lists
    if not os.path.exists(path):
        os.makedirs(path)
    A=[]
    B=[]
    C=[]
    D=[]
    E=[]
    F=[]
    G=[]
    time_start=time.time()
    year=str(year)
    for page in "1","2":
        request = urllib2.Request("http://www.imdb.com/search/title?release_date="+year+"&sort=boxoffice_gross_us,desc&page="+page+"&ref_=adv_prv",headers={"Accept-Language": "en-US,en;q=0.5"})

        #Query the website and return the html to the variable 'page'
        page = urllib2.urlopen(request).read()
        soup = BeautifulSoup(page,"html.parser")
        for film in soup.body.div.div.find('div', class_='pagecontent').find('div', class_='redesign').div.div.div.find('div', class_='lister-list').findAll('div', class_='lister-item mode-advanced'):
            A.append(film.find('div', class_='lister-item-content').h3.find('span', class_='lister-item-index unbold text-primary').string)
            B.append(film.find('div', class_='lister-item-content').h3.a.string)
            C.append(film.find('div', class_='lister-item-content').h3.find('span', class_='lister-item-year text-muted unbold').string)
            D.append(film.find('div', class_='lister-item-content').p.find('span', class_='runtime').string)
            E.append(film.find('div', class_='lister-item-content').p.find('span', class_='genre').string)
            directeur=film.find('div', class_='lister-item-content').findAll('p')[2].a.string
            F.append(directeur.strip('\n'))
    
    #import pandas to convert list to data frame
    df=pd.DataFrame(A,columns=['classement'])
    df['titre']=B
    df['annee']=C
    df['duree']=D
    df['categorie']=E
    df['realisateur']=F
    df.to_csv(path + "%s.csv" %(year),sep=';',encoding='latin1')
    elapsed=time.time()-time_start
    print('Done saving for year %s in %s s' %(year,elapsed))
    return df

def read_top100(year,path)
    return pd.read_csv(path+"%s.csv"%(year), sep=";",encoding='latin1',index_col=0)

def get_curated(year,path)
    return pd.read_csv(path+"%s.csv"%(year), sep=";",encoding='latin1',index_col=0)


def compare_top_vs_script(year,path_origin,path_destination):
    time_start=time.time()
    url_site="http://www.imsdb.com"   
    liste_script = urllib2.Request(url_site+"/all%20scripts")
    page = urllib2.urlopen(liste_script).read()
    soup = BeautifulSoup(page,"html.parser")
    annee=str(year)
    fichier=path_origin+annee+".csv"
    top=pd.read_csv(fichier, sep=";",encoding='latin1',index_col=0)
    top['url'] = [None] * len(top)
    top['url_script'] = [None] * len(top)
    for j in range(100):
        titre_top=top['titre'][j]
        for film in soup.body.findAll('table')[1].tr.find('td', valign='top').findAll('p'):
            titre=film.a.string
            if titre_top==titre:
                url_film=url_site+film.a.get('href')
                top['url'][j]=url_film
                url_film=url_film.replace(" ","%20")
                liste_script_ = urllib2.Request(url_film)
                page_ = urllib2.urlopen(liste_script_).read()
                soup_ = BeautifulSoup(page_,"html.parser")
                #print(url_film)
                a = soup_.findAll('a', href=re.compile('^/scripts/'))
                if len(a)==0:
                    print('Did not find scriptfile for %s.' %(url_film))
                #print(a)
                else:
                    top['url_script'][j]=url_site+a[0]['href']
                #print(j,' : ',titre,' : ',url_film)
    if not os.path.exists(path_destination):
        os.makedirs(path_destination)
    top.to_csv(path_destination+annee+".csv",sep=';',encoding='latin1')
    elapsed=time.time()-time_start
    print('Done comparing scripts and tops for year %s in %s s.' %(year,elapsed))
    return top    
    
    
    
    
    
  