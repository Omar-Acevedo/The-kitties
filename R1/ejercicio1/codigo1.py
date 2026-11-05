import sys
from collections import deque

# ---------------- Configuración de reglas (ajustar según la caja negra) ----------------
# WINDOW = True  -> tramo estable si max - min <= K dentro de todo el tramo
# WINDOW = False -> tramo estable si |a[i] - a[i+1]| <= K para cada par adyacente
WINDOW = True
# QMODE: tratamiento de '?'
#   'break' -> '?' corta la racha y no cuenta
#   'wild'  -> '?' es compatible con todo y cuenta en la longitud
#   'skip'  -> '?' se ignora (no corta ni cuenta); P es la posición del primer valor conocido
QMODE = 'break'
# ---------------------------------------------------------------------------------------

SCALE = 10 ** 6


def parse(tok):
    # tok: bytes, hasta 6 decimales -> entero escalado por 10^6 (sin flotantes)
    if b'.' in tok:
        i, f = tok.split(b'.')
        if i == b'' or i == b'-' or i == b'+':
            i += b'0'
        return int(i + f.ljust(6, b'0')[:6])
    return int(tok) * SCALE


def window_case(a, K, wild):
    best = 0
    bp = 1
    l = 0
    mx = deque()
    mn = deque()
    for r in range(len(a)):
        v = a[r]
        if v is None:
            if not wild:
                mx.clear()
                mn.clear()
                l = r + 1
                continue
        else:
            while mx and a[mx[-1]] <= v:
                mx.pop()
            mx.append(r)
            while mn and a[mn[-1]] >= v:
                mn.pop()
            mn.append(r)
            while a[mx[0]] - a[mn[0]] > K:
                l += 1
                if mx[0] < l:
                    mx.popleft()
                if mn[0] < l:
                    mn.popleft()
        ln = r - l + 1
        if ln > best:
            best = ln
            bp = l + 1
    return best, bp


def adj_case(a, K, wild):
    best = 0
    bp = 1
    start = 0
    prev = None
    for r in range(len(a)):
        v = a[r]
        if v is None:
            if not wild:
                start = r + 1
                prev = None
                continue
            prev = None
        else:
            if prev is not None and abs(v - prev) > K:
                start = r
            prev = v
        ln = r - start + 1
        if ln > best:
            best = ln
            bp = start + 1
    return best, bp


def solve_case(a, K):
    if QMODE == 'skip':
        pos = [i + 1 for i, v in enumerate(a) if v is not None]
        vals = [v for v in a if v is not None]
        if not vals:
            return 0, 1
        L, P = (window_case if WINDOW else adj_case)(vals, K, False)
        return L, pos[P - 1]
    wild = QMODE == 'wild'
    return (window_case if WINDOW else adj_case)(a, K, wild)


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    p = 1
    out = []
    for _ in range(t):
        n = int(data[p])
        K = parse(data[p + 1])
        p += 2
        a = [None if x == b'?' else parse(x) for x in data[p:p + n]]
        p += n
        L, P = solve_case(a, K)
        out.append("%d %d" % (L, P))
    sys.stdout.write("\n".join(out) + "\n")


main()
