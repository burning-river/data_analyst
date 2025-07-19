from fastapi import FastAPI, Request, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
import shutil
import os
from analyst import Analyst
import uvicorn
import tempfile
import openai

openai.api_key = "**"

app = FastAPI(title="Data Analysis Platform")
templates = Jinja2Templates(directory="templates")

# We will store uploaded files temporarily in a folder "uploads"
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload")
async def upload_csv_file(csvFile: UploadFile = File(...)):
    # Accept only CSV files by content type and filename extension
    if not (csvFile.filename.endswith('.csv') or csvFile.content_type in ['text/csv', 'application/vnd.ms-excel']):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a CSV file.")

    file_location = os.path.join(UPLOAD_DIR, csvFile.filename)
    # Save uploaded file to disk temporarily
    try:
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(csvFile.file, buffer)
    except Exception:
        raise HTTPException(status_code=500, detail="Error saving uploaded file.")

    analyst = Analyst()
    try:
        analyst.upload_csv(file_location)
        data_size = analyst.get_data_size()
        data_types = analyst.get_column_data_types()
        missing_values = analyst.get_missing_values_count()
        numeric_stats = analyst.get_numeric_column_stats()
        categorical_stats = analyst.get_categorical_column_stats()
 
    except Exception as e:
        # Clean up uploaded file on error
        if os.path.exists(file_location):
            os.remove(file_location)
        raise HTTPException(status_code=400, detail=str(e))

    # Clean up uploaded file after use
    if os.path.exists(file_location):
        os.remove(file_location)

    # Compose response JSON
    response_json = {
        "data_size": data_size,
        "data_types": data_types,
        "missing_values": missing_values,
        "numeric_stats": numeric_stats,
        "categorical_stats": categorical_stats
    }

    prompt = f"""
    Prepare a report using the following dictonary: {response_json}.
    DO NOT display any tables, text only.
    State the size of the dataset.
    State the number of categorical columns.
    State the number of numerical columns.
    """
    response = openai.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": prompt}

    ],
    temperature=0.5
)

    report = response.choices[0].message.content.strip()
    #print(report)
    response_json['report'] = report
    return JSONResponse(content=response_json) 

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8080, reload=True)
# Note: To run the app do: uvicorn app:app --reload
# Client interface is at http://localhost:8000/ which serves output/templates/index.html
# The endpoint /upload accepts the CSV file and returns JSON with analysis results per specifications.
