from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import hashlib
import os

app = Flask(__name__)
CORS(app)

def sha1_hash(senha):
    return hashlib.sha1(senha.encode()).hexdigest().upper()

@app.route("/api/verificar", methods=["POST"])
def verificar():
    data = request.json
    senha = data.get("senha")

    if not senha:
        return jsonify({"erro": "Senha não informada"}), 400

    sha1 = sha1_hash(senha)
    prefix = sha1[:5]
    suffix = sha1[5:]

    r = requests.get(
        f"https://api.pwnedpasswords.com/range/{prefix}",
        timeout=10
    )

    if r.status_code != 200:
        return jsonify({"status": "erro"})

    for linha in r.text.splitlines():
        h, count = linha.split(":")
        if h == suffix:
            return jsonify({
                "status": "vazada",
                "ocorrencias": int(count),
                "fonte": "bases públicas conhecidas"
            })

    return jsonify({
        "status": "nao_encontrada"
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
