# video-making-of-skill

<div align="center">
  <img src="capa/logo.svg" alt="Arckhé AI" height="48" />
  <p><strong>Arckhé AI</strong></p>
</div>


**ðŸ‡§ðŸ‡· [PortuguÃªs](README.md) Â· ðŸ‡ºðŸ‡¸ [English](README.en.md) Â· ðŸ‡ªðŸ‡¸ [EspaÃ±ol](README.es.md)**

![Making Of](capa/capa.png)

## ðŸ“– Guia de uso

Guia completo (landing + passo a passo): **https://inematds.github.io/video-making-of-skill/guia/**

---

Transforma **uma foto de referÃªncia** num vÃ­deo *behind-the-scenes* ultra-realista de efeito
prÃ¡tico: a coisa da foto vira **maquete** dentro de um rig de estÃºdio (tanque de ondas, mesa
sÃ­smica, barras de fogoâ€¦), e o efeito destrÃ³i a maquete enquanto a equipe filma de longe.

| keyframe A â€” a maquete montada | o resultado â€” a onda destruindo |
|---|---|
| ![maquete](guia/assets/maquete.jpg) | ![destruiÃ§Ã£o](guia/assets/destruicao.jpg) |

Os dois clipes que funcionaram, ambos de 15s a partir da mesma foto â€” [receita B](guia/assets/b-kling.mp4)
(plano Ãºnico, fiel ao guia) e [variante v2](guia/assets/v2-kling.mp4) (multi-shot com revelaÃ§Ã£o do estÃºdio).
Assista no [guia](https://inematds.github.io/video-making-of-skill/guia/#video).

Baseado no guia AVCC de destruiÃ§Ã£o de miniatura em tanque de ondas (`doc/`), corrigido pelo
que foi **medido** gerando ~15 clipes reais em dois provedores.

## A descoberta central

> O gerador de vÃ­deo tem que receber a **maquete jÃ¡ montada** como primeiro frame â€” nÃ£o a foto
> de referÃªncia.

Teste controlado, mesmo prompt integral do guia, mesma imagem de origem:

| | A â€” foto crua | B â€” maquete como frame inicial |
|---|---|---|
| abertura | a cidade real, intacta | estÃºdio, maquete fiel |
| destruiÃ§Ã£o | prÃ©dios **se dissolvem no lugar**, em cubos | prÃ©dios **quebram** e sÃ£o arrastados |
| onda | nenhuma | vem do lado da Ã¡gua aberta, atravessa lateralmente |
| final | tanque vazio (sem nunca mostrar maquete nem onda) | base raspada + destroÃ§os |

Com a foto crua o modelo entende *"transformar esta foto"*, nÃ£o *"construir uma maquete disto"* â€”
e nem o prompt integral com os 15 negativos vira esse jogo. Por isso o pipeline tem duas etapas.

## Pipeline

```
foto de referÃªncia
   â””â”€ scripts/kf_a.py â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â–º  kf_a.png   (maquete montada no rig â€” Agnes, US$ 0)
                                          â”‚
                        â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”´â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
        scripts/render_kling.sh                  scripts/render_agnes.py
        (Kling v3_0, plano Ãºnico)                (interpolaÃ§Ã£o 3 keyframes, US$ 0)
```

```bash
# 1) a maquete (o --lock vocÃª escreve olhando a foto, em inglÃªs, prÃ©dio a prÃ©dio)
scripts/kf_a.py doc/poa2.jpg out/kf_a.png --ratio 16x9 --efeito onda \
  --lock "the same orange-brick riverside power-plant hall, the same tall slender chimney, \
          the same white apartment blocks behind the treeline, the same curved promenade"

# 2) o filme
scripts/render_kling.sh out/kf_a.png out/filme.mp4 prompts/avcc-ondas-16x9-en.txt
```

## Os dois provedores

| | Kling (`render_kling.sh`) | Agnes (`render_agnes.py`) |
|---|---|---|
| modelo | `kling-video-v3_0`, assinatura Pro/SVIP | `agnes-video-v2.0` |
| custo | crÃ©ditos do plano | **US$ 0** |
| modo | image-to-video de 1 frame + texto | sÃ³ `mode: keyframes`, **2 a 3 imagens** |
| Ã¡udio | nativo, no mesmo passe | nÃ£o |
| forÃ§a | onda com fÃ­sica de verdade, plano contÃ­nuo | maquete fiel, iteraÃ§Ã£o barata |
| fraqueza | ancora o frame 1 na imagem dada | interpola = morfa; sem 3Âº keyframe a onda some |

Receitas detalhadas, com as falhas medidas de cada um: `doc/receita-kling.md` e
`doc/receita-agnes.md`. A variante com multi-shot e Ã¡gua em slow motion (boa, mas viola o
guia): `doc/variante-kling-v2.md`.

## Placar honesto

Efeito **onda**, Kling: **2 de 4** imagens de referÃªncia renderizaram um clipe bom â€” e sÃ³ depois das
correÃ§Ãµes de causalidade, geometria do `kf_a` e escopo da destruiÃ§Ã£o (`doc/receita-kling.md`).
VÃ­deo na **Agnes**: **0 de 5** â€” ela acerta os keyframes, nÃ£o o movimento (`doc/receita-agnes.md`).
A descoberta dos dois estÃ¡gios acima estÃ¡ sustentada pelo teste A vs B; "a receita entrega um clipe
bom" nÃ£o Ã© garantido.

## Regras que custaram caro

- **Prompt sempre em inglÃªs.** Em PT a Agnes bloqueia prompt legÃ­timo com HTTP 400.
- **Nada de `--tailImage` / Aâ†’B puro.** Frame final obrigatÃ³rio faz o modelo *morfar* em vez de
  simular: a destruiÃ§Ã£o chega por trÃ¡s e os prÃ©dios se dissolvem. Custo de tirar: o "nada resta"
  deixa de ser garantido.
- **A Ã¡gua nÃ£o escala.** Dizer "miniature" para tudo miniaturiza tambÃ©m a Ã¡gua (espuma de
  banheira). SÃ³ os prÃ©dios sÃ£o maquete; a Ã¡gua Ã© massa real.
- **A geometria manda mais que o texto.** "A onda vem do lado da Ã¡gua aberta" nÃ£o adianta se o
  `kf_a` mostra a maquete como ilha cercada de Ã¡gua: sai onda de dois lados. A maquete tem que
  encostar em uma borda, com uma faixa larga de Ã¡gua aberta num lado sÃ³.
- **Causalidade tem que ser dita.** "Nenhum prÃ©dio Ã© danificado atÃ© a Ã¡gua tocÃ¡-lo; o dano aparece
  sÃ³ onde a Ã¡gua jÃ¡ passou" â€” sem essa regra espacial a destruiÃ§Ã£o acontece antes da onda chegar.
- **"Scenery" significa o cenÃ¡rio do ESTÃšDIO**, nÃ£o a maquete. Escrever "chunks of handcrafted
  scenery" fez o modelo arrastar cÃ¢meras, refletores e flight cases para dentro da Ã¡gua.
- **"Tank" convoca um tanque de guerra.** Apareceu um blindado na piscina em duas geraÃ§Ãµes
  seguidas. Use `effects pool` / `water basin`.
- **Kling: sempre `--poll 0` + `query_tasks`.** O poll longo cai (3 de 9 jobs) enquanto o job
  pago termina normal. Grave o `generation_id` antes de qualquer parse.

## Skills

Vivem em `skills/`, dentro deste repo:

- **`making-of-tanque-ondas`** â€” o caso AVCC: destruiÃ§Ã£o de maquete em tanque de ondas.
- **`making-of-simulacao`** â€” genÃ©rica: qualquer simulaÃ§Ã£o prÃ¡tica (fogo, terremoto, explosÃ£o,
  neve, vento) com a mesma estrutura de dois estÃ¡gios.

Para instalar no Claude Code, aponte `~/.claude/skills/` para elas por symlink â€” assim editar
num lugar edita no outro e a skill nunca sai de sincronia com o cÃ³digo que ela descreve:

```bash
ln -s "$PWD/skills/making-of-tanque-ondas" ~/.claude/skills/making-of-tanque-ondas
ln -s "$PWD/skills/making-of-simulacao"    ~/.claude/skills/making-of-simulacao
```

## PrÃ©-requisitos

`AGNES_API_KEY` em `~/projetos/agnes-nei/.env` Â· CLI `kling` logado (`kling who_am_i`) Â·
`ffmpeg`/`ffprobe` no PATH.

## Estrutura

```
doc/       guia AVCC original (PT/EN), receitas medidas, fotos de referÃªncia
prompts/   prompts prontos, em inglÃªs, validados
scripts/   kf_a.py Â· render_kling.sh Â· render_agnes.py
skills/    making-of-tanque-ondas Â· making-of-simulacao
guia/      a pÃ¡gina publicada (landing + guia) + assets
```

---

<div align="center">
  <img src="capa/logo.svg" alt="Arckhé AI" height="32" />
  <p><strong>Arckhé AI</strong></p>
</div>