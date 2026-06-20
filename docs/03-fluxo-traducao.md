# 03 — Fluxo de tradução

```
extract → units → (assist) → revisar → qa → build → package
```

## 1. Unidades de tradução

Depois de `p5r-ptbr units`, cada arquivo `dump/.../X.msg` tem um
`translation/.../X.msg.json` com unidades assim:

```json
{
  "key": "field/example.msg::msg:dlg_001#0",
  "speaker": "Ryuji",
  "source": "Texto original em ingles[e]",
  "target": "",
  "status": "untranslated",
  "context": "Linhas vizinhas da cena...",
  "notes": ""
}
```

Edite **`target`** e mude **`status`**. O campo `context` mostra a cena ao redor para
ajudar na localização. **Preserve as tags** entre colchetes.

## 2. (Opcional) Rascunho de IA

```bash
p5r-ptbr assist --translation translation/ --limit 50
```

Gera rascunhos de qualidade com o Claude (contexto rico: glossário + guia de estilo + voz
do personagem + cena). Tudo sai como `status: "draft"` — **rascunho, não final**. Requer
`pip install -e ".[assist]"` e `ANTHROPIC_API_KEY`. É opcional: o fluxo 100% humano funciona
sem ele.

## 3. Revisão humana (obrigatória)

Toda linha passa por uma pessoa. Veja `06-guia-de-revisao.md`. Ao aprovar, mude o status
para `reviewed` (e, depois de testar no jogo, `final`).

## 4. QA

```bash
p5r-ptbr qa --translation translation/ --max-len 42
```

Verifica tags preservadas, alvos vazios em unidades aprovadas, linhas longas e aderência
ao glossário. Resolva os problemas antes do build.

## 5. Build + empacotamento

```bash
p5r-ptbr build --dump dump/ --translation translation/ --mod mod/
p5r-ptbr package --mod mod/
```

`build` reconstrói os `.msg` traduzidos dentro de `mod/` (só usa `reviewed`/`final` com
tags íntegras; mensagens não aprovadas ficam no original). `package` gera o `.zip` em
`dist/` para o Reloaded-II.

## Progresso

```bash
p5r-ptbr stats --translation translation/
```
