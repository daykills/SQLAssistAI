import openai
from datetime import date
from jinja2 import Environment, FileSystemLoader
import os
import csv
import argparse
from datetime import datetime
import re

openai.api_key = ''


def call_chatgpt(prompt):
    """
    Function to call OpenAI's ChatGPT API.
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo-preview",
            messages=[{"role": "system", "content": "Your system message here, if any"},
                      {"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=2000
        )
        response_text = response.choices[0].message['content']
        return response_text
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def parse_response(response_text):
    """
    Placeholder for parsing the ChatGPT response.
    This will need to be adjusted according to the actual format of the response.
    """
    judgement_pattern = re.compile(
        r'- \*\*Correctness Judgment\*\*:\s*\n  - (\w+)\.')
    explanation_pattern = re.compile(
        r'- \*\*Explain the Query\*\*:\s*\n  - ([^\n]+)')
    suggestions_pattern = re.compile(
        r'- \*\*Suggestions for Improvement\*\*:\s*\n  - ([^\n]+)')

    # Search for each section using the defined regex patterns
    judgement_match = judgement_pattern.search(response_text)
    explanation_match = explanation_pattern.search(response_text)
    suggestions_match = suggestions_pattern.search(response_text)

    # Extract the matched text or use a fallback default value
    judgement = judgement_match.group(
        1) if judgement_match else "No judgement provided."
    explanation = explanation_match.group(
        1) if explanation_match else "No explanation provided."
    suggestions = suggestions_match.group(
        1) if suggestions_match else "No suggestions provided."

    # Construct and return a dictionary with the parsed content
    return {
        'judgement': judgement,
        'explanation': explanation.strip(),
        'suggestions': suggestions.strip(),
    }


def update_csv_row(row, parsed_response):
    """
    Update the CSV row with the parsed response from ChatGPT.
    """
    row['judgement'] = parsed_response['judgement']
    row['explanation'] = parsed_response['explanation']
    row['suggestions'] = parsed_response['suggestions']
    row['date'] = datetime.now().strftime("%Y-%m-%d")


def main(template_file_path) -> None:
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template(template_file_path)

    # Load CSV data
    csv_rows = []
    with open('query.csv', mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            csv_rows.append(row)

    # Interact with ChatGPT for each row
    for row in csv_rows:
        # Ensure 'id' and 'query' are used directly, as the template expects
        rendered_prompt = template.render(row=row)
        response_text = call_chatgpt(rendered_prompt)

        # Parse the response from ChatGPT
        parsed_response = parse_response(response_text)

        # Update the CSV row with the parsed response
        update_csv_row(row, parsed_response)

    # Write the updated data back to a new CSV file
    with open('query_updated.csv', 'w', newline='', encoding='utf-8') as file:
        fieldnames = ['id', 'query', 'judgement',
                      'explanation', 'suggestions', 'date']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        # Write the updated rows to a CSV
        writer.writerows(csv_rows)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Process some CSV data using a Jinja template.')
    parser.add_argument('template_file_path', type=str,
                        help='The path to the Jinja template file')
    args = parser.parse_args()

    main(args.template_file_path)
