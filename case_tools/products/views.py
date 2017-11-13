from django.contrib.auth.decorators import login_required
from .forms import Userform, Loginform
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.contrib.auth import authenticate, login
from django.views import generic
from django.views.generic import View
from django.views.generic import FormView
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.core.files import File
import json
from django.http import JsonResponse
import codecs
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import os

def index(request):
    return HttpResponse("Hello world")


def error(request):
    return HttpResponse("Error!")


class UserFormView(View):
    form_class = Userform
    template_name = "products/signup.htm"

    def get(self, request):
        #username=request.user.get_full_name()
        form = self.form_class(None)
        
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        #username=request.user.get_full_name()
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('products:index')
        else:
            return HttpResponse("Error")

        return render(request, self.template_name, {'form': form})

@login_required
def display(request):
    page = request.GET.get('page', 1)
    with codecs.open('products/amazon.json', 'r', 'utf-8') as amazon, \
            codecs.open('products/flipkart.json', 'r', 'utf-8') as flipkart:
        data1 = json.load(amazon)
        data2 = json.load(flipkart)
    prod_list1 = data1["selection1"]
    prod_list2 = data2["selection1"]

    prod_list = list()
    # f = open("temp.txt", "w")
    pics = os.listdir('products/static/images')

    for prods in prod_list1:
        if "selection2" in prods:
            prods["image"] = None
            # print(os.listdir('products/static/images'))

            for pic in pics:
                # print("stuff="+prods["name"])
                # print("pic="+pic)
                if prods["name"] in pic:
                    # print("yes")
                    prods["image"] = pic
                    # print( prods["image"])
                    continue

            prod_list.append(prods)
    username=request.user.get_full_name()
    print(username)
    temp_list = list()
    for prods in prod_list:
        for p in prod_list2:
            if p["name"].split(',')[0].startswith(prods["name"].split(',')[0]
                                                  [:len(prods["name"].split(',')[0]) - 1]) \
                    and prods["name"] not in temp_list:
                # print(prods["name"])
                temp_list.append(prods)
    #print(temp_list)
    print("length=" + str(len(temp_list)))
    temp_list1=list()
    temp_list1=temp_list[:50]
    paginator = Paginator(temp_list1, 3)
    try:
        temp_list1 = paginator.page(page)
    except PageNotAnInteger:
        temp_list1 = paginator.page(1)
    except EmptyPage:
        temp_list1 = paginator.page(paginator.num_pages)

    context = {"prod_list": temp_list1,"username":username}

    return render(request, "products/index.html", context)


class AutoCompleteView(View):
    def get(self,request):
        name = request.GET.get("term","")
        word=name
        name=word[0].upper()+word[1:]
        print(name)        
        with codecs.open('products/amazon.json', 'r', 'utf-8') as data_file:
            data = json.load(data_file)
        prod_list1 = data["selection1"]
        prodstuff=[]
        print(name)
        if name:
            for p in prod_list1:
                if p["name"].startswith(name):
                    prodstuff.append(p)
        else:
            prodstuff=prod_list1
        i=0
        results = []
        for prods in prodstuff:
            if "selection2" in prods:
                user_json = {}
                user_json['id']=i
                user_json['label'] = prods["name"]
                user_json['value'] = prods["name"]
                results.append(user_json)
                i=i+1

        data = json.dumps(results[:10])
        mimetype = 'application/json'
        return HttpResponse(data, mimetype)

def details(request,name):
    with codecs.open('products/amazon.json', 'r', 'utf-8') as amazon,\
            codecs.open('products/flipkart.json', 'r', 'utf-8') as flipkart:
        data1 = json.load(amazon)
        data2 = json.load(flipkart)
		
    prod_list1 = data1["selection1"]
    prod_list2 = data2["selection1"]

    prod_list=list()
    pics = os.listdir('products/static')

    for prods in prod_list1:
        if "selection2" in prods:
            prods["image"]=None

            for pic in pics:
                if prods["name"] in pic:
                    prods["image"]=pic
                    continue

            prod_list.append(prods)
    '''
    temp_list=list()
    for prods in prod_list:
        for p in prod_list2:
            if p["name"].split(',')[0].startswith(prods["name"].split(',')[0]
                                                  [:len(prods["name"].split(',')[0]) - 1]) \
                    and prods["name"] not in temp_list:
                temp_list.append(prods["name"])
    #print(temp_list)
    #file=open('products/a.txt','w')
    #file.write(str(temp_list))
    #print("length=" + str(len(temp_list)))
    '''
    temp=dict()
    new_list=list()
    p_list=list()
    #username=request.user.get_full_name()
    for prods in prod_list:
        if prods["name"]==name:
            temp=prods
            for p in prod_list2:
                if p["name"].split(',')[0].startswith(prods["name"].split(',')[0]
                                                      [:len(prods["name"].split(',')[0])-1])\
                        and prods["name"] not in new_list:
                    new_list.append((temp["name"]))
                    temp["f_url"]=p["url"]
                    temp["f_price"]=p["selection2"]
                    temp["f_price_url"]=p["selection2_url"]
					

    return render(request,"products/details.html",{"product":temp})