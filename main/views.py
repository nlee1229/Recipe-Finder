from django.shortcuts import render, HttpResponse, redirect
from login_reg.models import User
from .models import Recipe, Image, Ingredient
from django.db.models import Q
import json


def admin(request):
    context = {
        "user": User.objects.all(),
        "recipe": Recipe.objects.all(),
        "ing": Ingredient.objects.all(),
    }
    return render(request, "admin/admin.html", context)

# *************************************************** ADMIN
def inputinformation(request):
    context = {
        "myuser": User.objects.get(id=request.session['user_id']),
        "recipes": Recipe.objects.all(),
    }
    return render(request, "admin/input_recipe.html", context)


def add_recipe(request):
    recipe = Recipe.objects.create(
        title=request.POST["title"],
        level=request.POST["level"],
        cooktime = request.POST["cooktime"],
        desc=request.POST["desc"],
        instructions=request.POST["instructions"],
        created_by=User.objects.get(id=request.session["user_id"]),
    )
    
    # img = Image.objects.create(
        
    # )
    id = recipe.id
    return redirect(f'/recipe_profile/{id}')

def edit(request, id):
    context = {
        "recipe": Recipe.objects.get(id = id)
    }
    return render(request, "admin/edit.html", context)

def edit_proc(request, id):
    recipe = Recipe.objects.get(id = id)
    recipe.title = request.POST['title']
    recipe.desc = request.POST['desc']
    recipe.level = request.POST['level']
    recipe.cooktime = request.POST['cooktime']
    recipe.instructions = request.POST['instruction']
    recipe.save()
    return redirect(f'/recipe_profile/{id}')
    
    
def recipe_profile(request, id):
    context = {
        "myuser": User.objects.get(id=request.session['user_id']),
        "recipes": Recipe.objects.all(),
        "this_recipe": Recipe.objects.get(id=id),
        
    }
    return render(request, 'admin/input_Ing.html', context)



def add_ingredient(request, id):
    recipe = Recipe.objects.get(id = id)
    Ingredient.objects.create(
        name = request.POST["ingredient"],
        qty = request.POST["qty"],
        unit = request.POST["unit"],
        recipe = recipe
    )
    
    return redirect(f'/recipe_profile/{id}')



def add_image(request, id):
    Image.objects.create(
        img = request.POST['img'],
        recipe_img = Recipe.objects.get(id=id)
    )
    return redirect(f'/recipe_profile/{id}')

def del_image(request, id, recipe_id):
    d = Image.objects.get(id=id)
    d.delete()
    return redirect(f'/recipe_profile/{recipe_id}')
    
# This deletes the ingredient from the admin page.

def del_ing(request, id):
    d = Ingredient.objects.get(id=id)
    d.delete()
    return redirect('/input')



def del_recipe(request, id):
    r = Recipe.objects.get(id=id)
    r.delete()
    return redirect('/input')



#This deletes an ingredient from the recipe page.
def del_ingredient(request, ing_id, recipe_id):
    i = Ingredient.objects.get(id=ing_id)
    i.delete()
    return redirect(f'/recipe_profile/{recipe_id}')



# ************************************************************** USER

def home(request):
    recipes = []
    
    # Nothing is searched
    this_recipe = Recipe.objects.all()
    
    if "nosearch" in request.session: 
        context = {
            "nosearch": request.session["nosearch"]
            
        }
    
    # Everything is pulled but nothing is searched
    elif "list_of_recipes" not in request.session or request.session["list_of_recipes"] == []:
        order = Recipe.objects.all().order_by("title")
        context = {
            "list_of_recipes": order,
        }
    
    # Specific item is searched
    else:
        recipe_ids = request.session["list_of_recipes"]
        level=[]
        for id in recipe_ids:
            recipes.append(Recipe.objects.get(id=id))
            level.append(Recipe.objects.get(id=id).level)
        context = {
            "list_of_recipes": recipes,
            "level": level
        }

    
    return render(request, 'user/home.html', context)
    
def search(request):
    if request.GET.get('search', "") != "":
        if "nosearch" in request.session:
            del request.session["nosearch"]
        else:
            query = request.GET.get('search')
            results = Recipe.objects.filter(Q(title__icontains=query) | Q(desc__icontains=query) | Q(cooktime__icontains=query) | Q(instructions__icontains=query))
            if len(results) == 0:
                request.session["nosearch"] = "No results found from search."
                return redirect('/home')
            list = []
            for i in results:
                list.append(i.id)  
            request.session['list_of_recipes'] = list
    return redirect('/home')
        
def clearsearch(request):
    if "nosearch" in request.session:
        del request.session["nosearch"]
    if "list_of_recipes" not in request.session: 
        return redirect('/home')
    else:
        del request.session["list_of_recipes"]
        return redirect('/home')    

################################## WORK IN PROGRESS!
def searching(request):
    if request.GET.get('searching', "") != "":
        if "nosearching" in request.session:
            del request.session["nosearching"]
        query = request.GET.get('searching')
        x = query.split(", ")
        results = Ingredient.objects.filter(Q(name__icontains=query) | Q(name__in= x))
        if len(results) == 0:
            request.session["nosearching"] = "No results found from search."
            return redirect('/list_ingredients')
        else:
            list=[]
            for item in results:
                list.append(item.id)
            request.session['list_of_ingredient'] = list
  
        
    return redirect('/list_ingredients')

def clearsearching(request):
    if "nosearching" in request.session:
        del request.session["nosearching"]
    if "list_of_ingredient" not in request.session: 
        return redirect('/list_ingredients')
    else:
        del request.session["list_of_ingredient"]
        return redirect('/list_ingredients')    


################################## WORK IN PROGRESS!
def list_ingredients(request):
    if "nosearching" in request.session: 
        context = {
            "nosearching": request.session["nosearching"]
            
        }
    if "list_of_ingredient" in request.session:
        list_name=[]
        for id in request.session["list_of_ingredient"]:
            list_name.append(Ingredient.objects.get(id=id))
        ing_list = list_name
    else:
        ing_list = Ingredient.objects.all()    
    list = []
    for item in ing_list:
        if str(item.name).capitalize() not in list:
            list.append(str(item.name).capitalize())
    list.sort()
    context = {
        "unique_ing" : list
    }
    return render(request, 'user/ingredient.html', context)
    
def process_ing(request): 
    list = request.POST.getlist("item")
    this_set = set(list)
    list_of_recipes = []
    for recipe in Recipe.objects.all():
        temp_set = set([])
        for ing in recipe.ingredients.all():
            temp_set.add(ing.name)
        if temp_set.intersection(this_set):
            list_of_recipes.append(recipe.id)
    request.session["list_of_recipes"] = list_of_recipes
    return redirect('/home')
    

# **********************************************************

def account_user(request):    
    thisuser = User.objects.get(id = request.session["user_id"])

    if "recents" in request.session:
        list = request.session["recents"]
        recipe_list=[]
        for id in list:
            recipe_list.append(Recipe.objects.get(id=id))

        context = {
            'user' : User.objects.get(id = request.session["user_id"]),
            'most_recent' : recipe_list[:4],
            'img': thisuser.favorites.all()
        }
    
    else: 
        context = {
            'user' : User.objects.get(id = request.session["user_id"]),
            'most_recent' : [],
            'img': thisuser.favorites.all()
        }
        
    return render(request, 'user/user_acct.html', context)


def addfav(request, recipe_id):
    this_user = User.objects.get(id=request.session["user_id"])
    fav = Recipe.objects.get(id=recipe_id)
    this_user.favorites.add(fav)
    return redirect('/home')

def addfavfromrecipe(request, recipe_id):
    this_user = User.objects.get(id=request.session["user_id"])
    fav = Recipe.objects.get(id=recipe_id)
    this_user.favorites.add(fav)
    return redirect(f'/recipeinfo/{recipe_id}')

def removefav(request, recipe_id):
    this_user = User.objects.get(id=request.session["user_id"])
    fav = Recipe.objects.get(id=recipe_id)
    this_user.favorites.remove(fav)
    return redirect('/account_user')
# **********************************************************

def recipeinfo(request, id):
    this_recipe = Recipe.objects.get(id=id)
    this_user = User.objects.get(id=request.session["user_id"])
    # remove if recipe is in recents then add again...............
    if this_recipe in this_user.recents.all():
        this_user.recents.remove(this_recipe)
    this_user.recents.add(this_recipe)
    # Put recent recipes in a list and reverse list...............
    dict={}
    count=0
    for i in this_user.recents.all():
        dict[count] = i.id
        count += 1
    list=[]
    for i in range(-len(dict)+1, 1):
        list.append(dict[-i])
    request.session["recents"] = list
    # Convert difficulty level into length of list to loop thru...............
    level=[]
    length=this_recipe.level
    for i in range(length):
        level.append(i)

    context = {
        "recipe": Recipe.objects.get(id=id),
        "level": level
    }
    return render(request, 'user/recipeinfo.html', context)

