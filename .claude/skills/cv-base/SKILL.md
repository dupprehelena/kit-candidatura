---
name: cv-base
description: Monta o CV base no formato que o ATS lê, a partir do CV atual e do LinkedIn da pessoa, e cria o DOCS/perfil.md como fonte de verdade de cargos e datas. Use na primeira vez que o kit é aberto, ou quando disserem "monta meu CV", "começar", "atualiza meu CV base". NÃO use para ajustar o CV para uma vaga (isso é a /candidatura).
---

# CV base

Roda uma vez, no começo, e de novo quando a carreira muda (cargo novo, empresa nova). Sai daqui:

- `DOCS/perfil.md`: a fonte de verdade de nome, contato, cargos, empresas e datas
- `CV/cv-pt.html` (e `CV/cv-en.html`, se a pessoa quiser): o CV base, no formato de `CV/modelo-cv.html`
- `CV/cv-pt.pdf`: o PDF gerado e conferido

## A regra que não se negocia

Este passo **reorganiza**, não inventa. Cargo, número, data, ferramenta, empresa: ou está no
material que a pessoa entregou, ou ela confirmou nesta conversa, ou vira pergunta. Conquista
sem número fica sem número: sugerir que ela procure o dado é bom, chutar o dado não é.

## Passos

1. **Pedir o material.** O CV atual em PDF (DOCX → pedir para exportar em PDF) e o LinkedIn
   (no perfil, *Mais → Salvar como PDF*, ou o texto colado). Não acessar o LinkedIn por
   script: o PDF ou o texto colado bastam.
2. **Escrever `DOCS/perfil.md`.** Nome como aparece no LinkedIn, cidade, telefone com DDI,
   e-mail, links (portfólio, LinkedIn), e uma tabela de cargos: cargo, empresa, mês/ano de
   início e de saída. Formação e idiomas. Data ou cargo diferente entre o CV e o LinkedIn →
   perguntar qual vale e anotar: o recrutador cruza as duas fontes, e a incoerência aparece
   para ele.
3. **Montar `CV/cv-pt.html`** a partir de `CV/modelo-cv.html`: copiar o modelo e trocar o
   conteúdo, mantendo a estrutura (coluna única, `h2` com os headings do modelo, `h3` para o
   cargo, `.meta` para empresa, `.dates` para o período). Nada de tabela, coluna, ícone ou
   imagem: é isso que embaralha a leitura do robô.
   - Bullet: verbo de ação, o que fez e o resultado, com o resultado só se a pessoa tiver o dado.
   - Habilidade só entra em COMPETÊNCIAS se aparece também em algum bullet; se não aparece,
     perguntar onde ela usou.
   - Experiência com mais de 10 anos ou fora da área pode ir para `EXPERIÊNCIA ANTERIOR`, em
     uma linha por cargo.
4. **Gerar e conferir.**

   ```
   python3 CV/build.py CV/cv-pt.html
   uv run --with pdfminer.six python -c "from pdfminer.high_level import extract_text; print(extract_text('CV/cv-pt.pdf'))"
   ```

   Se o texto sair na ordem em que um humano lê, passou. Se sair embaralhado, quebrou.
5. **Inglês, se ela quiser.** `CV/cv-en.html` é a tradução fiel do PT, com os headings em
   inglês listados no comentário de `CV/modelo-cv.html`. Mesma conferência.
6. **Fechar com a lista de lacunas.** Bullet sem resultado, cargo sem data de saída,
   habilidade sem prova: listar como perguntas para a pessoa responder quando puder.
