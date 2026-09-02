@echo off
chcp 437 >nul
color 0A
mode con: cols=80 lines=25
title CONTROLEUR DOCKER LABO v2

:menu
cls
echo ================================================================
echo                    CONTROLEUR DE LABO DOCKER
echo ================================================================
echo.
echo   [ CONFIGURATION DU TEST DISTRIBUE ]
echo.
echo   Nombre de machines Docker (Noeuds) a simuler :
set /p "fenetre=   >>> "

echo.
echo   =========================================
echo   CHOIX DU TYPE DE CIBLE :
echo   [1] Cible de type URL (Ex: google.com)
echo   [2] Cible de type IP (Ex: 8.8.8.8)
echo   =========================================
echo.
set /p "type_cible=   Votre choix (1 ou 2) >>> "

echo.
echo   Entrez l'adresse de la cible :
set /p "cible=   >>> "

if "%cible%"=="" goto menu
if "%fenetre%"=="" set "fenetre=1"
if "%type_cible%"=="" set "type_cible=1"

cls
echo ================================================================
echo                    PREPARATION DE DOCKER
echo ================================================================
echo.
echo   TARGET  : %cible%
echo   TYPE    : Option %type_cible% selectionnee
echo   NOEUDS  : %fenetre% conteneurs en parallele
echo.
echo   Arret des anciens tests en cours...
docker compose down >nul 2>&1

echo   Mise a jour et construction de l'image Docker...
docker compose build

cls
echo ================================================================
echo                    LANCEMENT DE LA SIMULATION
echo ================================================================
echo.
echo   Demarrage de %fenetre% machines virtuelles...
:: Commande mise à jour pour passer la cible et le type au script python
docker compose up --scale noeud_test=%fenetre% -d

echo.
echo   [OK] Simulation Docker lancee avec succes !
echo   Affichage des compteurs (Faites Ctrl+C pour quitter)...
echo ================================================================
timeout /t 2 >nul

docker compose logs -f

echo.
echo   Nettoyage et arret du laboratoire Docker...
docker compose down
echo.
echo   Appuyez sur une touche pour revenir au menu...
pause >nul
goto menu
