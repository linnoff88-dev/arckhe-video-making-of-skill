# Receita Agnes — interpolação por keyframes

`scripts/render_agnes.py` · custo **US$ 0** · `agnes-video-v2.0`

## O fato que define tudo

**A Agnes não é image-to-video.** O `/v1/videos` só tem `mode: keyframes` e exige 2 a 3
imagens — com uma só devolve `HTTP 400: keyframes mode requires 2 to 3 images`. Ou seja, ela
**não consegue executar o guia AVCC como escrito**, porque o guia pressupõe UMA imagem de
referência e o modelo construindo os 15 segundos a partir do texto.

Consequência: aqui o trabalho pesado não está no prompt, está nos keyframes.

## Falhas medidas (com 2 keyframes)

| sintoma | onde apareceu |
|---|---|
| a onda não aparece; a espuma cresce por igual no tanque todo | poa1, poa2 |
| os prédios são **substituídos** por casinhas genéricas em vez de quebrarem | poa2 16:9, frame ~220 |
| destruição chegando "por trás", sem a onda encostar | poa2 |
| escala da maquete muda no meio do clipe | poa2 |

A causa é a mesma do lado do Kling: **A→B é morph, não simulação.** O modelo procura o caminho
mais barato entre os dois estados, e o caminho mais barato nunca é simular física.

Agrava no caso da Agnes: o keyframe B "depois" tem espuma uniforme no tanque inteiro, então a
interpolação faz espuma crescer de todos os lados — o oposto de uma onda direcional.

## O padrão: 3 keyframes

A API aceita até 3 (`max_images: 3`). Use os três:

- **A** — maquete intacta, tanque calmo.
- **B** — o efeito **no meio do impacto**: parede de água na metade do caminho, prédios sendo
  arrancados na direção do movimento. É o keyframe que faz a onda *existir na tela* em vez de
  ser inferida.
- **C** — base raspada, destroços empurrados para o lado oposto ao do gerador de ondas.

```bash
scripts/render_agnes.py --kf A.png B.png C.png \
  --prompt-file prompts/avcc-ondas-16x9-en.txt \
  --out filme.mp4 --ratio 16x9 --segundos 15
```

## Como escrever o prompt para a Agnes

Diferente do Kling: **prompt curto, só de transição e movimento**, não descrição de cena. A
cena já está nos keyframes; texto longo de set/segurança é ignorado. Descreva *o que muda de
A para B para C*.

## Armadilhas da API (medidas)

- **Prompt em INGLÊS.** Em PT o filtro de conteúdo bloqueia prompt legítimo com HTTP 400.
- `size` explícito (`1312x736` / `736x1312`), nunca `ratio` — é ignorado em img2img.
- `num_frames ≤ 441` (18,4s @24fps), regra **8n+1**.
- **Rate limit real: 5 req/min** (HTTP 429), não 1/min como diz o guia.
- O `size` da resposta **mente** — meça com `ffprobe`. Pedindo 736x1312 sai 704x1280.
- Data URI base64 funciona nos keyframes, apesar da doc dizer que exige URL pública.
- ~34% de HTTP 503 na geração; o script já faz retry com backoff.

## Placar do movimento: 0 de 5

Cinco tentativas de **vídeo** na Agnes, cinco degenerações diferentes: 2 keyframes substituíram os
prédios por casinhas genéricas (2x); 3 keyframes produziram caixas gigantes flutuando e uma "onda
feita de coisas" (2x); e a versão com fragmentos pequenos virou um tapete uniforme de pedrinhas,
com a maquete sumida e uma pessoa dentro da piscina.

As caixas gigantes tinham causa nomeável: o keyframe do "depois" dizia **"chunks of handcrafted
scenery"**, e *scenery* em linguagem de set é o **cenário do estúdio** — o modelo passou a arrastar
câmeras, refletores e flight cases. Corrigido em todos os prompts, mas o resto da degeneração
permaneceu.

**Recomendação:** usar a Agnes só para gerar keyframes (onde ela acerta quase sempre) e deixar o
movimento com o Kling. Decisão do usuário ainda em aberto.

## Onde a Agnes ganha

Custo zero e keyframes controlados: a maquete sai fiel à referência porque cada frame é
gerado com a foto como referência de img2img. Serve para iterar composição e enquadramento
barato antes de gastar créditos no Kling — inclusive os `kf_a` que a receita Kling consome
saem daqui.
