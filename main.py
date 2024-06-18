import requests
from parse_gvf import parse_gvf_file
from bs4 import BeautifulSoup
import mysql.connector
from dotenv import load_dotenv
import os
import time

load_dotenv()

db_user = os.getenv('DB_USER')
db_host = os.getenv('DB_HOST')
db_password = os.getenv('DB_PASSWORD')
db_port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')

cnx = mysql.connector.connect(user=db_user,
                              host=db_host,
                              password=db_password,
                              port=db_port,
                              database=db_name)
cursor = cnx.cursor()


def query_dbSNP(rs_id):
    # Get sample size, ref allele, and alt allele
    url = f"https://www.ncbi.nlm.nih.gov/snp/{rs_id}"
    response = requests.get(url)

    if response.status_code == 200:
        # Get HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        # Initialize variables to store extracted data
        data = {}

        # Find all <dt> and <dd> pairs within <dl class="usa-width-one-half">
        dl_element = soup.find('dl', class_='usa-width-one-half')
        div_element = soup.find('div', class_='popfreq_table')

        if dl_element:
            dt_elements = dl_element.find_all('dt')
            dd_elements = dl_element.find_all('dd')

            # Loop through <dt> and <dd> pairs
            # Use zip because there are multiple elements
            for dt, dd in zip(dt_elements, dd_elements):
                dt_text = dt.get_text(strip=True)
                dd_text = dd.get_text(strip=True)

                # Store data in dictionary, data['Title'] = 'value'
                data[dt_text] = dd_text

        # This is where the sample size and frequency is derived from
        # A table with class 'popfreq_table' contains the sample size and allele frequencies
        if div_element:
            td_element = div_element.find_all(
                'td', class_=['samp_s', 'popfreq_ref_allele', 'popfreq_alt_allele'])
            # Define custom keys for the data
            keys = ['Sample Size', 'Ref Allele', 'Alt Allele']
            for key, td in zip(keys, td_element):
                td_text = td.get_text(strip=True)
                data[key] = td_text

        return data  # Return the extracted data dictionary
    else:
        print(
            f"Error fetching data: {response.status_code} - {response.reason}")
        return None  # Return None if there's an error


def main():
    # Shortened data
    print("Example: ./genetic-variant-annotation/homo_sapiens-chrY-short.gvf")
    gvf_file = input(str("Insert the filepath of your GVF file: "))

    # Parse GVF file and extract variant information
    variants = parse_gvf_file(gvf_file)

    print('Query started, this may take a while...')

    for variant in variants:

        rs_id = variant['rs_id']
        dbSNP_annotation = query_dbSNP(rs_id)  # Get the annotation

        time.sleep(1)  # Send request every 1 second

        frequency = dbSNP_annotation.get('Frequency', 'N/A')

        # formatting by remove whitespace and adding newline
        frequency = frequency.replace(' ', '')
        frequency = frequency.replace('\n', '')
        frequency = frequency.replace(")", ")\n")

        # adding extra information from dbSNP
        position = dbSNP_annotation.get('Position', 'N/A')
        sample_size = dbSNP_annotation.get('Sample Size', 'N/A')
        ref_allele = dbSNP_annotation.get('Ref Allele')
        alt_allele = dbSNP_annotation.get('Alt Allele')

        # Store or process annotation results
        variant['frequency'] = frequency
        variant['position'] = position.split('(')[0]
        variant['sample_size'] = sample_size
        variant['ref_allele'] = ref_allele
        variant['alt_allele'] = alt_allele

        # Table name and column names
        add_variant = ("INSERT INTO `genetic_variants` "
                       "(variant_id, rs_id, variant_sequence, allele, position, sample_size, ref_allele, alt_allele) "
                       "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")

    print("DATABASE INSERTING STARTED")
    # # # Example: Print or further process the extracted information
    for variant in variants:

        data_variant = (variant['variant_id'], variant['rs_id'], variant['variant_sequence'], variant['allele'],
                        variant['start'], variant['sample_size'], variant['ref_allele'], variant['alt_allele'])

        # Insert the variant data into the database
        try:
            cursor.execute(add_variant, data_variant)
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            continue
        cnx.commit()  # Commit changes to database


if __name__ == "__main__":
    main()


# Optional for printing information

# print(variant)
# print(f"Variant ID: {variant['variant_id']}")
# print(f"RS ID: {variant['rs_id']}")
# print(f"Variant Sequence: {variant['variant_sequence']}")
# print(f"Allele: {variant['allele']}")
# print(
#     f"Type: {variant['variant_type']}, Start: {variant['start']}, End: {variant['end']}")
# print(f"Frequency:\n{variant['frequency']}")
# print(f"Position: {variant['position']}")

# print("-" * 50)  # Separator for readability
