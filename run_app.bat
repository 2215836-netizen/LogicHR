@echo off
cd /d "%~dp0"
echo LogicHR 실행 중... (브라우저가 자동으로 열립니다)
python -m streamlit run app.py
pause
