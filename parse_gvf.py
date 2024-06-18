# Parse GVF files and return a list of variant information

def parse_gvf_file(gvf_file):

    variants = []
    with open(gvf_file, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith('##'):
                continue  # Skip metadata lines
            else:
                fields = line.split('\t')
                variant_type = fields[2]
                start = int(fields[3])  # Position
                end = int(fields[4])  # Position
                attributes = fields[8]
                attribute_pairs = attributes.split(';')

                # Initialize a dictionary to store variant information
                variant_info = {}

                for pair in attribute_pairs:
                    key, value = pair.split('=')
                    variant_info[key] = value

                # Access specific attributes from the dictionary
                variant_id = variant_info.get('ID', '')
                variant_sequence = variant_info.get('Variant_seq', '')
                allele = variant_info.get('Reference_seq', '')
                sn_id = variant_info.get('Dbxref', '').split(':')[1]

                # Store variant information in a structured format
                variant_data = {
                    'variant_id': variant_id,
                    'variant_sequence': variant_sequence,
                    'allele': allele,
                    'variant_type': variant_type,
                    'start': start,
                    'end': end,
                    'sn_id': sn_id
                }

                # Append variant_data to the list of variants
                variants.append(variant_data)

    return variants
