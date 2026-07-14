@echo off
cd /d D:\AI探索学习\worldcup
echo Starting World Cup Dashboard on http://localhost:8888
echo Sync takes ~5s, then browser ready.
echo Keep this window open.
.venv\Scripts\python sync_worldcup.py --serve
