# Guia de estilo — localização PT-BR de Persona 5 Royal

Este guia é o coração do projeto. A meta não é "traduzir", é **localizar com qualidade**:
fiel ao sentido e à intenção do original, soando natural para quem joga em português
brasileiro. Nada de tradução literal de máquina.

## Princípios

1. **Fidelidade ao sentido, não à forma.** Traduza a ideia, não as palavras. Se a frase
   literal soa estranha em PT-BR, reescreva mantendo a intenção.
2. **Naturalidade.** O diálogo deve soar como um brasileiro falaria de verdade na situação.
   Leia em voz alta: se você não diria assim, reescreva.
3. **Gírias e registro.** Adapte gírias para equivalentes brasileiros que combinem com o
   personagem e a época. Evite regionalismos muito específicos que quebrem a compreensão.
4. **Trocadilhos e referências culturais.** Recrie o efeito (humor, duplo sentido) em vez
   de traduzir ao pé da letra. Quando precisar adaptar bastante, deixe uma nota no campo
   `notes` da unidade explicando a escolha.
5. **Voz do personagem.** Cada personagem fala de um jeito. Veja `vozes-personagens.md` e
   mantenha a consistência entre cenas.
6. **Consistência de termos.** Use sempre os termos definidos em `glossario.pt-br.csv`.

## Tom e tratamento

- Tratamento padrão entre os jovens: **informal** ("você", "a gente", "cê" só quando couber
  ao personagem). Adultos formais e figuras de autoridade podem usar registro mais alto.
- Evite o "tu" conjugado de forma mista; mantenha "você" como padrão para consistência.
- Palavrões: adapte a intensidade do original. Não suavize demais nem exagere.

## Honoríficos japoneses (-san, -kun, -senpai)

- Política padrão do projeto: **remover honoríficos** e expressar a relação pelo tom
  (ex.: tratamento mais respeitoso, uso do primeiro/último nome). "Senpai" pode virar
  "veterano(a)" ou ser resolvido pelo contexto.
- Exceção: quando o honorífico for **piada ou ponto de enredo**, mantenha e, se necessário,
  adapte. Registre a decisão em `notes`.

## Formatação e restrições técnicas

- **Preserve todas as tags de controle** entre colchetes (ex.: `[e]`, `[n]`, `[f 2 1]`).
  Mesma quantidade, mesmo conteúdo. O QA (`p5r-ptbr qa`) reprova traduções que alteram tags.
- `[n]` costuma ser quebra de linha manual: respeite o ritmo das falas, mas cuidado com o
  tamanho das linhas em telas estreitas (caixas de diálogo, menus). Use `--max-len` no QA.
- Acentuação completa do PT-BR (á à â ã é ê í ó ô õ ú ç) depende da fonte do jogo aceitar
  esses glifos — veja `docs/04-fontes-acentos.md`.

## Fluxo de qualidade (estados)

`untranslated` → `draft` → `reviewed` → `final`

- `draft`: rascunho (humano ou IA). **Nunca** entra no build.
- `reviewed`: revisado por uma pessoa contra este guia e o glossário.
- `final`: revisado e validado no jogo.
- O build só usa `reviewed`/`final` com tags íntegras.
