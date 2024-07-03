from fastapi import FastAPI, File, UploadFile, Form
from ai import get_details
from utils import encode_image

app = FastAPI()


@app.post("/process/")
async def process_image_and_text(
    image: UploadFile = File(...), 
    question: str = Form("Is this an aadhar card?"), 

) -> dict:
    await image.seek(0)
    encoded_image = encode_image(await image.read())
    prompt_question = f"{question} Analyze the provided image to extract details: for Aadhaar (full or half-sized) return 'aadhaar_number (without spaces)', 'name', and 'date of birth (dob)' which is mentioned just below the name in the format 'DD/MM/YYYY' for PAN return 'pan_number' and 'name'; return an empty JSON object for any other document."
    details = get_details(encoded_image, prompt_question)
    print(details)

    return {"details":details}
