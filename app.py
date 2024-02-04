import streamlit as st  # for building the web application
import PIL  # for image processing tasks
import PIL.Image  # for working with images
from datetime import date  # for working with dates
import os  # for interacting with the operating system
import base64  # for encoding and decoding binary data
import pandas_profiling  # for generating data visualizations and summaries
import streamlit.components.v1 as components  # for rendering HTML components
import pandas as pd  # for data manipulation and analysis
from fpdf import FPDF  # for creating PDF files
# create the files
# here we created get_report.py it is importing this and accesing the function
from get_report import generateReport
# here we created recognise.py it is importing this
from recognise import get_result_for_single_image,append_to_patient_record_csv

df = pd.read_csv('out_csv.csv')  # Replace with your file path
# Extract the 'PatientID' column values and convert them to a list
patient_id = list(df['PatientID'])


def predict():
    st.title("Diabetic Retinopathy Report Tool")
    st.write("Please provide the necessary information and upload an image.")

    # Add user input fields
    id = st.text_input("ID")  # Create a text input field for ID
    sex = st.selectbox("Sex", ["Male", "Female"])  # Create a dropdown selectbox for sex
    age = st.slider("Age", 1, 100)  # Create a slider for age
    selected_date = st.date_input("Select a date", date.today())  # Create a date input field
    eye_part = st.selectbox("Eye Part", ['Left Eye', 'Right Eye'])  # Create a dropdown selectbox for eye part

    # Add image upload option
    uploaded_image = st.file_uploader("Upload an image",
                                      type=["jpg", "jpeg", "png"])  # Create a file uploader for images

    # Check if an image has been uploaded
    if uploaded_image is not None:
        # Read the uploaded image
        image = PIL.Image.open(uploaded_image)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        # Generate a random filename
        filename = id + ".png"

        # Save the image to the "image Database" directory
        image.save(os.path.join("image Database", filename))
        st.write("Image saved successfully.")
        # Call the append_to_patient_record_csv function
        append_to_patient_record_csv(id, sex, selected_date, eye_part)
    # if predict button is pressed
    if st.button("Predict"):
        #to store data in csv and image db
        get_result_for_single_image(id)  # redirects to recognise.py
        response = generateReport(id)  # # redirects to get_report.py
        render_report(response)  # Call the render_report function in this file


def create_download_link(val, filename):
    b64 = base64.b64encode(val)  # Encode the value in base64 format
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="{filename}.pdf">Download Report</a>'


def render_report(rep_data):
    # Create an instance of the FPDF class
    pdf = FPDF()
    # Add a new page to the PDF document
    pdf.add_page()
    # Set the font to Arial, bold, size 16
    pdf.set_font('Arial', 'B', 16)
    pdf.multi_cell(300, 20, '            AI generated Diabetes Retinopathy Report', 0, 3)

    pdf.line(0, 30, pdf.w, 30)  # Draw a line at the specified coordinates
    # Remove the 'image' key from the dictionary and assign its value to rep_image

    rep_image = rep_data.pop('image')

    # Add the image to the PDF at the specified coordinates

    pdf.image(rep_image, 150, 40, 50, type='png')

    # Iterate over the remaining key-value pairs in rep_data
    for key, value in rep_data.items():
        text = key + '   :     ' + value  # Create a text string with the key-value pair
        pdf.set_font('Arial', '', 12)  # Set the font to Arial, size 12
        pdf.multi_cell(300, 15, text, 0, 1)  # Add the text to the PDF
    # Convert the PDF output to base64 format
    base64_pdf = base64.b64encode(pdf.output(dest="S").encode("latin-1")).decode('utf-8')
    pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf">'
    # Display the PDF in Streamlit
    st.markdown(pdf_display, unsafe_allow_html=True)
    # Create a download link for the PDF
    html = create_download_link(pdf.output(dest="S").encode("latin-1"), "Report")
    # Display the download link in Streamlit
    st.markdown(html, unsafe_allow_html=True)


def report():
    st.header('Reports')
    st.write('The Diabetes Retinopathy report generated by the AI Inference Engine can be viewed here and downloaded')
    rep_patientId = st.selectbox('Select Patient ID for generating the report', patient_id)

    if st.button('Get Report'):
        report = generateReport(rep_patientId)  # redirects to get_report.py
        render_report(report)  # Call the render_report function


def home():
    st.write("Service providing simplified retinopathy diagnosis by enabling easy scan uploads and providing AI-generated predictions.")
    st.write("AI-based solution ensures high diagnostic accuracy, delivering precise and objective results for retinopathy diagnosis.")
    st.write("AI-based  solution streamlines the diagnostic process, saving time and improving efficiency.")
    st.write("AI Model is featured with Automated tasks which enable scalability, allowing for the processing of a large number of scans.")

def dashboard():
    st.title('Get Data Summary of all Images in Database')
    st.write('Generating a Batch summary and getting results of all images in the database')
    runbatch = st.button("Run batch inference")

    if runbatch:
        data = pd.read_csv('out_csv.csv')  # Replace with your own file path

        # Generate pandas profiling report
        report = pandas_profiling.ProfileReport(data, title='Data Visualisation Report')

        # Display the report in Streamlit
        st.title('Data Summary')
        #print(report)
        components.html(report.to_html(), height=1000, width=800, scrolling=True)


def main():
    st.sidebar.image('template/nav.png')  # Display an image in the sidebar
    st.sidebar.write('Welcome to AI Medical Imaging Application')  # Write a text in the sidebar
    opt = st.sidebar.selectbox("Go to page:", ['Home', 'Prediction', 'Report',
                                               'Dashboard'])  # Create a dropdown selectbox for page selection
    st.image('template/main.png')  # Display an image in the main area
    st.title('AI Medical Imaging Application')  # Write a title in the main area

    if opt == 'Home':
        home()  # Call the home function
    if opt == 'Prediction':
        predict()  # Call the predict function
    if opt == 'Report':
        report()  # Call the report function
    if opt == 'Dashboard':
        dashboard()  # Call the dashboard function


if __name__ == "__main__":
    main()  # Call the main function