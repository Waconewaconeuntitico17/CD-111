import json

import matplotlib.figure
import matplotlib.font_manager
import matplotlib.pyplot
import functions
import matplotlib
from pathlib import Path

wages = {"agricultura" : 4455, "Hoteleria y restauracion" : 4564, "Ciencia innovacion y tecnologia" : 5376, "Educacion": 3932, "Salud" : 4222}
x = ["plaza de la revolucion", "centro habana", "diez de octubre"]
y = []
def cestpartiedutruc(p) :
  for n in x :
   sampooool = 0
   tous =0
   for i in Path(n).iterdir() :
    tous +=1
    with open (i, "r", encoding="utf-8") as truc :
     ouf = json.load(truc)
     if functions.affordabillity_check(ouf, wages.get(p), 1, 2, "False") is True :
      sampooool += 1
   if sampooool > 1:
    y.append((sampooool * 100) / tous)  
  if y != []:
   return y

def cestuntruc() :
 
 for v in wages :
    y.clear()
    cestpartiedutruc(v)
    matplotlib.pyplot.scatter(x,y, label = v) 
    matplotlib.rcParams.update({'font.size': 8})
    matplotlib.pyplot.legend()   

