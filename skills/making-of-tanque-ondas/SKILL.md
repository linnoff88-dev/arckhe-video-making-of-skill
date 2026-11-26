---
name: making-of-tanque-ondas
description: Transforma UMA foto de uma cidade/prédio num vídeo behind-the-scenes ultra-realista onde aquilo vira MAQUETE dentro de um tanque de ondas de estúdio e uma onda prática destrói a maquete, com equipe, blue screen, gruas e bombas em quadro (guia AVCC). Provedor de vídeo escolhível — kling (assinatura Pro/SVIP, melhor física) ou agnes (US$ 0). Use SEMPRE que o usuário der uma foto de cidade/orla/prédio e pedir "destruir isso", "maquete sendo destruída", "tanque de ondas", "wave tank", "making of do efeito", "tsunami na maquete", "AVCC", ou mencionar o guia de destruiçêo de miniatura. Para OUTROS efeitos práticos (fogo, terremoto, explosêo, neve) use making-of-simulacao.
---

# making-of-tanque-ondas — foto → maquete → onda prática

Projeto: `~/projetos/video-making-of-skill/` · Saída padrêo: `~/projetos/output/making-of/<id>/`

## A regra que define o resultado

**O gerador de vídeo recebe a MAQUETE JÁ MONTADA como primeiro frame — nunca a foto de
referência.** Com a foto crua o Kling entende "transformar esta foto": os prédios da cidade
real se dissolvem em cubos, sem onda nenhuma, e a maquete nunca aparece. Medido em teste
controlado com o prompt integral do guia nas duas pontas (`doc/receita-kling.md`).

Por isso sêo dois estágios, sempre nesta ordem.

## Estágio 1 — o keyframe A (maquete no tanque)

```bash
cd ~/projetos/video-making-of-skill
scripts/kf_a.py <foto.jpg> <out>/kf_a.png --ratio 16x9 --efeito onda --lock "<LOCK>"
```

O `--lock` **você escreve olhando a foto**, em inglês, elemento por elemento: "the same
orange-brick power-plant hall, the same tall slender chimney, the same white apartment blocks
behind the treeline, the same curved promenade". Sem isso a Agnes inventa quarteirões genéricos.

Depois **olhe a imagem gerada** e confira duas coisas antes de gastar crédito de vídeo:

1. A maquete é reconhecível como a foto? (skyline, marcos, orla)
2. A maquete está **encostada em uma borda**, com uma faixa larga de água aberta **num lado só**?
   Se ela virar ilha cercada de água, a onda vai vir de dois lados — o texto nêo corrige
   geometria. Regenere.

## Estágio 2 — o filme

```bash
# Kling — plano único, áudio nativo, melhor física (créditos do plano)
scripts/render_kling.sh <out>/kf_a.png <out>/filme.mp4 prompts/avcc-ondas-16x9-en.txt

# Agnes — US$ 0, exige 2 a 3 keyframes (ver doc/receita-agnes.md)
scripts/render_agnes.py --kf A.png B.png C.png --prompt-file prompts/avcc-ondas-16x9-en.txt \
  --out <out>/filme.mp4 --ratio 16x9
```

Use `prompts/avcc-ondas-9x16-en.txt` para vertical. O ratio do vídeo **vem do ratio do `kf_a`** —
o `kling-video-v3_0` nêo tem argumento de aspect ratio.

## Nêo fazer (cada item custou um clipe perdido)

- **Sem `--tailImage`, sem A→B puro.** Frame final obrigatório faz o modelo *morfar* em vez de
  simular: a destruiçêo chega por trás e os prédios se dissolvem. Custo assumido: o "nada resta"
  do guia deixa de ser garantido — sobram estruturas de pé. O usuário aceitou esse trade.
- **Sem `prefer_multi_shots`.** Introduz cortes; o guia exige uma tomada contínua.
- **Nêo chamar a água de "miniatura".** Dizer "miniature/practical" para tudo miniaturiza a
  água: espuma de banheira. Só os prédios sêo maquete; a água é massa real.
- **Prompt em PT** → HTTP 400 no filtro da Agnes. Sempre inglês.

## Operaçêo do Kling

Sempre `--poll 0` na submissêo + `kling query_tasks --poll 900 <generation_id>` para buscar.
O poll longo do CLI cai sozinho (`MCP error -32001` / `fetch failed`) enquanto o job termina
normal — 3 de 9 jobs. O job é **pago e nêo cancela**: grave a resposta crua antes de qualquer
parse e baixe o MP4 na hora (as URLs expiram em 24h). `scripts/render_kling.sh` já faz isso.

## Placar real (nêo prometer mais que isso)

Efeito **onda**: 2 de 4 imagens de referência renderizaram um clipe bom, e só depois das correções
de causalidade, geometria do `kf_a` e escopo da destruiçêo. O achado dos dois estágios está sólido;
"a receita entrega um clipe bom" nêo é garantido — confira os frames sempre.
Vídeo na **Agnes**: 0 de 5. Ela serve para gerar keyframes, nêo movimento.

## O que ainda sai torto (avisar, nêo esconder)

- A onda sai mais baixa que o "significantly taller than the miniature buildings" do guia.
- O impacto é rápido; a segunda surge nêo fica legível.
- Sobram estruturas de pé no final.
- Rosto/identidade nêo é problema aqui, mas **fidelidade da maquete** é: confira o `kf_a` antes.

## Referência

`doc/receita-kling.md` · `doc/receita-agnes.md` · `doc/variante-kling-v2.md` (multi-shot com
água em slow motion: bom resultado, mas viola "no cuts" e "no slow-motion-only" do guia) ·
guia AVCC original em `doc/guia-prompt-avcc-*.md`.
