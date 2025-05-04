import os
import PyPDF2

def merge_pdfs(folder_path, output_filename):
    pdf_merger = PyPDF2.PdfMerger()

    # Get all PDF files in the folder
    pdf_files = [f for f in os.listdir(folder_path) if f.endswith(".pdf")] # Using list comprehension to filter pdf files
    pdf_files.sort()  # Optional: Sort files alphabetically

    for pdf in pdf_files:
        pdf_merger.append(os.path.join(folder_path, pdf))

    pdf_merger.write(os.path.join(folder_path, output_filename))
    pdf_merger.close()
    print(f"Merged {len(pdf_files)} PDFs into {output_filename}")

# Example usage
folder = "input"  # Replace with your relative or absolute folder path
output_pdf = "merged_output.pdf"
merge_pdfs(folder, output_pdf)
