import csv
import io


def clean_csv_string(raw_csv_text):
    # io.StringIO tricks Python into treating a string like an actual open file
    input_stream = io.StringIO(raw_csv_text.strip())
    output_stream = io.StringIO()

    reader = csv.reader(input_stream)
    writer = csv.writer(output_stream, lineterminator="\n")

    # Read the header row first
    try:
        header = next(reader)
        writer.writerow([column.strip() for column in header])
    except StopIteration:
        return ""   # Return empty string if input is empty
    

    for row in reader:
        # Check if the row is completely empty or just full of spaces
        if not row or all(cell.strip() == "" for cell in row):
            continue

        # Clean every cell in the row
        cleaned_row = [cell.strip().upper() if i == 1 else cell.strip() for i, cell in enumerate(row)]
        writer.writerow(cleaned_row)

    return output_stream.getvalue()