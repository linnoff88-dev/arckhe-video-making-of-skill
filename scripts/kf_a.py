#!/usr/bin/env python3
"""Gera o KEYFRAME A: a maquete da foto de referencia ja montada dentro do rig de efeitos.

Ingrediente decisivo da receita (ver doc/receita-kling.md): o gerador de video precisa
receber a MAQUETE como primeiro frame, nao a foto original. Com a foto crua o Kling entende
"transformar esta foto" e destroi a cidade real, sem rig e sem efeito fisico.

    ./kf_a.py <foto-referencia> <saida.png> --ratio 16x9 --efeito onda \
        --lock "the same brick power-plant hall, the same tall chimney, ..."

--lock e escrito a mao olhando a foto: a lista do que a maquete tem que reproduzir predio a
predio. Sem ele a Agnes inventa quarteiroes genericos. Sempre em INGLES: em PT o filtro de
conteudo da Agnes bloqueia prompt legitimo com HTTP 400.
"""
import argparse, base64, json, os, sys, time, urllib.request

AGNES_ENV = os.path.expanduser('~/projetos/agnes-nei/.env')
IMG_API = 'https://apihub.agnes-ai.com/v1/images/generations'
SIZE = {'16x9': '1312x736', '9x16': '736x1312'}

LOCK_FIM = ("Build ONLY what is in the reference image, as a handcrafted photorealistic physical scale "
            "miniature with visible model-making craftsmanship. No invented landmarks, no fantasy "
            "buildings, no extra monuments. ")

# Cada efeito tem seu RIG (o aparato pratico visivel) e seu ESTADO inicial.
RIGS = {
    'onda': (
        "The miniature sits inside a huge reinforced practical wave tank, with high-capacity water pumps, "
        "thick hoses and a wave generator. The pool has a wide open stretch of deep water on ONE side only, "
        "with no miniature in it; that open-water side is the wave generator side, and the miniature sits "
        "against the opposite edge. That open-water lane is wide — it takes up at least a third of the pool, "
        "enough run-up for a full wave to build. The miniature stands on a rigid platform bolted to the pool "
        "floor at a fixed height above the water line: it never floats, sinks or tilts. ",
        "The miniature is intact and dry, crew making final adjustments from the deck, tank water still calm."),
    'fogo': (
        "The miniature sits on a fireproof effects stage with gas fire bars, propane lines, flame trenches, "
        "fire extinguishers, blast shields and a standby fire crew in protective gear. ",
        "The miniature is intact and unlit, crew making final adjustments, fire bars cold."),
    'terremoto': (
        "The miniature sits on a hydraulic gimbal shake table with visible actuators, hydraulic lines, control "
        "console and dust cannons at the edges. ",
        "The miniature is intact and still, crew making final adjustments, the table at rest."),
    'explosao': (
        "The miniature sits inside a blast containment area with mortar pots, squib lines, debris netting, "
        "blast shields and a pyrotechnics supervisor at a firing board behind cover. ",
        "The miniature is intact, charges placed and wired, crew making final adjustments from behind cover."),
    'neve': (
        "The miniature sits under snow cannons, foam machines and wind fans on rigging trusses, with hoses and "
        "control units along the deck. ",
        "The miniature is intact and dry, crew making final adjustments, the cannons idle."),
}

SET = ("Ultra-realistic behind-the-scenes iPhone photo on a blockbuster film soundstage, surrounded by blue "
       "screens, lighting rigs, cranes, cables, production monitors and a cARCKHÉ camera in protective housing, "
       "crew members in black t-shirts. Handheld wide shot from a dry elevated platform 10-15 meters away, "
       "safety barrier in frame, the whole miniature and part of the production set visible. Documentary look, "
       "real production footage, not a polished movie shot. ")
SEGURANCA = ("Every crew member and every piece of equipment stands on the dry deck OUTSIDE the effects zone, behind the safety barrier, with dry shoes and dry clothes. A clear empty gap of several meters — deck, railing and barrier — separates the nearest person or camera from the edge of the miniature; nobody stands on, beside or over the miniature, and nothing overhangs it. ")
FISICA = ("Every object obeys gravity and stays in contact with the ground, the water or its own base, and the "
          "air above the effects zone is completely empty and clear. ")


def chave():
    for linha in open(AGNES_ENV):
        if linha.startswith('AGNES_API_KEY='):
            return linha.strip().split('=', 1)[1]
    sys.exit('AGNES_API_KEY nao encontrada em ' + AGNES_ENV)


def gerar(prompt, ref, size, dest, key, tentativas=5):
    body = {'model': 'agnes-image-2.1-flash', 'prompt': prompt, 'size': size,
            'extra_body': {'response_format': 'url', 'image': [ref]}}
    for t in range(1, tentativas + 1):
        try:
            r = urllib.request.Request(IMG_API, data=json.dumps(body).encode())
            r.add_header('Authorization', 'Bearer ' + key)
            r.add_header('Content-Type', 'application/json')
            d = json.loads(urllib.request.urlopen(r, timeout=400).read())
            u = d['data'][0]['url']
            open(dest, 'wb').write(urllib.request.urlopen(u, timeout=180).read())
            open(dest + '.url', 'w').write(u)
            print(f'OK {dest} ({os.path.getsize(dest)//1024} KB)\nurl: {u}')
            return u
        except Exception as e:
            print(f'  falha {t}: {str(e)[:140]}', flush=True)
            time.sleep(4 * t)
    return None


def main():
    p = argparse.ArgumentParser()
    p.add_argument('referencia')
    p.add_argument('saida')
    p.add_argument('--ratio', choices=list(SIZE), default='16x9')
    p.add_argument('--efeito', choices=list(RIGS), default='onda')
    p.add_argument('--lock', required=True, help='o que a maquete reproduz, em ingles, predio a predio')
    p.add_argument('--rig', help='sobrescreve o texto do rig (para efeitos fora da lista)')
    a = p.parse_args()

    rig, estado = RIGS[a.efeito]
    if a.rig:
        rig = a.rig.strip() + ' '
    prompt = a.lock.strip() + ' ' + LOCK_FIM + SET + rig + SEGURANCA + FISICA + estado
    ref = 'data:image/jpeg;base64,' + base64.b64encode(open(a.referencia, 'rb').read()).decode()
    if not gerar(prompt, ref, SIZE[a.ratio], a.saida, chave()):
        sys.exit('nao consegui gerar o keyframe A')


if __name__ == '__main__':
    main()
