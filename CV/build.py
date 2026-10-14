#!/usr/bin/env python3
"""Imprime o CV em PDF pelo Chrome (ou Edge) em modo headless.

Uso:  python3 CV/build.py <cv.html> [<saida.pdf>]
      sem <saida.pdf>, o PDF sai ao lado do HTML, com o mesmo nome.

Navegador fora do lugar padrão? Aponte a variável CHROME para o executável.
Só stdlib: roda em Mac, Windows e Linux sem instalar nada além do navegador.
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

CANDIDATOS = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]
NO_PATH = ["google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "microsoft-edge"]


def navegador() -> str:
    if os.environ.get("CHROME"):
        return os.environ["CHROME"]
    for c in CANDIDATOS:
        if Path(c).exists():
            return c
    for c in NO_PATH:
        if shutil.which(c):
            return shutil.which(c)
    sys.exit("ERRO: não achei Chrome nem Edge. Instale um deles ou defina CHROME=<caminho do executável>.")


def main() -> None:
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    html = Path(sys.argv[1]).resolve()
    pdf = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else html.with_suffix(".pdf")
    if not html.exists():
        sys.exit(f"ERRO: {html} não existe.")
    pdf.unlink(missing_ok=True)
    subprocess.run([navegador(), "--headless", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={pdf}", "--virtual-time-budget=4000", html.as_uri()],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
    # A prova é o arquivo existir, não o código de saída do navegador.
    if not pdf.exists() or pdf.stat().st_size == 0:
        sys.exit(f"ERRO: o navegador não gerou {pdf.name}.")
    print(f"ok  {pdf}")


if __name__ == "__main__":
    main()
