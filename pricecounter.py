import pypdfium2 as pdfium
import numpy as np
from .regression import pricePrediction
from concurrent.futures import ProcessPoolExecutor

def image_precount(img):
    w, h = img.size
    img = img.rotate(90, expand=True) if w > h else img
    resized_image = img.resize((2480, 3508))
    return resized_image

def countColorArea(img):
    img_array = np.array(img)
    color_pixels = np.all(img_array[:, :, :3] != img_array[:, :, :3].mean(axis=2, keepdims=True), axis=2)
    color_area = np.sum(color_pixels)
    total_pixels = img_array.shape[0] * img_array.shape[1]
    return round((color_area / total_pixels) * 100, 2)

def CountBlackArea(img):
    img_array = np.array(img)
    
    similiar_pixels = np.all(img_array[:, :, :3] == img_array[:, :, :3].mean(axis=2, keepdims=True), axis=2)
    total_similiar_pixels = np.sum(similiar_pixels)
    
    white_pixels = np.all(img_array[:, :, :3] == 255, axis=2)
    total_white_pixels = np.sum(white_pixels)
    
    bw_area = np.sum(total_similiar_pixels-total_white_pixels)
    total_pixels = img_array.shape[0] * img_array.shape[1]
    return round((bw_area / total_pixels) * 100, 2)

def priceCounter(img):
    color_area = countColorArea(img)
    print_area = color_area + CountBlackArea(img)
    return pricePrediction(color_area, print_area)

def process_page(page_number, pdf_path):
    pdf = pdfium.PdfDocument(pdf_path)
    page = pdf[page_number]
    image = page.render(scale=4).to_pil()
    image = image.convert('RGB')
    img = image_precount(image)
    return priceCounter(img)

def getprice(pdf_path):
    pdf = pdfium.PdfDocument(pdf_path)
    with ProcessPoolExecutor() as executor:
        futures = [executor.submit(process_page, i, pdf_path) for i in range(len(pdf))]
        harga_total = sum(future.result() for future in futures)
    return harga_total

def getpage(pdf_path):
    pdf = pdfium.PdfDocument(pdf_path)
    return len(pdf)
