# Run on web-server: uvicorn main:app --reload

from fastapi import FastAPI, Request, Form, File, UploadFile
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os
import io
import base64

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


app = FastAPI()

app.mount('/static', StaticFiles(directory='static'), name='static')

templates = Jinja2Templates(directory='templates')


@app.get('/')
async def root(request: Request, message='Hello, Coursera students'):
    # return {'message': 'Hello World'}
    return templates.TemplateResponse('index.html',
                                      {'request': request, 'message': message})


@app.post('/show_plot')
async def show_plot(request: Request, numbers: str = Form(...)):
    numbers = list(map(int, numbers.split(',')))

    fig = plt.figure()
    plt.plot(numbers)

    png_image = io.BytesIO()
    fig.savefig(png_image)
    png_image_b64_string = base64.b64encode(png_image.getvalue()).decode('ascii')

    return templates.TemplateResponse('plot.html',
                                      {'request': request,
                                       'numbers': numbers,
                                       'picture': png_image_b64_string})
