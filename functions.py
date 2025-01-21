def get_by_info(json_file, typ, further_info, categories, logic = "and") :  
 selected = []
 all = ["entree", "main_dish", "Side_dish", "desert", "alcoholic", "non_alcoholic"]
 if categories is None :
   categories = all  
 for j in categories :
    selected.append(get_out_of_category(json_file, typ, further_info, j, logic))
 return selected

def get_out_of_category(json_file, typ, further_info, category, logic) :
 selected = [category,] 
 if further_info is None :
   
   for n in json_file.get("menu").get(category).get("items") : 
     try: 
      selected.append(json_file.get("menu").get(category).get(typ)[json_file.get("menu").get(category).get("items").index(n)]) 
     except:
       None
 else: 
  if  logic == "or" : 
    for n in json_file.get("menu").get(category).get("items") : 
     for i in further_info : 
      furth = i.lower()
      if type(n) is str:
       if furth in json_file.get("menu").get(category).get("items")[json_file.get("menu").get(category).get("items").index(n)].lower() :
        selected.append(json_file.get("menu").get(category).get(typ)[json_file.get("menu").get(category).get("items").index(n)])    
        break
  
  if logic == "and" :
    for n in json_file.get("menu").get(category).get("items") : 
      and_clause = 0
      for i in further_info: 
       furth = i.lower()
       if type(n) is str: 
        if furth in json_file.get("menu").get(category).get("items")[json_file.get("menu").get(category).get("items").index(n)].lower() : 
         and_clause += 1 
      if and_clause == len(further_info) : 
        selected.append(json_file.get("menu").get(category).get(typ)[json_file.get("menu").get(category).get("items").index(n)])  
 
 
 return selected

def get_median_price(json_file, further_info, categories, logic = "and" ) :
     import statistics
     dataset = []
     for i in get_by_info(json_file, "prices", further_info, categories, logic ) :
        for j in i :
          if type(j) is int:
           dataset.append(j)
          elif type(j) is float:
            dataset.append(j) 
        for i in dataset: 
         if i is not None : 
          return statistics.median(dataset)   

def cost_check(json_file, billsplit, costumers, drinks, expcut):
  all  = ["entree", "main_dish", "desert"]
  medians = []
  drink_median = 0 
  if expcut is True :
   if billsplit is True:
    def sucesion(n) : 
     if n == 1:
      return 1
     else : 
      return (sucesion(n-1) * (n-1) + (n % 2)) / n
   if billsplit is False: 
     def sucesion(n) :
       if n == 1:
        return 1
       else : 
        return (sucesion(n-1) + (n % 2))
    

   entrees = [] 
   import statistics
   all.remove("entree")
  
  if get_median_price(json_file, None, ["alcoholic", "non_alcoholic"]) is not None:
    drink_median = get_median_price(json_file, None, ["alcoholic", "non_alcoholic"])
  for i in all :
     if get_median_price(json_file, None, [i] ) is not None : 
       medians.append(get_median_price(json_file, None, [i] ))
  if expcut is True :
   for v in json_file.get("menu").get("entree").get("items") :
     count = 0
     if v is not None :  
      for x in ["crema", "sopa"] : 
       if x in v :
        count +=1 
     if count == 0 : 
      if (type(json_file.get("menu").get("entree").get("prices")[json_file.get("menu").get("entree").get("items").index(v)]) is int) or (type(json_file.get("menu").get("entree").get("prices")[json_file.get("menu").get("entree").get("items").index(v)]) is float) :
       entrees.append(json_file.get("menu").get("entree").get("prices")[json_file.get("menu").get("entree").get("items").index(v)])   
  if medians == [] :
     medians = 0
  else :
     medians = sum(medians)  
  if expcut is False :
     if billsplit is True:
      return (medians + (drink_median * drinks))
     elif billsplit is False: 
      return costumers * (medians + (drink_median * drinks))   
  if (expcut is True) :
     if entrees != [] :     
      if billsplit is False:
       return (costumers * (medians + (drink_median * drinks))) + (statistics.median(entrees) * sucesion(costumers)) 
      else:
       return (medians + (drink_median * drinks)) + (statistics.median(entrees) * sucesion(costumers))  
     else:  
      if billsplit is False:
       return costumers * (medians + (drink_median * drinks))
      if billsplit is True:
        return (medians + (drink_median * drinks))
        

def affordabillity_check(json_file, budget, people, drinks, expcut) :
  return cost_check(json_file, False, people, drinks, expcut) * 100 / budget 


def Diversity_within_a_menu(json_file, category, min):
 tipos = {
   "Pescado" : ["pescado", "pargo", "bacalao", "canciller"], 
   "res": ["vaca", "res", "beef", "ropavieja"], 
   "pollo" : ["pollo", "gordon blue", "gordonblue", "pechuga"], 
   "cerdo" : ["cerdo", "puerco"],
   "pizza" : ["pizza"],
   "pasta" : ["pasta", "lasagna", "lasana", "canelonni", "caneloni", "canelones", "fettuccine", "fettuccini", "spaguetti", "espaguetti", "espagueti", "penne", "macarrones", "maccarroni"],
   "langosta/camarones" : ["lobster", "langosta", "thermidor", "camar", "gamba", "camarones"],
   "sandw..." : ["ndwich", "emparedado", "pan con", "pan c/", "hamburguesa", "hotdog", "hot dog"]
   }
   
 length = len(json_file.get("menu").get(category).get("items")) 
 if length < min :
   return None
 Suma = 0
 N = 0
 compare = []
 rest = 0
 for d in tipos :
   n = 0 
   for c in get_out_of_category(json_file, "items", tipos[d], category, "or") :
      if c not in compare:
       if c != category:
        compare.append(c)
        n += 1
        N += 1
   Suma += (n*(n-1))
 for p in json_file.get("menu").get(category).get("items"):
  if p not in compare: 
    rest +=1
 Suma += (rest*(rest-1))
 N += rest
 if N != 0 : 
  return (Suma / (N * (N-1)))
 else :
   return None
   

   








