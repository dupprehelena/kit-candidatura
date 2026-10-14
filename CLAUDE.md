# Kit de candidatura

Projeto de candidatura a vagas: um CV base que o robô de ATS lê sem embaralhar, ajustado e
medido para cada vaga, com carta e respostas de formulário.

## Regra que manda em tudo aqui

**Nunca inventar dado sobre a carreira de quem usa este kit.** Cargo, número, data,
ferramenta, empresa, telefone, cidade: ou está no CV base, ou a pessoa confirmou nesta
conversa, ou vira pergunta. Um número inventado num CV é o tipo de erro que explode na
frente do recrutador. Vale igual para palavra-chave de vaga: termo que a pessoa não
consegue defender numa entrevista não entra.

## Por onde começar

- Primeira vez, ou `DOCS/perfil.md` não existe → `/cv-base`.
- Colaram uma vaga ou um link de vaga → `/candidatura`.

## Coerência entre plataformas

O recrutador cruza CV com LinkedIn com Gupy. `DOCS/perfil.md` é a fonte de verdade de cargo,
empresa e data: mudou algo, muda **lá primeiro** e propaga para os CVs.

## Como o CV funciona

- `CV/cv-pt.html` e `CV/cv-en.html` são o CV base. É aqui que se edita, e é o próprio HTML
  que vira PDF: coluna única, headings padrão, sem tabela, coluna ou imagem.
- `python3 CV/build.py <cv.html> [<saida.pdf>]` imprime o PDF pelo Chrome ou Edge.
- Cada vaga ganha uma cópia própria em `CANDIDATURAS/AAAA-MM-DD-empresa/cv.html`. O CV base
  não se ajusta para vaga nenhuma.

## Verificação obrigatória depois de mexer no CV

Gerar PDF não é prova. Extrair o texto e conferir a ordem de leitura é:

```
uv run --with pdfminer.six python -c "from pdfminer.high_level import extract_text; print(extract_text('CV/cv-pt.pdf'))"
```

Ajustou para uma vaga? A segunda prova é onde cada palavra-chave caiu:

```
uv run --with pdfminer.six python CV/cobertura.py <pdf> "design system" figma
```

Palavra que só aparece em COMPETÊNCIAS ou no resumo sai como `⚠️ sem prova`: o ATS pontua,
o entrevistador cobra.

## Onde está o quê

- `DOCS/perfil.md`: fonte de verdade (criado pela `/cv-base`).
- `CV/`: modelo, CV base, `build.py` e `cobertura.py`.
- `CANDIDATURAS/`: uma pasta por vaga e o `TRACKER.md`.
