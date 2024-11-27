from django.shortcuts import render, redirect
from django.http import HttpResponse
import os
from django.conf import settings
import pytesseract
from PIL import Image
from pathlib import Path
from django.contrib.auth.decorators import login_required
import pickle
import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
port_stem = PorterStemmer()
vectorization = TfidfVectorizer()

vector_form = pickle.load(open(os.path.join(settings.BASE_DIR, 'fakenews', 'vector.pkl'), 'rb'))
load_model = pickle.load(open(os.path.join(settings.BASE_DIR, 'fakenews', 'model.pkl'), 'rb'))

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def stemming(content):
    con=re.sub('[^a-zA-Z]', ' ', content)
    con=con.lower()
    con=con.split()
    con=[port_stem.stem(word) for word in con if not word in stopwords.words('english')]
    con=' '.join(con)
    return con

def fake_news(news):
    news=stemming(news)
    input_data=[news]
    vector_form1=vector_form.transform(input_data)
    prediction = load_model.predict(vector_form1)
    return prediction

@login_required(login_url='/sign-in/')
def home(request):
    return render(request, 'Home.html')

@login_required(login_url='/sign-in/')
def resultPage(request):
    return render(request, 'ResultPage.html')

@login_required(login_url='/sign-in/')
def textDetection(request):
    if request.method == 'POST':
        text = request.POST.get('my-sentence')
        prediction = fake_news(text)

        if prediction[0] == 0:
            res = 1
        else:
            res = 0
        
        return render(request, 'ResultPage.html', {
            'res':res,
            'sentence':text
        })
    
@login_required(login_url='/sign-in/')
def imageDetection(request):

    if request.method == 'POST':
        if 'image' not in request.FILES:
            return HttpResponse("No file uploaded!", status=400)

        image_file = request.FILES['image']

        if not image_file.name:
            return HttpResponse("No selected file.", status=400)

        # Save the uploaded image to a temporary file
        temp_image_path = "temp_image.png"
        with open(temp_image_path, 'wb') as temp_file:
            for chunk in image_file.chunks():
                temp_file.write(chunk)

        try:
            # Perform OCR on the image
            extracted_text = pytesseract.image_to_string(Image.open(temp_image_path))

            # Clean up the temporary image file
            os.remove(temp_image_path)

            # Render the extracted text in a new template
            prediction = fake_news(extracted_text)

            if prediction[0] == 0:
                res = 1
            else:
                res = 0
        
            return render(request, 'ResultPage.html', {
                'res':res,
                'sentence':extracted_text
            })

        except Exception as e:
            return HttpResponse(f"Error processing the image: {e}")
    else:
        return HttpResponse("Invalid request method.", status=405)


@login_required(login_url='/sign-in/') 
def dashboard(request):
    return render(request, 'dashboard.html')