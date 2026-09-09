# PC Shutdown Timer

Um temporizador simples e visual para programar o desligamento do computador no Windows.

## Para usar

Se você recebeu o executável, não precisa instalar Python nem bibliotecas:

1. Abra `PCShutdownTimer.exe`.
2. Informe horas, minutos e segundos.
3. Clique em **Iniciar desligamento**.
4. Confirme a operação.

O Windows será programado para desligar quando a contagem chegar a zero. Para interromper a operação, clique em **Cancelar**.

O executável pronto fica em `dist\PCShutdownTimer.exe`. A Área de Trabalho pode conter também um atalho com o ícone do aplicativo.

## Recursos

- Contagem regressiva em formato `HH:MM:SS`.
- Horário exato previsto para o desligamento.
- Confirmação antes de programar a ação.
- Cancelamento seguro usando `shutdown /a`.
- Interface responsiva, tema escuro e janela redimensionável.
- Botões para minimizar e fechar.
- Compatível com Windows 10 e Windows 11.

## Executar pelo código-fonte

### Requisitos

- Windows 10 ou Windows 11.
- Python 3.10 ou superior.

No PowerShell, dentro da pasta do projeto:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python main.py
```

Se o PowerShell bloquear a ativação do ambiente virtual, execute uma vez:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

## Gerar o executável

Com o ambiente virtual ativado, instale as ferramentas de empacotamento:

```powershell
python -m pip install pyinstaller pillow
```

Gere o ícone e o executável:

```powershell
python -c "from PIL import Image; Image.open('app_icon.png').save('app_icon.ico')"
pyinstaller --noconfirm --clean --onefile --windowed --name PCShutdownTimer --icon app_icon.ico main.py
```

O resultado estará em `dist\PCShutdownTimer.exe`. O arquivo é independente: quem baixá-lo não precisa ter Python instalado.

## Como funciona

O aplicativo usa os comandos nativos do Windows:

```text
shutdown /s /t SEGUNDOS   -> agenda o desligamento
shutdown /a               -> cancela o desligamento
```


