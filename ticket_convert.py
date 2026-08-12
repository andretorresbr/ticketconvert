#!/usr/bin/env python3
"""
ticket_convert - KRB_CRED base64 → .kirbi + .ccache

Uso:
    ticket_convert.exe <base64> <saida>

Exemplo:
    ticket_convert.exe "doIFm..." felipe.brasil
    → gera felipe.brasil.kirbi
    → gera felipe.brasil.ccache
"""

import sys
import base64

__version__ = '1.1.0'

BANNER = r"""
  ████████╗██╗ ██████╗██╗  ██╗███████╗████████╗
     ██╔══╝██║██╔════╝██║ ██╔╝██╔════╝╚══██╔══╝
     ██║   ██║██║     █████╔╝ █████╗     ██║
     ██║   ██║██║     ██╔═██╗ ██╔══╝     ██║
     ██║   ██║╚██████╗██║  ██╗███████╗   ██║
     ╚═╝   ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝   ╚═╝
          C O N V E R T  v{ver}
  KRB_CRED base64  →  .kirbi  +  .ccache

Autor: André Torres (https://github.com/andretorresbr/ticketconvert)

""".format(ver=__version__)

USAGE = """
Uso:   ticket_convert.exe <base64> <saida>

  base64   Ticket em base64 (output do Rubeus asktgt/dump)
  saida    Nome base dos arquivos gerados (sem extensão)

Exemplo:
  ticket_convert.exe "doIFm..." felipe.brasil

  Gera:
    felipe.brasil.kirbi   (formato Mimikatz/Rubeus)
    felipe.brasil.ccache  (formato impacket/Linux)
"""


def decode_b64(b64_str: str) -> bytes:
    """Decodifica base64, tolerando quebras de linha e padding ausente."""
    b64 = b64_str.strip().replace('\n', '').replace('\r', '').replace(' ', '')
    rem = len(b64) % 4
    if rem:
        b64 += '=' * (4 - rem)
    return base64.b64decode(b64)


def save_kirbi(data: bytes, path: str) -> None:
    with open(path, 'wb') as f:
        f.write(data)


def save_ccache(data: bytes, path: str) -> None:
    try:
        from impacket.krb5.ccache import CCache
    except ImportError:
        raise RuntimeError(
            "impacket não encontrado.\n"
            "  Instale com: pip install impacket\n"
            "  Se estiver usando o .exe, recompile com: build.bat"
        )
    ccache = CCache()
    ccache.fromKRBCRED(data)
    ccache.saveFile(path)


def main() -> None:
    print(BANNER)

    if len(sys.argv) != 3:
        print(USAGE)
        sys.exit(1)

    b64_input  = sys.argv[1]
    output_base = sys.argv[2]

    kirbi_path  = f'{output_base}.kirbi'
    ccache_path = f'{output_base}.ccache'

    print(f'  Ticket : {b64_input[:72]}{"…" if len(b64_input) > 72 else ""}')
    print(f'  Saida  : {output_base}.[kirbi|ccache]')
    print()

    # Decodifica
    try:
        data = decode_b64(b64_input)
        print(f'[*] Ticket decodificado : {len(data)} bytes')
    except Exception as e:
        print(f'[-] Erro ao decodificar base64: {e}', file=sys.stderr)
        sys.exit(1)

    all_ok = True

    # .kirbi
    try:
        save_kirbi(data, kirbi_path)
        print(f'[+] .kirbi  → {kirbi_path}')
    except Exception as e:
        print(f'[-] Erro ao salvar .kirbi: {e}', file=sys.stderr)
        all_ok = False

    # .ccache
    try:
        save_ccache(data, ccache_path)
        print(f'[+] .ccache → {ccache_path}')
    except Exception as e:
        print(f'[-] Erro ao salvar .ccache: {e}', file=sys.stderr)
        all_ok = False

    print()
    if all_ok:
        print('[+] Concluído!\n')
        print('  ── impacket (Linux) ──────────────────────────────────────────')
        print(f'  export KRB5CCNAME={ccache_path}')
        print(f'  python3 secretsdump.py  -k -no-pass <alvo>')
        print(f'  python3 psexec.py       -k -no-pass <alvo>')
        print(f'  python3 wmiexec.py      -k -no-pass <alvo>')
        print()
        print('  ── Rubeus (Windows) ──────────────────────────────────────────')
        print(f'  .\\Rubeus.exe ptt /ticket:{kirbi_path}')
        print(f'  .\\Rubeus.exe describe /ticket:{kirbi_path}')
    else:
        print('[!] Finalizado com erros.', file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
