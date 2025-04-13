import requests
import os

def send_to_webhook(payload):
    webhook_url = os.getenv("WEBHOOK_URL")
    if not webhook_url:
        print("Webhook URL não encontrada no .env")
        return False
    try:
        response = requests.post(webhook_url, json=payload, timeout=10)
        return response.status_code == 200
    except Exception as e:
        print(f"Erro no envio do webhook: {e}")
        return False
