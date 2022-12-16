from django.shortcuts import render
from utils import get_db_handle, get_collection_handle
from django.shortcuts import render
from django.http import HttpResponse

db_handle, mongo_client = get_db_handle("SGA","localhost","27017","", "")

def test1(request):
    collection_handle = get_collection_handle(db_handle, "Country")
    print(type(collection_handle))
    return HttpResponse("hello")
# Create your views here.

