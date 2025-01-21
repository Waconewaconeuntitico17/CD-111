import json

import statistics
import matplotlib.figure
import matplotlib.font_manager
import matplotlib.pyplot
import functions
import matplotlib
from pathlib import Path
#"Hoteleria y restauracion" : 4564,

matplotlib.rcParams.update({'font.size': 8})
wages = {"Ciencia innovacion y tecnologia" : 5376, "Hoteleria y restauracion" : 4564, "agricultura" : 4455, "Salud" : 4222,  "Educacion": 3932}
x = ["Playa", "Plaza de la revolucion", "Centro habana", "Diez de octubre", "Habana Vieja", "Habana del Este"]
y = []
mun = ["Playa", "Plaza de la revolucion", "Centro habana", "Diez de octubre", "Habana Vieja", "Habana del Este", "Cerro", "La Lisa", "San Miguel del Padron"]
tipos = {
   "fish" : ["pescado", "pargo", "bacalao", "canciller"], 
   "pork" : ["cerdo", "puerco"],
   "beef": ["vaca", "res", "beef", "ropavieja"], 
   "chicken" : ["pollo", "gordon blue", "gordonblue", "pechuga"]
 }

def cestpartiedutruc(p) :
  per_wage = []
  for n in x :
   for i in Path(n).iterdir() :
    with open (i, "r", encoding="utf-8") as truc :
     ouf = json.load(truc)
     per_wage.append(functions.affordabillity_check(ouf, wages.get(p), 1, 2, True)) 
   y.append(statistics.mean(per_wage))
   per_wage.clear()      
   


def cestuntruc() :
 
 matplotlib.pyplot.figure(figsize = (10,6))
 for v in wages :
    
    cestpartiedutruc(v)
    matplotlib.pyplot.scatter(x,y, label = v) 
    matplotlib.pyplot.legend() 
    y.clear()

def pechesansleurre():
 deselements = ["fish", "pork", "beef", "chicken", "other" ]
 partie = [0, 0, 0, 0, 0]
 for i in mun :
  for l in Path(i).iterdir():
   with open(l, "r", encoding = "utf-8") as truc:
      ouf = json.load(truc) 
      for t in functions.get_out_of_category(ouf, "items", None, "main_dish", "or") :
           partie[4] += 1
      for g in tipos :
       for n in functions.get_out_of_category(ouf, "items", tipos[g], "main_dish", "or") :
        if (type(n) is not list) and (n != "main_dish") :
          partie[deselements.index(g)] += 1 
          partie[4] -= 1

                           
 matplotlib.pyplot.pie(partie, labels = deselements) 



def pecheavecleurre():
 deselements = ["fish", "pork", "beef", "chicken"]

 g_avg = []
 y_axis = []
 for g in  tipos:
  for i in mun :
   for l in Path(i).iterdir():
     with open(l, "r", encoding = "utf-8") as truc:
      ouf = json.load(truc)      
      for n in functions.get_out_of_category(ouf, "prices", tipos[g], "main_dish", "or") :
        if (type(n) is not list) and (type(n) is not str) :
         g_avg.append(n)
       
  y_axis.append(statistics.mean(g_avg))
  g_avg.clear()

 matplotlib.pyplot.bar(deselements, y_axis)

def cestdautre(k) :
  per_person = []
  for n in x :
   for i in Path(n).iterdir() :
    with open (i, "r", encoding="utf-8") as truc :
     ouf = json.load(truc)
     per_person.append(functions.cost_check(ouf,True, 4, 2, k)) 
   y.append(statistics.mean(per_person))
   per_person.clear()      
   


def ouaiscestdautre() :
    matplotlib.pyplot.figure(figsize = (10,6))
    cestdautre(True)
    matplotlib.pyplot.scatter(x,y, label = "sharing an entree") 
    y.clear()
    cestdautre(False)
    matplotlib.pyplot.scatter(x,y, label = "whole entree for each") 
    y.clear()
    matplotlib.pyplot.legend() 

def troipummons(minim) :
  checked = []
  rank = []
  allrest = {}
  munc = {}
  pos = 0
  for i in mun :
   for l in Path(i).iterdir():
     with open(l, "r", encoding = "utf-8") as truc:
      ouf = json.load(truc) 
      if functions.Diversity_within_a_menu(ouf, "main_dish", minim) is not None:
       rank.append(functions.Diversity_within_a_menu(ouf, "main_dish", minim)) 
       allrest[ouf.get("name")] = functions.Diversity_within_a_menu(ouf, "main_dish", minim)
       munc[ouf.get("name")] = i
  rank.sort()
  for n in rank:
    if pos < 29 : 
     for t in allrest:
      if t not in checked:
       if allrest[t] == n:
        checked.append(t)
        pos += 1
        print(f'{pos}.  {t}  ({munc[t]})')
   

    
