# -*- coding: utf-8 -*-
"""Âncora diária das cadeias de registros do SIGAB/QUANTOCA.

Roda nos servidores do GitHub (fora do Supabase). Pergunta à função `acesso` as CABEÇAS
das duas cadeias de hashes — movimentos do QUANTOCA e rastro de acessos — e grava um
arquivo por dia em ancoras/AAAA/AAAA-MM-DD.json. Em seguida o arquivo é carimbado no
OpenTimestamps (registro público no Bitcoin, que ninguém altera).

Como isso prova a integridade: cada registro de movimento leva o hash do anterior. A
cabeça (último hash) resume TODOS os registros até ela. Se alguém mudar um registro
antigo, a cabeça refeita não bate mais com a que ficou carimbada aqui naquela data.
"""
import json, hashlib, os, sys, urllib.request
from datetime import datetime, timezone, timedelta

URL = "https://nfyksudihcbzmlolzmet.supabase.co/functions/v1/acesso"
CHAVE_PUBLICA = "sb_publishable_jJ_tiCqoCUQgHczASdMJvw_Jpp8SG9Y"   # chave pública do site (só lê)
BRT = timezone(timedelta(hours=-3))                                   # hora de Belém/Brasília

req = urllib.request.Request(URL, json.dumps({"acao": "cadeias"}).encode(), {
    "Content-Type": "application/json", "apikey": CHAVE_PUBLICA,
    "Authorization": "Bearer " + CHAVE_PUBLICA})
with urllib.request.urlopen(req, timeout=60) as r:
    c = json.load(r)

agora = datetime.now(BRT)
corpo = {
    "sistema": "SIGAB/QUANTOCA — AvHoFlu Rio Tocantins (H-12)",
    "data_local": agora.strftime("%Y-%m-%d"),
    "registrado_em_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "conferido_no_banco_em": c["conferido_em"],
    "movimentos": c["movimentos"],
    "rastro": c["rastro"],
}
# resumo do próprio arquivo: o que o carimbo público prende
canon = json.dumps(corpo, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
corpo["sha256_deste_registro"] = hashlib.sha256(canon.encode("utf-8")).hexdigest()

pasta = os.path.join("ancoras", agora.strftime("%Y"))
os.makedirs(pasta, exist_ok=True)
arq = os.path.join(pasta, agora.strftime("%Y-%m-%d") + ".json")
with open(arq, "w", encoding="utf-8") as f:
    json.dump(corpo, f, ensure_ascii=False, indent=1, sort_keys=True)
    f.write("\n")
print(arq)
if not (c["movimentos"] or {}).get("integra") or not (c["rastro"] or {}).get("integra"):
    print("ATENÇÃO: alguma cadeia NÃO está íntegra — ver o arquivo.", file=sys.stderr)
