from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.db import IntegrityError
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

from django.conf import settings
from django.contrib.auth.decorators import login_required
from bs4 import BeautifulSoup
import requests
from django.core.paginator import Paginator, EmptyPage




import requests
from bs4 import BeautifulSoup
from django.shortcuts import render
import unicodedata
from .models import Recette
recettes_t =[]
recettes_des =[]
recettes_img_url =[]
recettes_url_des_list =[]


def get_recettes(page):
    src = page.content
    soup = BeautifulSoup(src, "lxml")

    recettes_title = soup.find_all("h3")
    recettes_title = recettes_title[1:]
    recettes_desc = soup.find_all("p")
    recettes_imgs = soup.find_all("img", {"decoding": "async"})

    for i in range(len(recettes_title)):
        title = recettes_title[i].text
        # Check if a Recette object with the same title already exists in the database
        if Recette.objects.filter(title=title).exists():
            continue
        recette = Recette(
            title=title,
            description=recettes_desc[i].text,
            image_url=recettes_imgs[i].get("src"),
        )
        recette.save()

page = requests.get("https://www.recettescooking.com/")
get_recettes(page)


def recettes_view(request):
    recettes = Recette.objects.all()

    per_page = 6

    paginator = Paginator(recettes, per_page)

    page_number = request.GET.get('page')

    try:
        page = paginator.get_page(page_number)
    except EmptyPage:
        page = paginator.get_page(paginator.num_pages)

    context = {
        'recettes': page,
    }

    return render(request, 'index.html', context)


# Create your views here.
class MyPasswordResetView(PasswordResetView):
    template_name = 'password_reset_form.html'
    email_template_name = 'password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')
    
    
class MyPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'password_reset_done.html'
    
class MyPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'password_reset_confirm.html'
    success_url = reverse_lazy('login')
    
class MyPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'password_reset_complete.html'


def logOut(request):
    logout(request)
    return redirect('login')


def signUp(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        passwordConf = request.POST.get('passwordConf')
        if password != passwordConf:
            messages.error(request, 'Passwords do not match.')
        elif username == '' or email == '' or password == '' or passwordConf == '':
            messages.error(request, 'Enter all informations.')
        else:
            try:
                myUser = User.objects.create_user(username,email,password)
                myUser.save()
                return redirect('login')
            except IntegrityError:
                messages.error(request, 'This username is already taken. Please choose a different username.')
    return render(request,'signup.html')

def logIn(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass')
        user = authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            #messages.success(request, f"Welcome, {user.username} !")
            return redirect('index')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request,'login.html')

def Index(request):
    #context = recettes_view(request)
    #return render(request,'index.html', context)
    return recettes_view(request)
    
def aboutUs(request):
    return render(request,'about.html')

def userAccount(request):
    return render(request, 'user_account.html')



@login_required
def user_profile(request):
    user = request.user
    return render(request, 'user_account.html', {'user': user})


def search_recipes(request):
    query = request.GET.get('keyword')
    if query:
        #recipes = Recette.objects.filter(title__contains=query).distinct()
        recipes = Recette.objects.filter(title__icontains=query).distinct()
    else:
        recipes = Recette.objects.none()

    paginator = Paginator(recipes, 9)  # Modifier le nombre d'éléments par page selon vos besoins
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'recettes': page_obj,
        'keyword': query,
    }

    return render(request, 'index.html', context)

from .models import Commentaire

@login_required
def ajouter_commentaire(request):
    if request.method == 'POST':
        opinion = request.POST.get('opinion')  
        utilisateur = request.user  
        recette_id = request.POST.get('recette_id') 

        try:
            recette = Recette.objects.get(id=recette_id)
        except Recette.DoesNotExist:
            pass

        if opinion:
            commentaire = Commentaire(texte=opinion, utilisateur=utilisateur, recette=recette)
            commentaire.save()    
        return redirect('index')  

    return render(request, 'index.html') 

from .models import Ranking
def ajouter_rank(request, recette_id):
    recette = get_object_or_404(Recette, pk=recette_id)

    if request.method == 'POST':
        rank = request.POST.get('rank')
        if rank and rank.isdigit():  
            user = request.user
            ranking = Ranking.objects.create(user=user, recette=recette, rank=rank)
            ranking.save()
            return redirect('index')
        else:
            return HttpResponseBadRequest("Le champ de note est invalide.")
    
    context = {'recette': recette}
    return render(request, 'index.html', context)


