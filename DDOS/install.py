import sys
import os
import subprocess

def run_command(command, use_shell=True):
    """Exécute une commande système et gère les erreurs."""
    try:
        subprocess.check_call(command, shell=use_shell)
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n[!] Erreur lors de l'exécution de : {' '.join(command) if isinstance(command, list) else command}")
        return False

def check_wsl():
    """Détermine si le script tourne dans WSL ou Windows pur."""
    if sys.platform.startswith('linux'):
        # On vérifie si le mot 'microsoft' est dans la version du noyau
        if 'microsoft' in os.uname().release.lower():
            return "wsl"
        return "linux"
    return "windows"

def install_for_wsl():
    print("\n[+] Mode WSL détecté.")
    print("[+] Mise à jour des paquets et installation de hping3, scapy et requests...")
    
    # On vérifie si l'utilisateur est root/sudo
    if os.geteuid() != 0:
        print("[!] ATTENTION : Vous devez lancer ce script avec 'sudo python3 install.py' sous WSL.")
        sys.exit(1)
        
    # AJOUT : Installation de python3-requests en plus de hping3, scapy et pip
    cmd = "apt-get update && apt-get install -y hping3 python3-scapy python3-pip python3-requests"
    if run_command(cmd):
        print("\n[OK] Tout est installé avec succès pour WSL !")
    else:
        print("\n[X] L'installation a échoué. Vérifiez votre connexion internet.")

def install_for_windows():
    print("\n[+] Mode Windows détecté.")
    print("[+] Installation de Scapy et Requests pour Windows...")
    
    # Étape 1 : Installer scapy et requests via pip
    cmd_pip = f'"{sys.executable}" -m pip install scapy requests'
    run_command(cmd_pip)
    
    print("\n================================================================")
    print("[!] RAPPEL IMPORTANT POUR WINDOWS :")
    print("Pour que Scapy fonctionne sur Windows sans WSL, vous DEVEZ installer")
    print("le pilote Npcap manuellement si ce n'est pas déjà fait.")
    print("Téléchargement gratuit ici : https://npcap.com")
    print("================================================================")

if __name__ == "__main__":
    system_type = check_wsl()
    
    if system_type == "wsl":
        install_for_wsl()
    elif system_type == "windows":
        install_for_windows()
    else:
        print("[+] Mode Linux pur détecté (Hors WSL).")
        install_for_wsl()
