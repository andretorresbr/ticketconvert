```
  ████████╗██╗ ██████╗██╗  ██╗███████╗████████╗
     ██╔══╝██║██╔════╝██║ ██╔╝██╔════╝╚══██╔══╝
     ██║   ██║██║     █████╔╝ █████╗     ██║
     ██║   ██║██║     ██╔═██╗ ██╔══╝     ██║
     ██║   ██║╚██████╗██║  ██╗███████╗   ██║
     ╚═╝   ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝   ╚═╝
          C O N V E R T  v1.1.0
  KRB_CRED base64  →  .kirbi  +  .ccache
```

---

## Uso

```
ticket_convert.exe <base64> <saida>
```

| Argumento | Descrição |
|-----------|-----------|
| `base64`  | Ticket em base64 (output do Rubeus `asktgt` / `dump`) |
| `saida`   | Nome base dos arquivos gerados (sem extensão) |

**Exemplo:**

```
ticket_convert.exe "doIFm..." felipe.brasil
```

Gera:
- `felipe.brasil.kirbi` — formato Mimikatz/Rubeus
- `felipe.brasil.ccache` — formato impacket/Linux

---

## Instalação e geração do executável (ambiente Windows)

- Baixar o repositório e criar um ambiente virtual (venv)

```
cd ticketconvert
pip install virtualenv
virtualenv.exe myenv
.\myenv\Scripts\activate
pip install -r requirements.txt
```

- Compilar o executável usando o script `build.bat`

```
.\build.bat
deactivate
```

O executável gerado estará em `dist\ticket_convert.exe`.


## Uso do script em Python (Windows ou Linux)

- Baixar o repositório e criar um ambiente virtual (venv)

```
cd ticketconvert
pip install virtualenv
virtualenv.exe myenv
.\myenv\Scripts\activate
pip install -r requirements.txt
```

- Executar o script

```
python.exe .\ticket_convert.py
```
ou
```
python ticket_convert.py
```
