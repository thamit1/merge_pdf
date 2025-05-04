# pdf_merge

`pdf_merge.py` is a Python script that reads all PDF files from the `input` directory and merges them into a single PDF file.

## How to Use

1. Place all the PDF files you want to merge into a folder named `input` in the same directory as the script.
2. Run the script using the following command:
    ```bash
    python pdf_merge.py
    ```
3. The merged PDF will be saved as `output.pdf` in the same directory as the script.

## Requirements

Make sure you have Python installed along with the `PyPDF2` library. You can install `PyPDF2` using pip:
```bash
pip install PyPDF2
```

## Example

If your `input` directory contains:
- `file1.pdf`
- `file2.pdf`
- `file3.pdf`

Running the script will generate a single file named `output.pdf` containing the contents of all three files in the order they appear in the `input` directory.

## Notes

- The script processes files in the order they are listed by the operating system.
- Ensure all files in the `input` directory are valid PDF files to avoid errors.
- The output file will overwrite any existing `merged_output.pdf` in the directory.
