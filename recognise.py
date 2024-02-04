import csv
from tensorflow.keras.models import load_model
import pandas as pd
import pathlib
import numpy as np
from tensorflow.keras.preprocessing import image

# these we done in training phase
img_height = 224  # Set the desired height of the image
img_width = 224  # Set the desired width of the image
batch_size = 32  # Set the batch size for processing images

df = pd.read_csv('patient_record.csv')  # Read the patient record CSV file into a pandas DataFrame


def append_to_patient_record_csv(id, sex, selected_date, eye_part):
    # Append the provided information as a new row to the patient record CSV file
    with open("patient_record.csv", "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([id, sex, selected_date, eye_part])


def preprocess_image(image_path):
    # Preprocess the image by loading and resizing it
    img = image.load_img(image_path, target_size=(img_height, img_width))
    img = image.img_to_array(img)
    return img




def get_result_for_single_image(patientid):
    model = load_model('best_model.h5')  # Load the saved model
    # Create a Path object for the image path
    image_path = pathlib.Path(f"image Database/{patientid}.png")
    # Preprocess the image
    preprocessed_image = preprocess_image(str(image_path))
    # Make a prediction using the model
    prediction = model.predict(np.expand_dims(preprocessed_image, axis=0))
    # Get the predicted class
    predicted_class = np.argmax(prediction, axis=1)
    # Define the class labels
    class_labels = ['Mild', 'Moderate', 'No_DR', 'Proliferate_DR', 'Severe']
    predicted_label = class_labels[predicted_class[0]]  # Get the predicted label

    df = pd.read_csv('patient_record.csv')  # Read the patient record CSV file into a pandas DataFrame
    row_list = list(
        df.loc[df['PatientID'] == patientid].iloc[0])  # Get the row from the DataFrame for the given patient ID

    row_list.append(predicted_label)  # Append the predicted label to the row list


    with open("out_csv.csv", "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(row_list)  # Write the row list as a new row to the output CSV file
