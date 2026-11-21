#!/usr/bin/env python3
"""RECEITA AGNES — interpolacao por keyframes (doc/receita-agnes.md).

A Agnes NAO e image-to-video: `/v1/videos` so tem `mode: keyframes`, e exige 2 a 3 imagens
(`keyframes mode requires 2 to 3 images`, HTTP 400 com uma so). Ou seja, ela nao consegue
executar o guia AVCC como escrito — o guia pressupoe UMA imagem de referencia e o modelo
construindo os 15s a partir do texto.

Consequencias medidas, que definem como escrever para ela:
  - o prompt de video tem influencia fraca; quem manda sao os keyframes;
  - com 2 keyframes (A intacto -> C destruido) ela MORFA: a onda nao aparece e os predios
    sao SUBSTITUIDOS por casinhas genericas em vez de quebrarem;
  - por isso o padrao aqui e 3 keyframes: A intacto, B com o efeito NO MEIO DO IMPACTO,
    C arrasado. O efeito passa a existir na tela em vez de ser inferido.

    ./render_agnes.py --kf A.png B.png C.png --prompt-file prompts/x.md --out filme.mp4 --ratio 16x9
"""
import argparse, base64, json, os, subprocess, sys, time, urllib.request, urllib.error

AGNES_ENV = os.path.expanduser('~/projetos/agnes-nei/.env')
VID_API = 'https://apihub.agnes-ai.com/v1/videos'
VID_GET = 'https://apihub.agnes-ai.com/agnesapi?video_id='
WH = {'16x9': (1312, 736), '9x16': (736, 1312)}
FPS = 24


def chave():
    for linha in open(AGNES_ENV):
        if linha.startswith('AGNES_API_KEY='):
            return linha.strip().split('=', 1)[1]
    sys.exit('AGNES_API_KEY nao encontrada em ' + AGNES_ENV)


def req(url, key, body=None, timeout=300):
    r = urllib.request.Request(url, data=json.dumps(body).encode() if body else None)
    r.add_header('Authorization', 'Bearer ' + key)
    if body:
        r.add_header('Content-Type', 'application/json')
    return json.loads(urllib.request.urlopen(r, timeout=timeout).read())


def como_keyframe(caminho):
    """URL publica se houver .url ao lado; senao data URI (funciona, apesar da doc negar)."""
    if os.path.exists(caminho + '.url'):
        return open(caminho + '.url').read().strip()
    ext = 'jpeg' if caminho.lower().endswith(('.jpg', '.jpeg')) else 'png'
    return f'data:image/{ext};base64,' + base64.b64encode(open(caminho, 'rb').read()).decode()


def dur(p):
    r = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                        '-of', 'csv=p=0', p], capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except ValueError:
        return 0.0


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--kf', nargs='+', required=True, help='2 a 3 keyframes, em ordem')
    p.add_argument('--prompt-file', required=True)
    p.add_argument('--out', required=True)
    p.add_argument('--ratio', choices=list(WH), default='16x9')
    p.add_argument('--segundos', type=float, default=15.0)
    a = p.parse_args()

    if not 2 <= len(a.kf) <= 3:
        sys.exit('a Agnes aceita 2 a 3 keyframes (com 1 devolve HTTP 400)')

    # num_frames <= 441 (18,4s @24fps) e regra 8n+1
    frames = min(441, int(a.segundos * FPS))
    frames = ((frames - 1) // 8) * 8 + 1

    key = chave()
    w, h = WH[a.ratio]
    body = {'model': 'agnes-video-v2.0', 'prompt': open(a.prompt_file).read().strip(),
            'num_frames': frames, 'frame_rate': FPS, 'seed': 12345, 'width': w, 'height': h,
            'extra_body': {'image': [como_keyframe(k) for k in a.kf], 'mode': 'keyframes'}}

    vid = None
    for t in range(1, 5):
        try:
            d = req(VID_API, key, body)
            vid = d.get('video_id') or d.get('id')
            print('video_id:', vid, flush=True)
            break
        except urllib.error.HTTPError as e:
            print(f'HTTP {e.code}: {e.read()[:200].decode(errors="ignore")}', flush=True)
            time.sleep(70 if e.code == 429 else 6 * t)   # 429 = rate limit real, 5 req/min
        except Exception as e:
            print('erro:', str(e)[:150], flush=True)
            time.sleep(6 * t)
    if not vid:
        sys.exit('nao consegui submeter')

    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    t0 = time.time()
    while time.time() - t0 < 2400:
        try:
            d = req(VID_GET + vid, key, timeout=120)
            st = d.get('status')
            if st == 'completed':
                u = d.get('url') or (d.get('data') or [{}])[0].get('url') or d.get('video_url')
                open(a.out, 'wb').write(urllib.request.urlopen(u, timeout=600).read())
                # o `size` da resposta MENTE — medir com ffprobe
                print(f'OK {a.out} · {dur(a.out):.1f}s')
                return
            if st == 'failed':
                sys.exit('FALHOU: ' + json.dumps(d)[:300])
        except Exception:
            pass
        time.sleep(15)
    sys.exit('timeout no poll')


if __name__ == '__main__':
    main()
