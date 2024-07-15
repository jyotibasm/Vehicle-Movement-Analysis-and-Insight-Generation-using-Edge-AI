import cv2
from ultralytics import YOLO
import pandas as pd


# Load dataframe
df = pd.read_excel('./Database/updates.xlsx')

# Load the YOLOv8 model
model = YOLO('./Weights/model_2.pt')

# Predict on a single image
image_path = './Test Images/Parking Area.jpg'
results = model.predict(image_path)

# Load the image using OpenCV
image = cv2.imread(image_path)

# Initialize counters for 'Full' and 'Empty' classes
full_count = 0
empty_count = 0

# Example of how to process results (the actual implementation may vary based on the results format)
for result in results:
    for detection in result.boxes:
        bbox = detection.xyxy[0].tolist()  # [x1, y1, x2, y2]
        confidence = detection.conf[0].item()
        class_id = detection.cls[0].item()
        class_name = model.names[int(class_id)]

        # Increment the appropriate counter
        if class_name == 'Full':
            full_count += 1
        elif class_name == 'Empty':
            empty_count += 1

        # Set the color based on the class name (BGR format for OpenCV)
        color = (0, 255, 0) if class_name == 'Empty' else (0, 0, 255)

        # Draw the rectangle
        x1, y1, x2, y2 = map(int, bbox)
        cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)

        # Add the class label and confidence score
        label = f'{class_name} ({confidence:.2f})'
        label_size, base_line = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        y1_label = max(y1, label_size[1] + 10)
        cv2.rectangle(image, (x1, y1_label - label_size[1] - 10), (x1 + label_size[0], y1_label + base_line - 10), color, cv2.FILLED)
        cv2.putText(image, label, (x1, y1_label - 7), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        # display number slots with Full and Empty slots 
        print(f'Occupied = {full_count}, Available = {empty_count}')

        # upadate chages to database(Excel Sheet)
        df.loc[0, 'Full'] = full_count
        df.loc[0,'Empt'] = empty_count
        df.to_excel('./Database/updates.xlsx', index=False)


# Display the image using OpenCV
cv2.imshow('Image', image)
cv2.waitKey(0)
cv2.destroyAllWindows()

