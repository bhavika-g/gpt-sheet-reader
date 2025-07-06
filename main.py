from fastapi import FastAPI, Query
import gspread
import os
import json
from oauth2client.service_account import ServiceAccountCredentials
from fastapi.responses import FileResponse

app = FastAPI()

# Define the scope
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

# Load credentials from environment variable
creds_json = os.environ.get("GOOGLE_CREDENTIALS_JSON")
if creds_json is None:
    raise ValueError("Missing GOOGLE_CREDENTIALS_JSON environment variable")

creds_dict = json.loads(creds_json)
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

@app.get("/read_google_sheet")
def read_sheet(sheet_id: str, worksheet: str = "2.0G库存对接表Inventory%20detail"):
    try:
        sheet = client.open_by_key(sheet_id).worksheet(worksheet)
        data = sheet.get_all_records()
        return {"data": data}
    except Exception as e:
        return {"error": str(e)}

@app.get("/openapi.yaml", include_in_schema=False)
def serve_openapi_yaml():
    filepath = os.path.join(os.path.dirname(__file__), "openapi.yaml")
    return FileResponse(filepath, media_type="application/yaml")

