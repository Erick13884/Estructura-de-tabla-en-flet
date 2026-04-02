import requests

BASE = "http://localhost:8000/productos"
TIME_OUT = 10

async def list_products(limit:int=20, offset:int=0) -> dict:
    try:
        r = requests.get(f"{BASE}/", params={"limit":limit, "offset":offset}, timeout=TIME_OUT)
        if 200 <= r.status_code < 300:
            return r.json() if r.content else {}
        raise ValueError(f"Error {r.status_code}", r.status_code)
    except Exception as e:
        raise ValueError(f"Error de conexión: {str(e)}")

async def get_product(product_id:str) -> dict:
    try:
        r = requests.get(f"{BASE}/{product_id}", timeout=TIME_OUT)
        if 200 <= r.status_code < 300:
            return r.json() if r.content else {}
        raise ValueError(f"Error {r.status_code}", r.status_code)
    except Exception as e:
        raise ValueError("Error de conexión", str(e))

async def create_product(data:dict) -> dict:
    try:
        r = requests.post(f"{BASE}/", json=data, timeout=TIME_OUT)
        if 200 <= r.status_code < 300:
            return r.json() if r.content else {}
        raise ValueError(f"Error {r.status_code}", r.status_code)
    except Exception as e:
        raise ValueError("Error de conexión", str(e))

async def update_product(product_id:str, data:dict) -> dict:
    try:
        r = requests.put(f"{BASE}/{product_id}", json=data, timeout=TIME_OUT)
        if r.status_code >= 400:
            try:
                payload = r.json()
                detail = payload.get("detail") or payload.get("error") or r.text
            except:
                detail = r.text
            raise ValueError(detail, r.status_code)
        return r.json()
    except requests.RequestException as e:
        raise ValueError(f"Error de red: {str(e)}", 0)

async def delete_product(product_id: str):
    # Asegúrate de que BASE sea exactamente "http://localhost:8000/productos"
    # Sin barras diagonales al final de la variable BASE
    url = f"{BASE}/{product_id}"
    
    try:
        # Usamos requests.delete
        r = requests.delete(url, timeout=10)
        
        # Si el servidor responde 405, imprimimos la URL para ver qué está mal
        if r.status_code == 405:
            print(f"ERROR 405: El backend no acepta DELETE en la URL: {url}")
            raise ValueError("Método no permitido (405). Revisa la ruta en el Backend.")
            
        if r.status_code >= 400:
            raise ValueError(f"Error {r.status_code}: {r.text}")
            
        return r.json() if r.content else {}
    except Exception as e:
        print(f"Excepción en delete_product: {e}")
        raise e