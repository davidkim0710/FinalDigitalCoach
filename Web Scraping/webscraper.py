import requests
from bs4 import BeautifulSoup
import pandas as pd
import re


companies_url="https://prepinsta.com/interview-preparation/company-wise-interview-questions/"
cr = requests.get(companies_url)
soup1 = BeautifulSoup(cr.text, 'html.parser')
company_names = soup1.find_all('div', class_='elementor-widget-container')
c_text = []
for item in company_names:
    c_text.append(item.get_text())
company_string = ' '.join(c_text).strip()
#print(company_string)
# Extract company names using regex
company_names = re.findall(r"(\w+\s*\w*) Interview Questions", company_string)
company_names = [item for item in company_names if item != ""]
company_names = [item for item in company_names if "Companies" not in item and "Common" not in item and "specific" not in item]
company_names = list(set(company_names))
sorted(company_names, key=str.lower)
lines = company_names
# Initialize variables to store parsed data
companies = []
technical_interviews = []
hr_interviews = []

# Iterate over lines to parse the data
for line in lines:
    # Remove leading and trailing whitespaces
    line = line.strip()
    
    # Skip empty lines
    if not line:
        continue
    
    # Check if the line contains "Technical" or "HR" to determine the type of data
    if "Technical" in line:
        technical_interviews.append(line)
    elif "HR" in line:
        hr_interviews.append(line)
    else:
        companies.append(line)


# Print the parsed data
print("Companies:")
print(companies)
print("\nTechnical Interviews:")
print(technical_interviews)
print("\nHR Interviews:")
print(hr_interviews)
# Print the extracted company names
for name in companies:
    print(name)
    
    # URL of the webpage you want to scrape
    url = "https://prepinsta.com/interview-preparation/company-wise-interview-questions/"+ name + "/"

    # Send HTTP request to the specified URL and save the response from server in a response object called r
    r = requests.get(url)

    # Create a BeautifulSoup object and specify the parser
    soup = BeautifulSoup(r.text, 'html.parser')

    # Extract the desired information
    # (Replace 'div' and 'class_' with the HTML element and class of the data you want to scrape)
    data = soup.find_all('div', class_='elementor-widget-container')

    data_text = []
    for item in data:
        data_text.append(item.get_text())

    # Join all the items in the list into one string, separated by a space
    data_string = ' '.join(data_text)

    question_data = data_string.strip().split("Question ")[1:]
    # Initialize lists to store parsed data
    questions = []
    answers = []

    # Iterate over each question data
    for question_item in question_data:
        # Split each question item into question and answer
        parts = question_item.split("Answer")
        #print(parts)
        question = parts[0].split(":-")[1].strip()
        answer = parts[1].strip() if len(parts) > 1 else ""

        if answer.startswith(':'):
        # Remove the first character if it's a colon
            modified_answer = answer[1:]
        else:
            modified_answer = answer
        if "Read more at" in modified_answer:
            modified_answer = modified_answer.split("Read more at")[0]

        # Split the modified string based on new line character and take the first part
        modified_answer = modified_answer.split("\n")[0]
        # Append parsed data to lists
        questions.append(question)
        answers.append(modified_answer)

    # Create a DataFrame using pandas
    df = pd.DataFrame({'Question': questions, 'Answer': answers})

    # Write DataFrame to a CSV file
    csv_filename = name + '_interview_questions.csv'
    df.to_csv(csv_filename, index=False)

    print(f"CSV file '{csv_filename}' has been created successfully.")
