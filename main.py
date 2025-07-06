from fastapi import FastAPI, Query
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = FastAPI()

# Define the scope and load credentials
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]
creds = ServiceAccountCredentials.from_json_keyfile_name("/Users/bhavikagopalani/Downloads/doc_reader/key.json", scope)
client = gspread.authorize(creds)

@app.get("/read_google_sheet")
def read_sheet(sheet_id: str, worksheet: str = "2.0G库存对接表Inventory%20detail"):
    try:
        sheet = client.open_by_key(sheet_id).worksheet(worksheet)
        data = sheet.get_all_records()
        return {"data": data}
    except Exception as e:
        return {"error": str(e)}
