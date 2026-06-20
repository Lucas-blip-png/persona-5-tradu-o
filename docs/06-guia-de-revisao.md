# 06 — Guia de revisão

A qualidade da tradução vem da revisão. Todo `draft` (humano ou de IA) precisa passar por
uma pessoa antes de virar `reviewed`.

## Estados

| status         | significado                                              | entra no build? |
|----------------|----------------------------------------------------------|-----------------|
| `untranslated` | sem tradução                                             | não             |
| `draft`        | rascunho (humano ou IA)                                  | não             |
| `reviewed`     | revisado contra o guia de estilo e o glossário          | sim             |
| `final`        | revisado **e** validado no jogo                          | sim             |

## Checklist de revisão (por unidade)

1. **Sentido:** a tradução transmite a mesma ideia e intenção do original?
2. **Naturalidade:** soa como um brasileiro falaria? (leia em voz alta)
3. **Voz do personagem:** o registro bate com `vozes-personagens.md`?
4. **Gírias/trocadilhos:** foram adaptados (não traduzidos ao pé da letra)?
5. **Glossário:** os termos seguem `glossario.pt-br.csv`? (`p5r-ptbr qa` avisa divergências)
6. **Tags:** todas as tags `[...]` foram preservadas? (o QA reprova se não)
7. **Tamanho:** cabe na caixa/menu? (`p5r-ptbr qa --max-len N`)
8. **Honoríficos:** seguiram a política do guia de estilo?

Use o campo `notes` para registrar decisões difíceis (adaptação de trocadilho, escolha de
gíria, motivo de fugir do literal). Isso ajuda a manter consistência entre revisores.

## Boas práticas

- Revise por **cena**, não por linha solta — o `context` ajuda, mas ver a sequência inteira
  evita inconsistências.
- Ao aprovar uma boa tradução, ela alimenta a **memória de tradução** e passa a ser
  reaproveitada automaticamente em trechos idênticos.
- Rascunhos de IA são ponto de partida, não verdade: confira fidelidade, voz e tags.
