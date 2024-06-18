# Description: command line python script to read in xml document and output a delimited file containing fields for each child of the root element labeled to include their parent elements from the xml tree
import sys
import xml.etree.ElementTree as ET
import csv
import os

def parse_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    return root

def extract_tags_and_data(root):
    tags = set()
    data = []

    def recurse(element, data_row, parent_tag_counts, parent_tag):
        for child in element:
            tag = child.tag
            
            # Update the count for this tag in the current path
            if tag in parent_tag_counts:
                parent_tag_counts[tag] += 1
            else:
                parent_tag_counts[tag] = 1

            # Create an indexed tag name with the parent tag as a prefix
            indexed_tag = f"{parent_tag}_{tag}_{parent_tag_counts[tag]}"
            text = child.text.strip() if child.text else ""
            
            # Add the indexed tag to the set of tags
            tags.add(indexed_tag)
            
            # Add the text content to the data row under the indexed tag
            data_row[indexed_tag] = text
            
            # Recurse into child elements with a copy of the current tag counts and the current tag as the parent
            recurse(child, data_row, parent_tag_counts.copy(), tag)

    # Iterate through each direct child of the root element
    for element in root:
        data_row = {}
        recurse(element, data_row, {}, root.tag)
        data.append(data_row)

    return tags, data

def write_delimited_file(output_path, tags, data, delimiter):
    with open(output_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=sorted(tags), delimiter=delimiter)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py input.xml")
        sys.exit(1)

    input_path = sys.argv[1]

    # Generate the output file name
    base_name = os.path.splitext(input_path)[0]
    output_path = f"{base_name}-delimited.txt"

    # Prompt the user for the delimiter they want to use
    delimiter = input("Please enter the delimiter you would like to use for the output file: ")

    root = parse_xml(input_path)
    tags, data = extract_tags_and_data(root)
    write_delimited_file(output_path, tags, data, delimiter)
    print("Delimited file written: " +output_path)

if __name__ == "__main__":
    main()
