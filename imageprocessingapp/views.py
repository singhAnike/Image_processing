from django.http import JsonResponse
from django.shortcuts import render
import cv2
import numpy as np

def upload_image(request):
    if request.method == 'POST':
        return render(request, 'upload_image.html')

    return render(request, 'upload_image.html')

def process_image(request):
    if request.method == 'POST':
        image_file = request.FILES.get('image')

        if image_file:
            try:
                image_data = cv2.imdecode(np.fromstring(image_file.read(), np.uint8), cv2.IMREAD_COLOR)

                color_ranges = {
                    'URO': ([0, 0, 0], [255, 255, 255]),  
                    'BIL': ([0, 0, 0], [255, 255, 255]),  
                    'KET': ([0, 0, 0], [255, 255, 255]),  
                    'BLD': ([0, 0, 0], [255, 255, 255]),  
                    'PRO': ([0, 0, 0], [255, 255, 255]),  
                    'NIT': ([0, 0, 0], [255, 255, 255]), 
                    'LEU': ([0, 0, 0], [255, 255, 255]),  
                    'GLU': ([0, 0, 0], [255, 255, 255]), 
                    'SG': ([0, 0, 0], [255, 255, 255]),   
                    'PH': ([0, 0, 0], [255, 255, 255])    
                }


                results = {}

                for category, (lower_bound, upper_bound) in color_ranges.items():
                    mask = cv2.inRange(image_data, np.array(lower_bound), np.array(upper_bound))
                    mean_color = cv2.mean(image_data, mask=mask)[:3]
                    results[category] = [int(c) for c in mean_color]

                return JsonResponse(results)

            except Exception as e:
                error_message = f"Error processing the image: {str(e)}"
                return JsonResponse({'error': error_message})


    return render(request, 'upload_image.html')