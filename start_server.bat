@echo off
cd /d D:\AI探索学习\worldcup
echo Starting World Cup Dashboard on http://localhost:8888
echo Keep this window open. Close to stop server.
echo.
.venv\Scripts\python sync_worldcup.py --serve
