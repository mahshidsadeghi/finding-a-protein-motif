import re
import requests


INPUT_FILE = "/Users/mahshidsadeghi/Downloads/rosalind_mprt (3).txt"


def fetch_protein_sequence(uniprot_id):
    # Extract the base ID (remove any descriptors after an underscore)
    base_id = uniprot_id.split('_')[0]
    url = f"https://www.uniprot.org/uniprot/{base_id}.fasta"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch data for {uniprot_id}")
        return None
    fasta_data = response.text
    # Remove header and join sequence lines
    sequence = "".join(fasta_data.splitlines()[1:])
    return sequence

def find_nglycosylation_motif(sequence):
    # Define the N-glycosylation motif regex
    motif_pattern = r'N(?=[^P][ST][^P])'
    return [match.start() + 1 for match in re.finditer(motif_pattern, sequence)]

def main(input_file):
    input_file = input_file
    try:
        with open(input_file, 'r') as file:
            uniprot_ids = [line.strip() for line in file if line.strip()]
            
            if len(uniprot_ids) > 15:
                print("Please provide at most 15 UniProt IDs.")
                return
            
            for uniprot_id in uniprot_ids:
                sequence = fetch_protein_sequence(uniprot_id)
                if sequence:
                    locations = find_nglycosylation_motif(sequence)
                    if locations:
                        print(uniprot_id)
                        print(" ".join(map(str, locations)))
    except FileNotFoundError:
        print("The specified file was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main(INPUT_FILE)