---
name: candidatura
description: Monta a candidatura a uma vaga — CV ajustado e medido contra o ATS, carta, mensagem ao recrutador e respostas do formulário. Use quando colarem uma vaga ou link de job posting, ou disserem "roda a candidatura", "ajusta o CV pra essa vaga", "vale a pena me candidatar?". NÃO use para preparo de entrevista nem para montar o CV base (isso é a /cv-base).
---

# Candidatura a uma vaga

## A regra que não se negocia

Nada que sai da candidatura (CV, carta, mensagem, formulário) inventa dado da carreira de
quem está se candidatando. Cargo, número, data, ferramenta, empresa: ou está no CV base,
ou a pessoa confirmou nesta conversa, ou vira pergunta. Palavra-chave que ela não consegue
defender numa entrevista vira passivo. Lacuna se reporta e fica em aberto. Pretensão
salarial, disponibilidade e data de início sem resposta conhecida viram pergunta, nunca
estimativa.

## Antes de começar

`CV/cv-pt.html` (ou `CV/cv-en.html`) e `DOCS/perfil.md` precisam existir. Se não existirem,
parar e rodar a `/cv-base` primeiro.

## Onde a candidatura mora

Uma pasta por vaga, `CANDIDATURAS/AAAA-MM-DD-empresa/`:

| Arquivo | O que é |
|---|---|
| `vaga.md` | a descrição colada na íntegra, eliminatórios, palavras-chave nos três baldes, os ajustes feitos e as tabelas de cobertura (antes e depois) |
| `cv.html` | a cópia do CV só desta vaga: é aqui que se ajusta, nunca no CV base |
| `Nome_Sobrenome_CV.pdf` | o PDF que vai ser enviado, com o nome da pessoa (o de `DOCS/perfil.md`) |
| `carta.md` | carta, mensagem ao recrutador e respostas do formulário: tudo que é copiar e colar |

A descrição vai para o arquivo **antes** da análise: vaga despublicada some do ar, e sem o
texto original não dá para reauditar a decisão depois.

## Passos

1. **Ler a vaga.** Link → buscar o conteúdo. Texto incompleto (página com login, vaga
   carregada por script) → pedir que colem o texto, não deduzir.
2. **Eliminatório primeiro.** Anos de experiência, formação exigida, localização, visto,
   presencial: se a pessoa não cumpre, dizer na cara **antes** de ajustar qualquer coisa.
   Ajustar CV para vaga já perdida é trabalho jogado fora. A decisão de seguir é dela.
3. **Extrair as palavras-chave** em três baldes:
   - *obrigatórias* — aparecem em requisitos, ou repetidas 2+ vezes
   - *desejáveis* — "nice to have", "diferencial"
   - *cultura/senioridade* — nível, escopo do time, tipo de empresa
4. **Decidir o idioma.** Vaga em inglês ou empresa global → EN. Vaga em português → PT.
   Não existe `CV/cv-en.html` e a vaga é em inglês → perguntar se traduz o CV base agora
   (tradução fiel, sem acrescentar nada).
5. **Medir o ponto de partida.** Gerar o PDF do CV base e medir as obrigatórias:

   ```
   python3 CV/build.py CV/cv-pt.html
   uv run --with pdfminer.six python CV/cobertura.py CV/cv-pt.pdf "palavra 1" "palavra 2"
   ```

   Colar a tabela em `vaga.md` e, para cada obrigatória, dizer qual bullet a prova:
   - ✅ **provada** — existe bullet com o termo ou sinônimo direto
   - 🔁 **implícita** — a experiência existe e o CV usa outra palavra → trocar o termo é
     legítimo, e é aqui que está o ganho real. Só vale quando o bullet já descreve a prática
     com outras palavras; se é só parecida ou vizinha, é ❌ e vira pergunta
   - ❌ **ausente** — não está no CV → reportar como lacuna, e perguntar se a pessoa tem
6. **Ajustar numa cópia só da vaga.** Copiar o CV base para `CANDIDATURAS/AAAA-MM-DD-empresa/cv.html`
   e mexer só nela, apenas nos pontos 🔁 e nos ❌ que a pessoa confirmou que tem. Listar os
   ajustes em `vaga.md`. O CV base não se toca neste passo.
7. **Gerar o PDF e medir de novo.**

   ```
   python3 CV/build.py CANDIDATURAS/AAAA-MM-DD-empresa/cv.html CANDIDATURAS/AAAA-MM-DD-empresa/Nome_Sobrenome_CV.pdf
   uv run --with pdfminer.six python -c "from pdfminer.high_level import extract_text; print(extract_text('CANDIDATURAS/AAAA-MM-DD-empresa/Nome_Sobrenome_CV.pdf'))"
   uv run --with pdfminer.six python CV/cobertura.py CANDIDATURAS/AAAA-MM-DD-empresa/Nome_Sobrenome_CV.pdf "palavra 1" "palavra 2"
   ```

   Primeiro a ordem de leitura: se o texto sair na ordem em que um humano lê, passou.
   Depois a cobertura. É este o portão: nenhuma obrigatória termina `❌ ausente` ou
   `⚠️ sem prova` sem que a pessoa saiba e decida. Colar a tabela em `vaga.md`.
8. **Carta e mensagem ao recrutador.** Cada afirmação sobre a carreira aponta para um bullet
   do CV ajustado: carta é onde a invenção passa despercebida, porque ninguém confere prosa.
   Afirmação sobre a empresa (número, prêmio, lançamento) só com fonte no site da própria
   empresa ou na vaga; sem fonte, sai do texto. Motivação e intenção ("quero trabalhar com
   X", "me interessa Y") são da pessoa: perguntar ou marcar `[CONFIRMAR]`, nunca deduzir do
   CV ou da vaga. Anos de experiência: os mesmos do resumo do CV. Escrita direta, sem clichê de IA ("apaixonada
   por", "no cenário atual", "não apenas X, mas Y", lista de três adjetivos). Carta com até
   4 parágrafos curtos; mensagem de LinkedIn com até 5 linhas.
9. **Respostas do formulário.** Os campos que Gupy e LinkedIn costumam pedir: "por que essa
   vaga", pretensão, disponibilidade, perguntas de triagem. Escrever em `carta.md` para
   reuso; o que depende de decisão da pessoa (salário, data de início) fica em branco, com a
   pergunta ao lado.
10. **Registrar.** Abrir a linha em `CANDIDATURAS/TRACKER.md`.

## O que reportar mesmo sem ser perguntado

- Requisito eliminatório não cumprido (passo 2), sempre antes de qualquer ajuste.
- Palavra-chave obrigatória que ficou `⚠️ sem prova`: o robô pontua, o entrevistador cobra.
- Fato novo que a pessoa confirmou durante a vaga e que vale para a carreira toda (um cargo,
  uma responsabilidade, um projeto). Pela cópia da vaga ele não chega ao CV base: dizer qual
  é e perguntar se entra também em `CV/cv-pt.html`, `CV/cv-en.html` e `DOCS/perfil.md`.
- Divergência com `DOCS/perfil.md`. Mudou cargo, data ou empresa? Muda **lá primeiro** e
  propaga: o recrutador cruza CV com LinkedIn com Gupy.

## O que esta skill não faz

- Enviar a candidatura. Preencher formulário no navegador só se a pessoa pedir, e mesmo
  assim sem tocar na autodeclaração (gênero, raça/cor, PcD, orientação) e sem clicar no
  botão final de envio, que é sempre dela. Login e captcha também são dela.
- Preparo de entrevista.
