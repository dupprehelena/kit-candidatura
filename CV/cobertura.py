#!/usr/bin/env python3
"""Mede, no PDF ATS já gerado, onde cada palavra-chave da vaga caiu.

Gerar o PDF não prova que a vaga foi coberta. Extrair o texto e achar a palavra
na seção certa, sim: em WORK EXPERIENCE ela vem com empresa, data e resultado —
é prova. Só no resumo ou em SKILLS o ATS pontua e o entrevistador cobra.

Uso:  uv run --with pdfminer.six python cobertura.py <pdf> "design system" figma
      uv run --with pdfminer.six python cobertura.py <pdf> < palavras.txt
      uv run --with pdfminer.six python cobertura.py --test
"""
import re
import sys
import unicodedata
from pathlib import Path

# Seções onde a palavra-chave vem datada e creditada a uma empresa: é o que prova.
PROVA = {"WORK EXPERIENCE", "EXPERIÊNCIA PROFISSIONAL", "TEACHING EXPERIENCE",
         "EXPERIÊNCIA DOCENTE", "EARLIER EXPERIENCE", "EXPERIÊNCIA ANTERIOR"}

# Heading do ats.py: maiúscula, espaço, & e hífen. Nada de ponto, vírgula ou barra.
HEADING = re.compile(r"[A-ZÀ-Ú][A-ZÀ-Ú &-]{2,38}")


def normal(s: str) -> str:
    """Minúscula, sem acento, espaço colapsado — aplicado aos dois lados do match."""
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"\s+", " ", s).strip()


def secoes(texto: str) -> dict[str, str]:
    """Texto do PDF -> {heading: corpo}.

    Heading é linha curta, toda em maiúsculas — o que ats.py gera em <h2>.
    Detectar pelo formato, e não por lista fixa, sobrevive a heading novo.

    Só letras maiúsculas, espaço, & e hífen: pontuação elimina o fim de linha
    quebrado ("UI.", "NPS, CSAT", "A/B"). E sigla solta na linha ("WCAG", "MVP",
    "PWA") é barrada exigindo espaço ou 6+ caracteres — todo heading que o
    ats.py gera tem uma coisa ou outra. Sem isso, um fragmento vira seção
    fantasma e rouba as ocorrências da seção real, sem avisar ninguém.
    """
    atual, out = "CABEÇALHO", {"CABEÇALHO": ""}
    for linha in texto.splitlines():
        l = linha.strip()
        if not l:
            continue
        if HEADING.fullmatch(l) and (" " in l or len(l) >= 6):
            atual = l
            out.setdefault(atual, "")
        else:
            out[atual] += " " + l
    return out


def conta(kw: str, corpo: str) -> int:
    """Ocorrências de kw, tolerando o plural em qualquer dos dois lados."""
    base = re.escape(normal(kw).removesuffix("s"))
    return len(re.findall(rf"\b{base}s?\b", normal(corpo)))


def relatorio(pdf: Path, palavras: list[str]) -> str:
    from pdfminer.high_level import extract_text

    secs = secoes(extract_text(str(pdf)))
    out = [f"Cobertura medida em `{pdf.name}`", "",
           "| Palavra-chave | Ocorrências | Onde | Veredicto |", "|---|---|---|---|"]
    for kw in palavras:
        onde = {s: n for s in secs if (n := conta(kw, secs[s]))}
        if not onde:
            v = "❌ ausente"
        elif set(onde) & PROVA:
            v = "✅ provada"
        else:
            v = "⚠️ sem prova"
        lugares = ", ".join(f"{s} ({n}x)" for s, n in onde.items()) or "—"
        out.append(f"| {kw} | {sum(onde.values())} | {lugares} | {v} |")
    return "\n".join(out)


def demo() -> None:
    assert normal("Experiência  DOCENTE") == "experiencia docente"
    t = "[MOCK] Aluna Teste\nWORK EXPERIENCE\nLed a design system\nSKILLS\nFigma, Jira"
    s = secoes(t)
    assert set(s) == {"CABEÇALHO", "WORK EXPERIENCE", "SKILLS"}, s
    assert "design system" in s["WORK EXPERIENCE"]
    assert conta("design systems", s["WORK EXPERIENCE"]) == 1  # plural na vaga, singular no CV
    assert conta("Figma", s["SKILLS"]) == 1
    assert conta("design system", s["SKILLS"]) == 0
    assert conta("acessibilidade", "Acessibilidade WCAG e ACESSIBILIDADE digital") == 2
    assert conta("kubernetes", t) == 0
    # fim de linha quebrado e sigla solta não podem virar seção (bug de 22/09/2026:
    # "UI." virou seção e levou junto as ocorrências de design system do WORK EXPERIENCE)
    q = ("WORK EXPERIENCE\nran a design system with a generative, adaptive\nUI.\n"
         "audits aligned with\nWCAG\nand a navigable\nMVP\nSKILLS\nFigma")
    s2 = secoes(q)
    assert set(s2) == {"CABEÇALHO", "WORK EXPERIENCE", "SKILLS"}, s2
    assert conta("design system", s2["WORK EXPERIENCE"]) == 1
    assert conta("WCAG", s2["WORK EXPERIENCE"]) == 1
    assert secoes("VOLUNTEER WORK\n[MOCK] ONG")["VOLUNTEER WORK"].strip() == "[MOCK] ONG"
    assert "LANGUAGES" in secoes("LANGUAGES\nEnglish")
    print("ok")


if __name__ == "__main__":
    if "--test" in sys.argv:
        demo()
    else:
        pdf, *palavras = sys.argv[1:]
        if not palavras:
            palavras = [l.strip() for l in sys.stdin if l.strip()]
        print(relatorio(Path(pdf), palavras))
