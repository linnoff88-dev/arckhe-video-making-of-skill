#!/usr/bin/env python3
"""Gera os keyframes B (meio do impacto) e C (arrasado) a partir do keyframe A.

So a Agnes precisa deles: ela nao e image-to-video, so interpola (`mode: keyframes`, 2 a 3
imagens). Com 2 keyframes ela MORFA — a onda nao aparece e os predios sao substituidos por
casinhas genericas. O B, com o efeito no MEIO do caminho, e o que faz o efeito existir na tela.

    ./kf_bc.py <kf_a.png> --ratio 16x9 --efeito onda --out-b B.png --out-c C.png

Deriva de A (img2img usando o proprio A como referencia), para manter camera, luz e set.
"""
import argparse, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kf_a import SIZE, chave, gerar   # reaproveita cliente e retry

MESMO = ("Same soundstage, same effects rig, same camera angle, same framing and same lighting as the "
         "reference image. The set contains no vehicles of any kind: no military tank, no armored vehicle, no boat, no truck. ")
SEGURANCA = ("Every crew member stays on the dry deck outside the effects zone, behind the safety barrier. "
             "Nobody is inside the effects zone. ")
FISICA = ("Every object obeys gravity and stays in contact with the ground, the water or its own base; the air "
          "above the effects zone is empty and clear. ")

MEIO = {
    'onda': ("MID-IMPACT, frozen at the exact moment of collision. The effects pool stays FULL of water from edge to edge, "
             "at the same level as in the reference image. A single breaking wave — a curling crest of real water "
             "with a white foaming lip, like an ocean wave rolling in shallow water — is travelling across the "
             "water surface and is HALFWAY across the miniature, moving sideways. It is a moving swell on the "
             "water, NOT a waterfall, NOT a dam spillway, NOT a curtain of falling water, and the water does not "
             "pour off any edge. The buildings the crest already reached are shearing off their foundations and "
             "tumbling low inside the moving water; the buildings ahead of it are still standing. The dividing "
             "line between destroyed and intact is clearly visible. "),
    'fogo': ("MID-EVENT: the fire bars are lit and a wall of real flame is halfway across the miniature. The part "
             "already reached is burning and collapsing; the part ahead is still intact. "),
    'terremoto': ("MID-EVENT: the shake table is at full amplitude, dust cannons firing. Buildings on one side are "
                  "already toppling and cracking open; the far side still stands. "),
    'explosao': ("MID-EVENT: the charges have just fired on one side; a real blast front of debris and dust is "
                 "halfway across the miniature. The far side is still intact. "),
    'neve': ("MID-EVENT: the snow cannons and wind fans are at full power; a real wall of driven snow is halfway "
             "across the miniature, burying the near side while the far side is still clear. "),
}

FIM = ("AFTER the event: the miniature is destroyed. The effects pool is still FULL of water from edge to edge, at the "
       "same level as in the reference image, its surface churning with white foam — the water never drains and "
       "the floor is never exposed. Only the bare foundation platform remains, stripped down, awash and half "
       "submerged. The debris is a LOW, UNIFORM FIELD OF SMALL FRAGMENTS at miniature scale — no single large object, "
       "nothing bigger than a miniature building block — mixed into the white foam and floating flat ON THE WATER, "
       "pushed to the side opposite the origin of the effect. No building is left standing. Only pieces of the "
       "miniature are in the water: no cameras, no lights, no cases, no cables, no production equipment. ")

DOC = "Handheld iPhone behind-the-scenes photo, documentary look, real production footage."


def main():
    p = argparse.ArgumentParser()
    p.add_argument('kf_a')
    p.add_argument('--ratio', choices=list(SIZE), default='16x9')
    p.add_argument('--efeito', choices=list(MEIO), default='onda')
    p.add_argument('--out-b', required=True)
    p.add_argument('--out-c', required=True)
    a = p.parse_args()

    key = chave()
    # usa a URL publica do A se existir (evita reenviar 1,5 MB de base64 duas vezes)
    ref_a = (open(a.kf_a + '.url').read().strip() if os.path.exists(a.kf_a + '.url')
             else 'data:image/png;base64,' + __import__('base64').b64encode(open(a.kf_a, 'rb').read()).decode())

    ub = gerar(MESMO + MEIO[a.efeito] + SEGURANCA + FISICA + DOC, ref_a, SIZE[a.ratio], a.out_b, key)
    if not ub:
        sys.exit('nao consegui gerar o keyframe B')
    gerar(MESMO + FIM + SEGURANCA + FISICA + DOC, ub, SIZE[a.ratio], a.out_c, key) or sys.exit('falhou o C')


if __name__ == '__main__':
    main()
