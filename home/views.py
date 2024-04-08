from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from deepface import DeepFace
import os
from django.conf import settings
import tempfile
import shutil
import pandas as pd

from .forms import UploadImageForm
from .models import Vaccinated

from django.contrib.auth.decorators import login_required
#import cv2

# Create your views here.
@login_required
def dashboard(request):
    template = loader.get_template('registration/dashboard.html')
    return HttpResponse(template.render())

def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())

def upload_image(request):
    if request.method == "POST":
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_img = request.FILES['image']

            #Save uploaded image in temp location
            temp_file_path = os.path.join(settings.MEDIA_ROOT, 'temp_image.jpg')
            with open(temp_file_path, 'wb') as temp_file:
                for chunk in uploaded_img.chunks():
                    temp_file.write(chunk)

            #Retrieve DB Instances
            vaccinated_instances = Vaccinated.objects.all()

            #Temp dir to store images
            temp_dir = tempfile.mkdtemp()

            for instance in vaccinated_instances:
                #Open image and store in temp location
                with open(os.path.join(temp_dir, f'{instance.id}.jpg'), 'wb') as temp_image_file:
                    temp_image_file.write(instance.image.read())

            results = []
            #ver = DeepFace.find(img_path=temp_file_path, db_path=temp_dir, model_name="Facenet")
            for image in os.listdir(temp_dir):
                img2 = os.path.join(temp_dir, image)
                result = DeepFace.verify(img1_path=temp_file_path, img2_path=img2)['verified']
                results.append(result)
            if any(results):
                return render(request, 'match_found.html')

            else:
                return render(request, 'match_not_found.html')
            #request.session['ver'] = ver

            #Clean Up
            shutil.rmtree(temp_dir)
            os.remove(temp_file_path)
    else:
        form = UploadImageForm()

    return render(request, 'upload_image.html', {'form': form})
"""
def display_result(request, ver):
    #retrieve ver data from session
    ver_data = request.session.get('ver', [])

    if isinstance(ver_data, list):
        return render(request, 'result.html', {'ver_data': ver_data})

    elif isinstance(ver_data, pd.DataFrame):
        return render(request, 'result.html', {'ver_data': ver_data})

    #Clear ver data toavoid stale data
    #del request.session['ver']
"""

def match_found(request):
    return render(request, 'match_found.html')

def match_not_found(request):
    return render(request, 'match_not_found.html')
 


    


