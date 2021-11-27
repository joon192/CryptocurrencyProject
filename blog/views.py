from django.shortcuts import render, redirect
from .utils import get_plot_1d, get_plot_3d, get_plot_5d
from datetime import datetime, timedelta
import plotly.express as px
from .final import input_n_bounds_alevel_output_crypto, Recommendation_DB
from .models import User

# Create your views here.
def main(request):
    data = {
            }

    return render(request, "Main.html", data)

def detail(request):
    context = {

    }

    return render(request, "More-in-crypto.html", context=context)

def recommend(request):
    context = {

    }

    return render(request, "Recommendation.html", context=context)

modeling={}

def result(request):
    if request.method == "POST":
        select = request.POST.getlist('select')
        data = {'select': select}
        print(data["select"][0:4])
        global modeling
        modeling = {
            'model': input_n_bounds_alevel_output_crypto(int(data["select"][2]), int(data["select"][3]), int(data["select"][0]), int(data["select"][1]))
        }
        print(modeling)
    return render(request, "Result.html", modeling)

def about(request):
    context = {

    }

    return render(request, "About.html", context=context)

def signup(request):
    if request.method == "POST":
        print(request.POST)
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        phonenumber = request.POST["phonenumber"]

        user = User.objects.create_user(username, email, password)
        user.phonenumber = phonenumber
        user.save()
        return redirect("user:main")

    return render(request, "signup.html")

