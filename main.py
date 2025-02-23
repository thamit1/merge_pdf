from fastapi import FastAPI, File, UploadFile, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse, StreamingResponse
from PyPDF2 import PdfMerger
from typing import List
import os
import uuid
import tempfile

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def main():
    """
    Serves the main HTML page where users can select and upload PDF files.
    """
    return """
    <html>
        <head>
            <title>Merge PDF Files</title>
        </head>
        <body>
            <h3>Select PDF files to merge:</h3>
            <form action="/merge" method="post" enctype="multipart/form-data">
                <input type="file" name="files" multiple>
                <input type="submit" value="Submit">
            </form>
        </body>
    </html>
    """

@app.post("/merge")
async def merge(files: List[UploadFile] = File(...)):
    """
    Endpoint to handle the merging of uploaded PDF files.
    
    Args:
        files (List[UploadFile]): List of uploaded PDF files.

    Returns:
        RedirectResponse: Redirects to the success page with the merged PDF link.
        HTMLResponse: Error message if an exception occurs.
    """
    if len(files) < 2:
        raise HTTPException(status_code=400, detail="At least two PDF files are required for merging.")

    merger = PdfMerger()
    temp_dir = tempfile.gettempdir()
    output_filename = os.path.join(temp_dir, f"{uuid.uuid4()}.pdf")
    temp_files = []

    try:
        # Save uploaded files temporarily and append to merger
        for file in files:
            if file.content_type != "application/pdf":
                raise HTTPException(status_code=400, detail="Only PDF files are allowed.")
            temp_file_path = os.path.join(temp_dir, f"{uuid.uuid4()}" + file.filename)
            print(temp_file_path)
            with open(temp_file_path, "wb") as f:
                f.write(file.file.read())
            merger.append(temp_file_path)
            temp_files.append(temp_file_path)

        # Write the merged PDF to the output file
        merger.write(output_filename)
        merger.close()

        # Redirect to success page with download link
        return RedirectResponse(url=f"/success?filename={os.path.basename(output_filename)}", status_code=303)

    except Exception as e:
        # Return error message if an exception occurs
        return HTMLResponse(content=f"<h3>Error: {str(e)}</h3>")

    finally:
        # Clean up temporary files
        for temp_file in temp_files:
            os.remove(temp_file)

@app.get("/success", response_class=HTMLResponse)
async def success(request: Request, filename: str):
    """
    Serves the success page with a download link for the merged PDF file.

    Args:
        request (Request): The request object.
        filename (str): Name of the merged PDF file.

    Returns:
        HTMLResponse: Success message with a download link.
    """
    return f"""
    <html>
        <head>
            <title>Merge PDF Files - Success</title>
        </head>
        <body>
            <h3>Processing Complete!</h3>
            <p>The PDF files have been successfully merged.</p>
            <a href="/download/{filename}">Download Merged PDF</a>
        </body>
    </html>
    """

@app.get("/download/{filename}", response_class=FileResponse)
async def download_file(filename: str):
    """
    Endpoint to handle downloading of the merged PDF file.

    Args:
        filename (str): Name of the merged PDF file.

    Returns:
        FileResponse: The merged PDF file for download.
    """
    try:
        temp_dir = tempfile.gettempdir()
        file_path = os.path.join(temp_dir, filename)

        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not found.")
        
        def iterfile():
            with open(file_path, mode="rb") as file_like:
                yield from file_like
            os.remove(file_path)

        return StreamingResponse(iterfile(), media_type="application/pdf",\
             headers={"Content-Disposition": f"attachment; filename={filename}"})
    except Exception as e:
        return HTMLResponse(content=f"<h3>Error: {str(e)}</h3>")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="debug", reload=True)

