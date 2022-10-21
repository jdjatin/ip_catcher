from django.shortcuts import render
from .models import Student
from .serializers import StudentSerializer
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.http import JsonResponse
import requests

# Create your views here.

@csrf_exempt
@api_view(['GET'])
def student_api(request):
    if request.method =='GET':
        students=Student.objects.all()
        serializerr=StudentSerializer(students,many=True)
        return JsonResponse({'students':serializerr.data})

@csrf_exempt
@api_view(['POST'])
def post_api(request):
    if request.method=='POST':
        serializerr=StudentSerializer(data=request.data)
        if serializerr.is_valid():
            serializerr.save()
            res={'msg':'Data Created'}
            json_data=JSONRenderer().render(res)
            return HttpResponse(json_data,content_type='application/json')
        json_data=JSONRenderer().render(serializerr.errors)
        return HttpResponse(json_data,content_type='application/json')
@csrf_exempt        
def display(request):
    URL=requests.get("http://127.0.0.1:8000/get/")
    data=URL.json()
    return render(request,'index.html',{'Student':data})

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return HttpResponse(ip)