from django.http import HttpResponse
from django.shortcuts import render, redirect

from . import models
from .models import Result
from blackjack_code.main import single_simulation


def index(request):
    result = Result.objects.last()
    with open('blackjack_code/bankroll/TEST.csv') as f:
        first_line = f.readline()
    context = {'result': result, 'text': first_line}
    return render(request, 'blackjack/index.html', context)


def simulate(request):
    zen = {
        "name": "ZEN", "2": 1, "3": 1, "4": 2, "5": 2, "6": 2, "7": 1, "8": 0, "9": 0, "10": -2,
        "Jack": -2, "Queen": -2, "King": -2, "Ace": -1}
    adv = single_simulation('basic', 6, 'S17', .90, 'true', zen)
    result = Result.objects.create(name="Test", average_profit=adv)
    result.save()

    return redirect('index')


def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)


def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)
