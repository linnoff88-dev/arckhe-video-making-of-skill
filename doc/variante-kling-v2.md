# Kling v2 — receita que funcionou (onda real)

Clipe de referência: `~/projetos/output/videoanima/avcc-wave-tank/v2/kling-poa2-16x9-v2.mp4`
(15,04s · 1920x1076 · áudio nativo · `generation_id` em `kling-poa2-16x9-v2.mp4.json`)

Script executável: `kling-v2-receita.sh` (nesta mesma pasta).

## Chamada

```bash
# 1) submete SEM poll e guarda o generation_id
kling image_to_video \
  --image <kf_a.png> \
  --model kling-video-v3_0 \
  --duration 15 --resolution 1080p \
  --enable_audio true --prefer_multi_shots true \
  --poll 0 "<prompt abaixo>"

# 2) busca o resultado por query_tasks
kling query_tasks --poll 900 <generation_id>
```

**Regra fixa: sempre `--poll 0` + `query_tasks`.** O poll longo do CLI cai sozinho
(`MCP error -32001: Request timed out` / `MCP connection failed: fetch failed`) enquanto o
job termina normalmente do lado do Kling — aconteceu em 3 de 9 jobs, e piora com jobs em
paralelo. O job nunca se perde: o que importa é guardar o `generation_id`. As URLs de
resultado expiram em 24h, entêo baixe o MP4 assim que sair.

`kf_a.png` = frame da maquete **já montada no tanque**, gerado antes na Agnes
(`agnes-image-2.1-flash`, img2img a partir da foto de referência, `size` 1312x736 para 16:9
ou 736x1312 para 9:16). O usado no clipe: `~/projetos/output/videos-agnes/avcc-poa2-wave-tank/h/kf_a.png`.

## O que faz esta receita funcionar

1. **Sem `--tailImage`.** Com frame final obrigatório o modelo morfa A→B em vez de simular;
   é a causa de "a destruiçêo veio por trás" e "os prédios se dissolveram". Sem tail ele
   simula a onda de verdade. Custo: o estado final deixa de ser garantido — sobram prédios
   de pé.
2. **A água é escala REAL, só os prédios sêo maquete.** Enquanto o prompt dizia "miniature"
   e "practical debris" para tudo, o modelo miniaturizava a água também (espuma pequena,
   respingo de banheira). Água é a coisa que nêo escala.
3. **Linguagem de alta velocidade** (overcranked, 120fps reproduzido a 24, lâminas de água
   em vez de gotas) — é o truque real de cARCKHÉ e foi o que deu peso ao efeito.
4. **Frame inicial já dentro do estúdio**, entêo o clipe nêo gasta segundos na cidade real.

## Conflito conhecido com o documento AVCC

Esta receita **viola duas restrições negativas do guia**:
- `prefer_multi_shots true` introduz cortes → o guia exige "no cuts, transitions or multiple
  camera angles" (plano único contínuo).
- slow motion na água → o guia proíbe "no slow-motion-only destruction".

Também fica mais fechada que o "plano aberto a 10–15 m" pedido no guia.
Decisêo em aberto: manter a receita (melhor resultado prático) ou um meio-termo — plano
único, sem corte, com a água overcranked só na janela do impacto.

## Prompt (verbatim, inglês)

```
Overcranked high-speed cARCKHÉtography, filmed at 120fps and played back at 24fps, so the water moves in heavy slow motion. Shot 1: real aerial view of a riverside city at golden hour, wide and photographic. Shot 2: the camera pulls back and tilts, revealing that the city is a handcrafted photorealistic architectural miniature standing inside a huge reinforced practical wave tank on a film soundstage, with blue screens, lighting rigs, cranes, industrial pumps, hoses and crew in black t-shirts on the dry deck. Shot 3: on the open-water side of the tank a real full-scale wall of water, thousands of liters of genuine water mass, rises and travels laterally across the miniature; the water sheets and folds in dense slabs, not droplets, and stays photographically real at full scale while the buildings stay miniature. The wave shears the buildings off their foundations one row at a time in the direction of travel, roofs and facades breaking and tumbling low inside the moving water. A second surge strips the base. The crew stay dry on the deck behind the safety barrier; the operator and the foreground stay dry. Handheld iPhone behind-the-scenes footage, documentary look, real practical effects, not a CG disaster movie.
```
