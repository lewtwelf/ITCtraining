import json

# Sample validation function
def is_valid(record):
    # Check if required fields exist and are not empty
    return record.get("id") is not None and record.get("value") is not None

# Sample cleaning function
def clean_record(record):
    record["value"] = record["value"].strip() if isinstance(record["value"], str) else record["value"]
    record["timestamp"] = record.get("timestamp", "N/A")  # Fill missing timestamps
    return record

# Sample enrichment function
def enrich_record(record):
    record["value_length"] = len(record["value"]) if isinstance(record["value"], str) else 0
    record["processed"] = True  # Mark record as processed
    return record

# Generator for reading data source
def read_stream(file_path):
    with open(file_path, "r") as f:
        for line in f:
            yield json.loads(line)

# Data transformation pipeline
def transform_data(data):
    for record in data:
        if is_valid(record):         # Step 1: Filter invalid records
            cleaned_record = clean_record(record)   # Step 2: Clean record
            enriched_record = enrich_record(cleaned_record)  # Step 3: Enrich record
            yield enriched_record

# Save to output
def save_to_output(record, output_path):
    with open(output_path, "a") as f:
        f.write(json.dumps(record) + "\n")

# Usage Example
if __name__ == "__main__":
    input_file = "rawdata.json"  # Example input file
    output_file = "transformed_data.json"

    # Initialize transformed data generator
    transformed_data = transform_data(read_stream(input_file))

    # Process and save transformed records
    for record in transformed_data:
        save_to_output(record, output_file)

    print("Data transformation complete. Transformed records saved to:", output_file)

