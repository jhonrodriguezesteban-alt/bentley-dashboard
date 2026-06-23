import json, subprocess, os, urllib.request, sys
app_id = os.environ.get("OS_APP_ID","")
api_key = os.environ.get("OS_API_KEY","")
if not api_key: print("No API key"); sys.exit(0)

changed = subprocess.check_output(["git","diff","--name-only","HEAD~1","HEAD"]).decode()
title = "Bentley Produccion"
body = "Hay novedades"

if "prod_disenos.json" in changed:
    try:
        cur  = json.loads(subprocess.check_output(["git","show","HEAD:prod_disenos.json"]))
        prev = json.loads(subprocess.check_output(["git","show","HEAD~1:prod_disenos.json"]))
        prev_ids = {d["id"] for d in prev.get("disenos",[])}
        nuevos = [d for d in cur.get("disenos",[]) if d["id"] not in prev_ids]
        if nuevos:
            d = nuevos[-1]
            title = "Nuevo diseno: " + d.get("nombre","")
            body  = "{} - {} {}".format(d.get("responsable",""),d.get("categoria",""),d.get("genero",""))
        else:
            title = "Diseno actualizado"; body = "Cambios en modulo de diseno"
    except Exception as e: print(e)
elif "prod_ops.json" in changed:
    title = "Nueva Orden de Produccion"; body = "Se registro una nueva OP"
elif "prod_ots.json" in changed:
    title = "OT actualizada"; body = "Cambios en ordenes de trabajo"

payload = json.dumps({"app_id":app_id,"included_segments":["All"],
    "headings":{"en":title},"contents":{"en":body},
    "url":"https://jhonrodriguezesteban-alt.github.io/bentley-dashboard/produccion-bentley.html"}).encode()
req = urllib.request.Request("https://onesignal.com/api/v1/notifications",data=payload,
    headers={"Content-Type":"application/json","Authorization":"Basic "+api_key},method="POST")
try:
    with urllib.request.urlopen(req) as r: print("Sent:",json.loads(r.read()))
except Exception as e: print("Error:",e)
