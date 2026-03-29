import os
import pandas as pd
from fastapi import FastAPI, UploadFile, HTTPException, Request, Query
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from classify import classify

app = FastAPI()
templates = Jinja2Templates(directory="templates")

if not os.path.exists("resources"):
    os.makedirs("resources")

@app.get("/", response_class=HTMLResponse)
async def main_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/classify/")
async def classify_logs(file: UploadFile, mode: str = Query("download")):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV.")
    
    try:
        df = pd.read_csv(file.file)
        if "source" not in df.columns or "log_message" not in df.columns:
            raise HTTPException(status_code=400, detail="CSV must contain 'source' and 'log_message' columns.")
        
        # Core classification logic
        df["target_label"] = classify(list(zip(df["source"], df["log_message"])))
        
        if mode == "view":
            # Return top 50 rows for the Glass UI table
            return {"data": df.head(50).to_dict(orient="records")}
        
        output_file = "resources/output.csv"
        df.to_csv(output_file, index=False)
        return FileResponse(output_file, media_type='text/csv', filename="classified_results.csv")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        file.file.close()