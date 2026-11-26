ï»¿# video-making-of-skill

<div align="center">
  <img src="capa/logo.svg" alt="Arckhé AI" height="48" />
  <p><strong>Arckhé AI</strong></p>
</div>


**ê°Å¸â¡Â§ê°Å¸â¡Â· [PortuguêÂªs](README.md) êÂ· ê°Å¸â¡Âºê°Å¸â¡Â¸ [English](README.en.md) êÂ· ê°Å¸â¡Âªê°Å¸â¡Â¸ [EspaêÂ±ol](README.es.md)**

![Making Of](capa/capa.png)

## ê°Å¸ââ Guia de uso

Guia completo (landing + passo a passo): **https://inematds.github.io/video-making-of-skill/guia/**

---

Transforma **uma foto de referêÂªncia** num vêÂ­deo *behind-the-scenes* ultra-realista de efeito
prêÂ¡tico: a coisa da foto vira **maquete** dentro de um rig de estêÂºdio (tanque de ondas, mesa
sêÂ­smica, barras de fogoê¢â¬Â¦), e o efeito destrêÂ³i a maquete enquanto a equipe filma de longe.

| keyframe A ê¢â¬â a maquete montada | o resultado ê¢â¬â a onda destruindo |
|---|---|
| ![maquete](guia/assets/maquete.jpg) | ![destruiêÂ§êÂ£o](guia/assets/destruicao.jpg) |

Os dois clipes que funcionaram, ambos de 15s a partir da mesma foto ê¢â¬â [receita B](guia/assets/b-kling.mp4)
(plano êÂºnico, fiel ao guia) e [variante v2](guia/assets/v2-kling.mp4) (multi-shot com revelaêÂ§êÂ£o do estêÂºdio).
Assista no [guia](https://inematds.github.io/video-making-of-skill/guia/#video).

Baseado no guia AVCC de destruiêÂ§êÂ£o de miniatura em tanque de ondas (`doc/`), corrigido pelo
que foi **medido** gerando ~15 clipes reais em dois provedores.

## A descoberta central

> O gerador de vêÂ­deo tem que receber a **maquete jêÂ¡ montada** como primeiro frame ê¢â¬â nêÂ£o a foto
> de referêÂªncia.

Teste controlado, mesmo prompt integral do guia, mesma imagem de origem:

| | A ê¢â¬â foto crua | B ê¢â¬â maquete como frame inicial |
|---|---|---|
| abertura | a cidade real, intacta | estêÂºdio, maquete fiel |
| destruiêÂ§êÂ£o | prêÂ©dios **se dissolvem no lugar**, em cubos | prêÂ©dios **quebram** e sêÂ£o arrastados |
| onda | nenhuma | vem do lado da êÂ¡gua aberta, atravessa lateralmente |
| final | tanque vazio (sem nunca mostrar maquete nem onda) | base raspada + destroêÂ§os |

Com a foto crua o modelo entende *"transformar esta foto"*, nêÂ£o *"construir uma maquete disto"* ê¢â¬â
e nem o prompt integral com os 15 negativos vira esse jogo. Por isso o pipeline tem duas etapas.

## Pipeline

```
foto de referêÂªncia
   ê¢ââê¢ââ¬ scripts/kf_a.py ê¢ââ¬ê¢ââ¬ê¢ââ¬ê¢ââ¬ê¢ââ¬ê¢ââ¬ê¢ââ¬ê¢ââ¬ê¢ââ¬ê¢ââ¬ê¢ââ¬ê¢ââ¬ê¢ââ¬ê¢ââ¬ê¢âÂº  kf_a.png   (maquete montada no rig ê¢â¬â Agnes, US$ 0)
                                          ê¢ââ
                        ê¢âÅê¢ââ¬ê¢ââ¬ê¢ââ¬ê¢ââ¬ê¢ââ¬ê¢ââ¬ê¢ââ¬ê¢ââ¬ê¢ââ¬ê¢ââ¬ê¢ââ¬ê¢ââ¬ê¢ââ¬ê¢ââ¬ê¢ââ¬ê¢ââ¬ê¢ââ¬ê¢âÂ´ê¢ââ¬ê¢ââ¬ê¢ââ¬ê¢ââ¬ê¢ââ¬ê¢ââ¬ê¢ââ¬ê¢ââ¬ê¢ââ¬ê¢ââ¬ê¢ââ¬ê¢ââ¬ê¢ââ¬ê¢ââ¬ê¢ââ¬ê¢ââ¬ê¢ââ¬ê¢âÂ
        scripts/render_kling.sh                  scripts/render_agnes.py
        (Kling v3_0, plano êÂºnico)                (interpolaêÂ§êÂ£o 3 keyframes, US$ 0)
```

```bash
# 1) a maquete (o --lock vocêÂª escreve olhando a foto, em inglêÂªs, prêÂ©dio a prêÂ©dio)
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
| custo | crêÂ©ditos do plano | **US$ 0** |
| modo | image-to-video de 1 frame + texto | sêÂ³ `mode: keyframes`, **2 a 3 imagens** |
| êÂ¡udio | nativo, no mesmo passe | nêÂ£o |
| forêÂ§a | onda com fêÂ­sica de verdade, plano contêÂ­nuo | maquete fiel, iteraêÂ§êÂ£o barata |
| fraqueza | ancora o frame 1 na imagem dada | interpola = morfa; sem 3êÂº keyframe a onda some |

Receitas detalhadas, com as falhas medidas de cada um: `doc/receita-kling.md` e
`doc/receita-agnes.md`. A variante com multi-shot e êÂ¡gua em slow motion (boa, mas viola o
guia): `doc/variante-kling-v2.md`.

## Placar honesto

Efeito **onda**, Kling: **2 de 4** imagens de referêÂªncia renderizaram um clipe bom ê¢â¬â e sêÂ³ depois das
correêÂ§êÂµes de causalidade, geometria do `kf_a` e escopo da destruiêÂ§êÂ£o (`doc/receita-kling.md`).
VêÂ­deo na **Agnes**: **0 de 5** ê¢â¬â ela acerta os keyframes, nêÂ£o o movimento (`doc/receita-agnes.md`).
A descoberta dos dois estêÂ¡gios acima estêÂ¡ sustentada pelo teste A vs B; "a receita entrega um clipe
bom" nêÂ£o êÂ© garantido.

## Regras que custaram caro

- **Prompt sempre em inglêÂªs.** Em PT a Agnes bloqueia prompt legêÂ­timo com HTTP 400.
- **Nada de `--tailImage` / Aê¢â âB puro.** Frame final obrigatêÂ³rio faz o modelo *morfar* em vez de
  simular: a destruiêÂ§êÂ£o chega por trêÂ¡s e os prêÂ©dios se dissolvem. Custo de tirar: o "nada resta"
  deixa de ser garantido.
- **A êÂ¡gua nêÂ£o escala.** Dizer "miniature" para tudo miniaturiza tambêÂ©m a êÂ¡gua (espuma de
  banheira). SêÂ³ os prêÂ©dios sêÂ£o maquete; a êÂ¡gua êÂ© massa real.
- **A geometria manda mais que o texto.** "A onda vem do lado da êÂ¡gua aberta" nêÂ£o adianta se o
  `kf_a` mostra a maquete como ilha cercada de êÂ¡gua: sai onda de dois lados. A maquete tem que
  encostar em uma borda, com uma faixa larga de êÂ¡gua aberta num lado sêÂ³.
- **Causalidade tem que ser dita.** "Nenhum prêÂ©dio êÂ© danificado atêÂ© a êÂ¡gua tocêÂ¡-lo; o dano aparece
  sêÂ³ onde a êÂ¡gua jêÂ¡ passou" ê¢â¬â sem essa regra espacial a destruiêÂ§êÂ£o acontece antes da onda chegar.
- **"Scenery" significa o cenêÂ¡rio do ESTêÅ¡DIO**, nêÂ£o a maquete. Escrever "chunks of handcrafted
  scenery" fez o modelo arrastar cêÂ¢meras, refletores e flight cases para dentro da êÂ¡gua.
- **"Tank" convoca um tanque de guerra.** Apareceu um blindado na piscina em duas geraêÂ§êÂµes
  seguidas. Use `effects pool` / `water basin`.
- **Kling: sempre `--poll 0` + `query_tasks`.** O poll longo cai (3 de 9 jobs) enquanto o job
  pago termina normal. Grave o `generation_id` antes de qualquer parse.

## Skills

Vivem em `skills/`, dentro deste repo:

- **`making-of-tanque-ondas`** ê¢â¬â o caso AVCC: destruiêÂ§êÂ£o de maquete em tanque de ondas.
- **`making-of-simulacao`** ê¢â¬â genêÂ©rica: qualquer simulaêÂ§êÂ£o prêÂ¡tica (fogo, terremoto, explosêÂ£o,
  neve, vento) com a mesma estrutura de dois estêÂ¡gios.

Para instalar no Claude Code, aponte `~/.claude/skills/` para elas por symlink ê¢â¬â assim editar
num lugar edita no outro e a skill nunca sai de sincronia com o cêÂ³digo que ela descreve:

```bash
ln -s "$PWD/skills/making-of-tanque-ondas" ~/.claude/skills/making-of-tanque-ondas
ln -s "$PWD/skills/making-of-simulacao"    ~/.claude/skills/making-of-simulacao
```

## PrêÂ©-requisitos

`AGNES_API_KEY` em `~/projetos/agnes-nei/.env` êÂ· CLI `kling` logado (`kling who_am_i`) êÂ·
`ffmpeg`/`ffprobe` no PATH.

## Estrutura

```
doc/       guia AVCC original (PT/EN), receitas medidas, fotos de referêÂªncia
prompts/   prompts prontos, em inglêÂªs, validados
scripts/   kf_a.py êÂ· render_kling.sh êÂ· render_agnes.py
skills/    making-of-tanque-ondas êÂ· making-of-simulacao
guia/      a pêÂ¡gina publicada (landing + guia) + assets
```

---

<div align="center">
  <img src="capa/logo.svg" alt="Arckhé AI" height="32" />
  <p><strong>Arckhé AI</strong></p>
</div>