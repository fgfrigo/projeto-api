from fastapi import APIRouter, Depends, HTTPException
import requests

from app.core.auth import require_auth  # seu dependency que valida Bearer JWT

router = APIRouter(prefix="/external", tags=["external"])

@router.get("/cep/{cep}")
def lookup_cep(cep: str, _claims=Depends(require_auth)):
    clean = "".join([c for c in cep if c.isdigit()])

    if len(clean) != 8:
        raise HTTPException(status_code=400, detail="CEP inválido (precisa ter 8 dígitos)")

    url = f"https://viacep.com.br/ws/{clean}/json/"
    r = requests.get(url, timeout=10)
    r.raise_for_status()

    data = r.json()
    if data.get("erro") is True:
        raise HTTPException(status_code=404, detail="CEP não encontrado")

    # devolve direto (ou filtre campos se quiser)
    return data

