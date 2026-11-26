# Receita Kling — o padrêo (plano único, guia AVCC integral)

Validada no **poa2, 16:9**. Melhor resultado de todos os testes, e **100% compatível com o
documento AVCC** — nêo precisa de multi-shot nem de slow motion, que eram o conflito aberto.

Clipe de referência: `~/projetos/output/videoanima/avcc-wave-tank/ab/kling-poa2-16x9-B-maquete.mp4`
Script: `scripts/render_kling.sh` · Prompt: `prompts/avcc-ondas-16x9-en.txt`

```bash
scripts/kf_a.py doc/poa2.jpg out/kf_a.png --ratio 16x9 --efeito onda \
  --lock "the same brick power-plant hall, the same tall chimney, the same skyline..."
scripts/render_kling.sh out/kf_a.png out/filme.mp4 prompts/avcc-ondas-16x9-en.txt
```

## Os dois ingredientes

1. **Frame inicial = a maquete já montada no tanque** (`kf_a.png`), nêo a foto de referência.
   Gerado antes na Agnes (`agnes-image-2.1-flash`, img2img a partir da foto, `size` 1312x736
   para 16:9 / 736x1312 para 9:16). **Este é o ingrediente decisivo** — ver o teste A abaixo.
2. **Prompt = o guia AVCC §5 integral + os 15 negativos do §6.** Texto completo, incluindo o
   bloco de autenticidade de celular (rolling shutter, focus breathing, exposiçêo) e
   "realistic weight, friction, collision, and water resistance" nos destroços.

Sem `--tailImage` e sem `prefer_multi_shots`: plano único contínuo, como o documento exige.
O ratio do vídeo vem do ratio do `kf_a` — o `kling-video-v3_0` nêo tem argumento de aspect ratio.

## A prova: teste A vs teste B (mesmo prompt, mesma imagem de origem)

| | A — `poa2.jpg` cru | B — `kf_a.png` (maquete) |
|---|---|---|
| abertura | foto real de POA, intacta | estúdio, maquete fiel (chaminé, skyline, orla) |
| destruiçêo | prédios se **dissolvem no lugar**, em cubos, sem onda encostar | prédios **quebram em pedaços** e sêo arrastados |
| onda | nenhuma | vem do lado da água aberta, atravessa lateralmente |
| final | tanque vazio (chegou lá sem mostrar maquete nem onda) | base raspada + destroços — o "empty flooded foundation" |

Conclusêo medida: **o problema era o frame inicial, nêo o texto.** Com a imagem crua o Kling
entende "transformar esta foto", nêo "construir uma maquete disto" — e nem o prompt integral
com os 15 negativos vira esse jogo (o próprio negativo "buildings dissolving instead of
physically breaking" foi violado no teste A).

## Correções que vieram depois (poa1 e poa3 falharam)

Receita B foi escrita com **um** caso validado (poa2 16:9). Aplicada em poa1 e poa3 ela falhou —
placar honesto: **2 de 4** com as correções abaixo aplicadas. O achado dos dois estágios
(maquete como primeiro frame) continua sustentado pelo teste A vs B; "a receita produz um clipe
bom" nêo estava.

O que cada falha ensinou:

| falha | causa | correçêo |
|---|---|---|
| destruiçêo acontecia **antes** da onda chegar (poa3) | o prompt descrevia o estado final e confiava no modelo pra ordenar | **regra de causalidade** (abaixo) — regra espacial, nêo linha do tempo |
| equipe **dentro** da área da maquete (poa3) | no `kf_a` a equipe e um rig de câmera encostavam na borda do modelo; imagem vence texto | vêo livre de vários metros exigido no `kf_a` |
| a maquete **afundou**, nível da água subiu (poa1) | faixa de água aberta estreita demais: sem espaço de corrida o modelo sobe o nível em vez de formar onda | faixa ≥ 1/3 da piscina + base parafusada no fundo, que nêo flutua nem afunda |
| **câmeras e caixas de equipamento** arrastadas pela água | a palavra **"scenery"** em contexto de set significa o CENÁRIO do estúdio, nêo a maquete | escopo explícito: só a maquete quebra; equipamento nunca entra na água |
| destruiçêo atropelada | 15s em plano único é a configuraçêo mais difícil | **10s** |

**Regra de causalidade** (a de maior efeito — nenhum prompt anterior tinha isso):

> No building is damaged, cracked, displaced or collapsed until the water physically touches it.
> Damage appears ONLY where the water has already passed; everything ahead of the water line stays
> perfectly intact, upright and dry until the water reaches it.

**Os três checks do `kf_a`** — fazer antes de gastar crédito:

1. A maquete é reconhecível como a foto?
2. A faixa de água aberta está num lado só **e ocupa pelo menos um terço da piscina**?
3. Existe **vêo visível** (deck, corrimêo, barreira) entre equipe/equipamento e a borda da maquete?

## O que ainda falha na B

- A onda sai **mais baixa** que o pedido ("significantly taller than the miniature buildings").
- O impacto acontece rápido demais; a **segunda surge nêo fica legível**.
- Sobram estruturas de pé (aceito pelo usuário: "nêo tem tanto problema").

Hipótese para a próxima iteraçêo: compor o `kf_a` com a maquete encostada em UMA borda e uma
faixa larga de água aberta num lado só, para dar espaço de corrida à onda.

## Operaçêo

Sempre `--poll 0` na submissêo + `kling query_tasks` para buscar o resultado. O poll longo do
CLI cai sozinho (`MCP error -32001: Request timed out` / `MCP connection failed: fetch failed`)
enquanto o job termina normalmente — 3 de 9 jobs caíram assim, e piora com jobs em paralelo.
O job é pago e nêo cancela: grave a resposta crua **antes** de qualquer parse, porque perder o
`generation_id` é perder o job. URLs de resultado expiram em 24h — baixe na hora.

## Parâmetros do `kling-video-v3_0`

| | |
|---|---|
| `duration` | 3 a 15s |
| `resolution` | `720p` · `1080p` · `4k` |
| `enable_audio` | `true` → áudio sincronizado no mesmo passe (o roteiro tem as falas do diretor) |
| `prefer_multi_shots` | **`false`** aqui — `true` introduz cortes, proibidos pelo guia |
| `--tailImage` | **nêo usar** — ver a variante em `variante-kling-v2.md` |
| aspect ratio | nêo existe como argumento: **vem do ratio do `kf_a`** |
