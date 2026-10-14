# Kit de candidatura

Um projeto para o Claude Code que monta o seu CV num formato que os robôs de triagem (ATS)
leem sem embaralhar e ajusta esse CV para cada vaga, medindo quais palavras-chave da vaga
o CV prova. Também escreve a carta e as respostas do formulário.

O kit não inventa nada: o que não estiver no seu CV ou no seu LinkedIn vira pergunta para você.

## O que instalar (uma vez)

1. **Claude Code**: https://claude.com/claude-code
2. **Google Chrome** ou **Microsoft Edge**: é o navegador que imprime o PDF.
3. **uv**, que roda a medição do PDF:
   - Mac e Linux, no terminal: `curl -LsSf https://astral.sh/uv/install.sh | sh`
   - Windows, no PowerShell: `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`
4. **Python 3** (no Mac já vem; no Windows, pela Microsoft Store ou python.org).

## Como usar

1. Baixe ou clone esta pasta e abra no Claude Code.
2. Primeira vez: digite `/cv-base`. Tenha à mão o seu CV atual em PDF e o PDF do seu LinkedIn.
3. Para cada vaga: cole o link ou o texto da vaga, ou digite `/candidatura`.

Cada vaga vira uma pasta em `CANDIDATURAS/` com o CV ajustado em PDF, a carta e as
respostas. O envio é sempre seu.
