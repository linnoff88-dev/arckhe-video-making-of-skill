---
name: making-of-simulacao
description: Transforma UMA foto de referência num vídeo behind-the-scenes ultra-realista onde aquilo vira MAQUETE dentro de um rig de efeitos práticos de estúdio e uma simulação destrói/afeta a maquete — fogo, terremoto, explosão, neve, vento, desabamento, inundação — com equipe, blue screen, gruas e equipamento em quadro. Provedor escolhível (kling | agnes). Use SEMPRE que o usuário der uma foto e pedir para simular um efeito prático sobre ela: "e se pegasse fogo", "simula um terremoto nisso", "explode essa maquete", "making of do efeito", "efeito prático de estúdio", "miniatura sendo destruída", "bastidores do efeito". Para o caso específico de tanque de ondas/tsunami use making-of-tanque-ondas.
---

# making-of-simulacao — foto → maquete → simulação prática

Projeto: `~/projetos/video-making-of-skill/` · Saída padrão: `~/projetos/output/making-of/<id>/`

Generalização do fluxo AVCC de tanque de ondas para **qualquer efeito prático**. A estrutura
que faz o vídeo funcionar não é a onda — é a separação de quatro responsabilidades no prompt:
**contexto de produção · fidelidade à referência · lógica de câmera e segurança · cronologia
da destruição**. Troque o rig e o efeito; a estrutura fica.

## A regra que define o resultado

**O gerador de vídeo recebe a MAQUETE JÁ MONTADA no rig como primeiro frame — nunca a foto de
referência.** Com a foto crua o modelo entende "transformar esta foto": o assunto real se
dissolve, o rig nunca aparece e não há efeito físico. Medido em teste controlado com o mesmo
prompt nas duas pontas.

## Estágio 1 — o keyframe A (maquete no rig)

```bash
cd ~/projetos/video-making-of-skill
scripts/kf_a.py <foto.jpg> <out>/kf_a.png --ratio 16x9 --efeito <efeito> --lock "<LOCK>"
```

`--efeito`: `onda` · `fogo` · `terremoto` · `explosao` · `neve`. Cada um traz seu rig visível
(barras de gás e trincheiras de chama; mesa sísmica hidráulica com atuadores e canhões de
poeira; morteiros, squibs e rede de contenção; canhões de neve e ventiladores). Para um efeito
fora da lista, passe `--rig "<descrição do aparato, em inglês>"`.

`--lock`: **você escreve olhando a foto**, em inglês, elemento por elemento. Sem isso a Agnes
inventa arquitetura genérica.

Depois **olhe a imagem** antes de gastar crédito de vídeo:

1. A maquete é reconhecível como a foto?
2. O rig está visível e o **espaço de corrida do efeito** existe? A geometria manda mais que o
   texto: se a maquete estiver cercada pelo efeito em todos os lados, ele vem de todos os lados.
   O efeito precisa de **um lado de origem** claro. Regenere se não estiver.

## Estágio 2 — o filme

```bash
# Kling — plano único, áudio nativo, melhor física (créditos do plano)
scripts/render_kling.sh <out>/kf_a.png <out>/filme.mp4 <prompt.txt>

# Agnes — US$ 0, exige 2 a 3 keyframes
scripts/render_agnes.py --kf A.png B.png C.png --prompt-file <prompt.txt> \
  --out <out>/filme.mp4 --ratio 16x9
```

O prompt: copie `prompts/simulacao-generica-en.txt` e preencha os campos entre chaves —
`{EFEITO}` `{RIG}` `{EQUIPAMENTO}` `{GATILHO}` `{ARRANQUE}` `{IMPACTO}` `{PRIMEIRO_DANO}`
`{SEGUNDA_ONDA}` e os tempos `{T1}` `{T2}` `{DURACAO}` `{FORMATO}`. Os três atos
(preparação/tensão → impacto → consequência) e o bloco de negativos ficam como estão: é o que
impede a "cena genérica de catástrofe".

## Não fazer (cada item custou um clipe perdido)

- **Sem frame final obrigatório** (`--tailImage`, ou A→B puro na Agnes). Ele faz o modelo
  *morfar* em vez de simular: o dano aparece por trás e as estruturas se dissolvem em vez de
  quebrar. Custo assumido: o estado final deixa de ser garantido.
- **Sem multi-shot.** Introduz cortes; a estrutura pede uma tomada contínua.
- **Não chamar o agente do efeito de "miniatura".** Água, fogo e poeira **não escalam**: dizer
  "miniature/practical" para tudo produz chama de isqueiro e espuma de banheira. Só o objeto é
  maquete; o efeito é massa real, em escala real.
- **Prompt em PT** → HTTP 400 no filtro da Agnes. Sempre inglês.
- **Peso dos destroços**: incluir sempre "realistic weight, friction, collision, and
  resistance" — sem isso os destroços flutuam sem peso, que é a queixa mais comum.

## Operação do Kling

Sempre `--poll 0` + `kling query_tasks --poll 900 <generation_id>`. O poll longo do CLI cai
sozinho enquanto o job termina normal (3 de 9 jobs). O job é **pago e não cancela**: grave a
resposta crua antes de qualquer parse e baixe o MP4 na hora (URLs expiram em 24h).
`scripts/render_kling.sh` já faz isso.

## Placar real (não prometer mais que isso)

Só o efeito **onda** foi executado, e mesmo nele: 2 de 4 imagens de referência renderizaram um
clipe bom, depois das correções de causalidade, geometria do `kf_a` e escopo da destruição.
Vídeo na **Agnes**: 0 de 5 — ela serve para gerar keyframes, não movimento.

## O que esperar

Testado de ponta a ponta no efeito **onda** (~15 clipes, dois provedores). Os outros rigs
(`fogo`, `terremoto`, `explosao`, `neve`) estão implementados a partir da mesma estrutura mas
**nunca foram executados** — ao usar pela primeira vez, gere só o `kf_a` e confira antes de
soltar o vídeo. Diga isso ao usuário em vez de entregar em silêncio.

## Referência

`README.md` do projeto · `doc/receita-kling.md` · `doc/receita-agnes.md`.
