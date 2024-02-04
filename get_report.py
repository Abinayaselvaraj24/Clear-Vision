import pandas as pd  # Import the pandas library
import pathlib  # Import the pathlib module


def generateReport(patID):
    df = pd.read_csv('out_csv.csv', names=['PatientID', 'Sex', 'Date', 'Eye Part',
                                           'Labels'])  # Read the CSV file into a pandas DataFrame

    report_fields = ["PatientID", "Sex", "Date", "Eye Part", "Labels"]  # Define a list of report fields
    if len(df):  # Check if the DataFrame is not empty
        exam = df.loc[df[
                          'PatientID'] == patID]  # Select rows from the DataFrame where the 'PatientID' column matches the given patient ID

        report_data = exam.iloc[0]  # Get the first row of the selected rows

        report_dict = {}  # Create an empty dictionary to store the report data
        for field in range(0, len(report_fields)):
            # Add the report field and its corresponding value to the dictionary
            report_dict[report_fields[field]] = str(report_data[field])

        image_path = pathlib.Path(f"image Database/{patID}.png")  # Create a Path object for the image path
        report_dict['image'] = str(image_path)  # Add the image path to the dictionary with the key 'image'


        return report_dict  # Return the report dictionary