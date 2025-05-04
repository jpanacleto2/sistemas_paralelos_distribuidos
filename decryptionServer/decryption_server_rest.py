from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from vigenere import vigenere_decrypt

app = FastAPI(title="Crypto API - Vigenère Cipher")

class DecryptRequest(BaseModel):
    text: str
    key: str

class DecryptResponse(BaseModel):
    result: str

@app.post("/decrypt", response_model=DecryptResponse)
def decrypt(request: DecryptRequest):
    try:
        result = vigenere_decrypt(request.text, request.key)
        return DecryptResponse(result=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na codificação: {str(e)}")
