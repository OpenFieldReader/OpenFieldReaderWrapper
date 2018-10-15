"""
    openfieldreaderwrapper is a light wrapper around the openfieldreader command line tool to automatically detect paper-based form fields.
"""

import os
import json
import tempfile
import subprocess

import cv2

def find_fields(orig, resize_width = 800):
    """
        Description: find fields in the image
        Parameters:
            - orig: opencv image.
            - resize_width: recommanded 800 pixels (openfieldreader assume the page has certain pixels size)
        Returns: (returncode, fields)
            - returncode can be:
                - 0 = success,
                - 1 = unknown error
                - 10 = Too many junctions. The image seem too complex.
                - 30 = Too much solution.
                - 20 = This should not happen in normal condition. (Please open an issue on GitHub with your image if it happens.)
            - fields:
                - This value can be None if nothing has been found or an error occured.
                - Structure: [[field1_cell1_opencv_img, field1_cell2_opencv_img, ...], [field2_cell1_opencv_img, field2_cell2_opencv_img, ...], ...]
    """

    # Preprocess image.
    img = orig
    height, width, _ = img.shape
    if width > resize_width:
        resize_height = int(resize_width * height / width)
        img = cv2.resize(img, (resize_width, resize_height))
        orig = cv2.resize(orig, (resize_width, resize_height))

    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 33, 4)
    img = cv2.bitwise_not(img)
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (2, 2))
    img = cv2.dilate(img, kernel)
    img = cv2.bitwise_not(img)

    # Start openfieldreader
    
    img_with_preprocessing = img
    path_file_temp = tempfile.NamedTemporaryFile(suffix='.jpg').name
    cv2.imwrite(path_file_temp, img_with_preprocessing)
    os.environ['DOTNET_CLI_TELEMETRY_OPTOUT'] = '1'
    temp_file_output = tempfile.NamedTemporaryFile().name
    p = subprocess.Popen(
        [
            "openfieldreader",
            "--input",
            path_file_temp,
            "--max-solutions",
            "100000",
            "--output",
            temp_file_output
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    _ = p.wait()
    results = (p.returncode, json.load(open(temp_file_output))['Boxes'] if p.returncode == 0 else None)
    if p.returncode == 0:
        os.remove(temp_file_output)
    os.remove(path_file_temp)

    # Process output and return images

    fields = results[1]
    fields_img = []

    if fields is not None:
        resize_w = 800
        height, width = img.shape[:2]
        ratio_w = 1.0
        ratio_h = 1.0
        if width > resize_w:
            resize_height = resize_w * height / width
            ratio_w = width / resize_w
            ratio_h = height / resize_height

        for field in fields:
            cells = []
            for cell in field:
                x1 = int(min(cell['TopLeft']['X'], cell['BottomLeft']['X']) * ratio_w)
                y1 = int(min(cell['TopLeft']['Y'], cell['TopRight']['Y']) * ratio_h)
                x2 = int(max(cell['TopRight']['X'], cell['BottomRight']['X']) * ratio_w)
                y2 = int(max(cell['BottomLeft']['Y'], cell['BottomRight']['Y']) * ratio_h)
                sub_img = orig[y1:y2, x1:x2]
                cells.append(sub_img)
            fields_img.append(cells)

    return (p.returncode, fields_img)
