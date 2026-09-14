@echo off
title Statsfirm Co. - Servidor Web Corporativo
echo ========================================================
echo   STATSFIRM CO. - SERVIDOR WEB COMERCIAL Y CORPORATIVO
echo   Abriendo navegador en: http://localhost:3000
echo ========================================================
start "" http://localhost:3000
cd "%~dp0Statsfirm\app"
node server.js
pause
