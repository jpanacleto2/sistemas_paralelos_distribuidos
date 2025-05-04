from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from vigenere import vigenere_encrypt

app = FastAPI(title="Crypto API - Vigenère Cipher")

class EncryptRequest(BaseModel):
    text: str
    key: str

class EncryptResponse(BaseModel):
    result: str

@app.post("/encrypt", response_model=EncryptResponse)
def encrypt(request: EncryptRequest):
    try:
        result = vigenere_encrypt(request.text, request.key)
        return EncryptResponse(result=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na codificação: {str(e)}")
