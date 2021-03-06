# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from game.player import *
from game.Card import *
from game.market import *
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from models import User
from django import template

Players = {}
CardPiles = None
Markets = None
GameEnd = False

register = template.Library()


def get_value(map, key):
    return map[key]


key = register.filter('key', get_value)


# Create your views here.
class UserForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=50)
    password = forms.CharField(label='密码', widget=forms.PasswordInput())


class Hello:
    def __init__(self):
        self.body = ""
        self.title = ""


# Create your views here.
def say_hello(request):
    hello = Hello()
    hello.body = "hello world"
    hello.title = "hello title"
    users = [1, 2, 3, 4, 5]
    return render(request, 'index.html', {"hello": hello, "users": users})


def login(request):
    if request.method == 'POST':
        userform = UserForm(request.POST)
        if userform.is_valid():
            username = userform.cleaned_data['username']
            password = userform.cleaned_data['password']

            user = User.objects.filter(username__exact=username, password__exact=password)
            if user:
                return HttpResponseRedirect("/index/?user={}".format(username))
            else:
                return HttpResponse('用户名或密码错误,请重新登录')
    else:
        userform = UserForm()
    return render(request, 'login.html', {'userform': userform})


def register(request):
    global Players
    global CardPiles
    global Markets
    uname = request.REQUEST.get("username", "")
    Players[uname] = Player(Markets, CardPiles)
    return render(request, 'index.html',
                  {"username": uname, "players": Players, "cardpiles": CardPiles, "markets": Markets})


def new_game(request):
    global Players
    global CardPiles
    global Markets
    uname = request.GET.get("user")
    Markets = Market()
    Players = {}
    CardPiles = CardPile()
    Markets.init()
    CardPiles.init()
    return render(request, 'index.html',
                  {"username": uname, "players": Players, "cardpiles": CardPiles, "markets": Markets})


def test(request):
    global Players
    global CardPiles
    global Markets
    global GameEnd
    uname = request.GET.get("user")
    print uname
    Markets = Market()
    CardPiles = CardPile()
    Players["lizhe"] = Player(Markets, CardPiles, "lizhe", u"哲哥")
    Players["zhangpengcheng"] = Player(Markets, CardPiles, "zhangpengcheng", u"程哥")
    Players["shanliang"] = Player(Markets, CardPiles, "shanliang", u"良哥")
    Players['zhangbowen'] = Player(Markets, CardPiles, "zhangbowen", u"文哥")
    Players["lizhe"].init_ziyuan()
    Players["zhangpengcheng"].init_ziyuan()
    Players["shanliang"].init_ziyuan()
    Players['zhangbowen'].init_ziyuan()
    CardPiles.init()
    GameEnd = False
    print(str(CardPiles.wupin_card))
    # Players["lizhe"].wupin_card[CardPiles.wupin_card["1"].id] = CardPiles.wupin_card["1"]
    # Players["zhangpengcheng"].wupin_card["2"] = CardPiles.wupin_card["2"]
    print("lizhe has ", Players["lizhe"].wupin_card)
    # Players["shanliang"].wupin_card["1"] = CardPiles.wupin_card["1"]
    return render(request, 'index.html',
                  {"username": uname, "players": Players, "cardpiles": CardPiles, "markets": Markets})


def get_wupin_card_pile(request):
    global Players
    global CardPiles
    global Markets
    user = request.GET.get("user")
    uname = user
    print("uname=", uname)
    warning = Players[user].get_a_wupin_card()
    if warning is None:
        warning = ""
    print(CardPiles)
    return render(request, 'index.html', {"username": uname, "players": Players,
                                          "cardpiles": CardPiles, "markets": Markets, "warning": warning})


def get_ziyuan_card_pile(request):
    global Players
    global CardPiles
    global Markets
    user = request.GET.get("user")
    uname = user
    print("uname=", uname)
    warning = Players[user].get_a_ziyuan_card()
    if warning is None:
        warning = ""
    return render(request, 'index.html', {"username": uname, "players": Players,
                                          "cardpiles": CardPiles, "markets": Markets, "warning": warning})


def flush(request):
    global Players
    global CardPiles
    global Markets
    global GameEnd
    print GameEnd
    user = request.GET.get("user")
    uname = user
    return render(request, 'index.html', {"username": uname, "players": Players,
                                          "cardpiles": CardPiles, "markets": Markets,
                                          "gameend": GameEnd})


def get_card_from_consider(request):
    global Players
    global CardPiles
    global Markets
    user = request.GET.get("user")
    card_id = request.GET.get("card")
    player_name = request.GET.get("player")
    uname = user
    print("uname=", uname)
    warning = Players[player_name].get_card_from_consider(card_id)
    if warning is None:
        warning = ""
    print(CardPiles)
    return render(request, 'index.html', {"username": uname, "players": Players,
                                          "cardpiles": CardPiles, "markets": Markets, "warning": warning})


def use_card(request):
    global Players
    global CardPiles
    global Markets
    global GameEnd
    user = request.GET.get("user")
    card_id = request.GET.get("card")
    uname = user
    print("uname=", uname)
    Players[user].use(card_id)
    if Players[user].is_win():
        GameEnd = True
    else:
        GameEnd = False
    print(CardPiles)
    return render(request, 'index.html', {"username": uname, "players": Players,
                                          "cardpiles": CardPiles, "markets": Markets,
                                          "gameend": GameEnd})


def drop_card(request):
    global Players
    global CardPiles
    global Markets
    user = request.GET.get("user")
    player = request.GET.get("player")
    card_id = request.GET.get("card")
    uname = user
    print("uname=", uname)
    print("players have", Players.keys())
    print("lizhe has ", Players["lizhe"].wupin_card)
    print("zhangpengcheng has ", Players["zhangpengcheng"].wupin_card)
    Players[player].drop_to_none(card_id)
    print(CardPiles)
    return render(request, 'index.html',
                  {"username": uname, "players": Players, "cardpiles": CardPiles, "markets": Markets})


def drop_consider(request):
    global Players
    global CardPiles
    global Markets
    user = request.GET.get("user")
    card_id = request.GET.get("card")
    player_name = request.GET.get("player")
    to_none = request.GET.get("tonone")
    if to_none is None or len(to_none) == 0:
        to_none = False
    else:
        to_none = True
    uname = user
    print("uname=", uname)
    Players[player_name].drop_to_market(card_id, to_none=to_none)
    print(CardPiles)
    return render(request, 'index.html', {"username": uname, "players": Players,
                                          "cardpiles": CardPiles, "markets": Markets})


def add_score(request):
    global Players
    global CardPiles
    global Markets
    user = request.GET.get("user")
    score = int(request.GET.get("score"))
    uname = user
    print("uname=", uname)
    Players[user].add_score(score)
    print(CardPiles)
    return render(request, 'index.html', {"username": uname, "players": Players,
                                          "cardpiles": CardPiles, "markets": Markets})


def sub_score(request):
    global Players
    global CardPiles
    global Markets
    user = request.GET.get("user")
    score = int(request.GET.get("score"))
    uname = user
    print("uname=", uname)
    Players[user].sub_score(score)
    print(CardPiles)
    return render(request, 'index.html', {"username": uname, "players": Players,
                                          "cardpiles": CardPiles, "markets": Markets})


def buy(request):
    global Players
    global CardPiles
    global Markets
    user = request.GET.get("user")
    card_id = request.GET.get("card")
    uname = user
    print("uname=", uname)
    warning = Players[user].get_card_from_market(card_id)
    if warning is None:
        warning = ""
    print(CardPiles)
    return render(request, 'index.html', {"username": uname, "players": Players,
                                          "cardpiles": CardPiles, "markets": Markets, "warning": warning})


def get_hand(request):
    global Players
    global CardPiles
    global Markets
    user = request.GET.get("user")
    card_id = request.GET.get("card")
    player = request.GET.get("player")
    uname = user
    print("uname=", uname)
    print Players.keys()
    warning = Players[player].stolen(card_id, Players[user])
    if warning is None:
        warning = ""
    print(CardPiles)
    return render(request, 'index.html', {"username": uname, "players": Players,
                                          "cardpiles": CardPiles, "markets": Markets, "warning": warning})


def change_ziyuan(request):
    global Players
    global CardPiles
    global Markets
    user = request.GET.get("user")
    one = request.GET.get("one")
    five = request.GET.get("five")
    zise = request.GET.get("zise")
    one = int(one) if one.isdigit() else 0
    five = int(five) if five.isdigit() else 0
    zise = int(zise) if zise.isdigit() else 0
    uname = user
    print("uname=", uname)
    print Players.keys()
    warning = Players[user].change_ziyuan(one, five, zise)
    if warning is None:
        warning = ""
    print(CardPiles)
    return render(request, 'index.html', {"username": uname, "players": Players,
                                          "cardpiles": CardPiles, "markets": Markets, "warning": warning})


def add_ziyuan(request):
    global Players
    global CardPiles
    global Markets
    user = request.GET.get("user")
    one = request.GET.get("one")
    five = request.GET.get("five")
    zise = request.GET.get("zise")
    one = int(one) if one.isdigit() else 0
    five = int(five) if five.isdigit() else 0
    zise = int(zise) if zise.isdigit() else 0
    uname = user
    print("uname=", uname)
    print Players.keys()
    warning = Players[user].add_ziyuan(one, five, zise)
    if warning is None:
        warning = ""
    print(CardPiles)
    return render(request, 'index.html', {"username": uname, "players": Players,
                                          "cardpiles": CardPiles, "markets": Markets, "warning": warning})


def del_ziyuan(request):
    global Players
    global CardPiles
    global Markets
    user = request.GET.get("user")
    one = request.GET.get("one")
    five = request.GET.get("five")
    zise = request.GET.get("zise")
    one = int(one) if one.isdigit() else 0
    five = int(five) if five.isdigit() else 0
    zise = int(zise) if zise.isdigit() else 0
    uname = user
    print("uname=", uname)
    print Players.keys()
    warning = Players[user].del_ziyuan(one, five, zise)
    if warning is None:
        warning = ""
    print(CardPiles)
    return render(request, 'index.html', {"username": uname, "players": Players,
                                          "cardpiles": CardPiles, "markets": Markets, "warning": warning})


def drop_ziyuan(request):
    global Players
    global CardPiles
    global Markets
    user = request.GET.get("user")
    player = request.GET.get("player")
    uname = user
    print("uname=", uname)
    print Players.keys()
    warning = Players[player].drop_ziyuan_random()
    if warning is None:
        warning = ""
    print(CardPiles)
    return render(request, 'index.html', {"username": uname, "players": Players,
                                          "cardpiles": CardPiles, "markets": Markets, "warning": warning})


def stole_ziyuan(request):
    global Players
    global CardPiles
    global Markets
    user = request.GET.get("user")
    player = request.GET.get("player")
    is_drop = request.GET.get("isdrop")
    if len(is_drop) == 0:
        is_drop = False
    else:
        is_drop = True
    uname = user
    print("uname=", uname)
    print Players.keys()
    warning = Players[player].stolen_ziyuan(Players[user], is_drop)
    if warning is None:
        warning = ""
    print(CardPiles)
    return render(request, 'index.html', {"username": uname, "players": Players,
                                          "cardpiles": CardPiles, "markets": Markets, "warning": warning})
