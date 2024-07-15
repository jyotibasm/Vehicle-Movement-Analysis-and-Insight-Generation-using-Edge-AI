import cv2
from ultralytics import YOLO
import pytesseract
import pandas as pd
import re


# Read the Excel file
df = pd.read_excel('./Database/updates.xlsx')

# Load the YOLOv8 model
model = YOLO('./Weights/model_1.pt')

# Path to the tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Update this path if necessary

# Predict on a single image
image_path = './Test images/Vehicle Out.jpeg'
results = model.predict(image_path)

# Load the image
image = cv2.imread(image_path)

# Initialize counters for VIN and VOUT
vin_count = 0
vout_count = 0


# Cleaning of license plate 
def remove_special_characters(input_string):
    # Define the pattern to match any character that is not alphanumeric or whitespace
    pattern = r'[^a-zA-Z0-9\s]'
    
    # Use re.sub to replace occurrences of the pattern with an empty string
    clean_string = re.sub(pattern, '', input_string)
    
    return clean_string


# Process each result from YOLOv8 predictions
for result in results:
    for detection in result.boxes:
        bbox = detection.xyxy[0].tolist()  # [x1, y1, x2, y2]
        confidence = detection.conf[0].item()
        class_id = detection.cls[0].item()
        class_name = model.names[int(class_id)]

        # Extract coordinates
        x1, y1, x2, y2 = map(int, bbox)
        width = x2 - x1
        height = y2 - y1

        # Perform specific actions based on class name
        if class_name == 'Vin':
            vin_count += 1
        elif class_name == 'Vout':
            vout_count += 1

        # OCR 
        # Crop the license plate region from the image
        plate_image = image[y1:y1+height, x1:x1+width]

        # Optional: Preprocess the cropped image
        gray = cv2.cvtColor(plate_image, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # Perform OCR using Tesseract
        text = pytesseract.image_to_string(binary, config='--psm 8')
        # Print the extracted text
        print("Detected License Plate Number:", remove_special_characters(text.strip()))

        # Draw the bounding box
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 255), 2)

        # Annotate the image with class name and confidence score
        label = f'{class_name} ({confidence:.2f})'
        label_size, base_line = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        top = max(y1, label_size[1])
        cv2.rectangle(image, (x1, top - label_size[1]), (x1 + label_size[0], top + base_line), (255, 255, 255), cv2.FILLED)
        cv2.putText(image, label, (x1, top), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

# Print the counts of VIN and VOUT classes
print(f"Number of VIN classes detected: {vin_count}")
print(f"Number of VOUT classes detected: {vout_count}")

# Update a value in the DataFrame
df.loc[0, 'Vin'] = vin_count
df.loc[0, 'Vout'] = vout_count
df.to_excel('./Database/updates.xlsx', index=False)


# Display the image with annotations
cv2.imshow('YOLOv8 Predictions', image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Save the annotated image
cv2.imwrite('annotated_image_3.jpg', image)
