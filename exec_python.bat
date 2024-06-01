:: Matar outros processos Python em execução
taskkill /f /im python.exe

:: Ativar o ambiente do Conda
call conda activate chattelegram

:: Executar o script Python
cd app
python main.py