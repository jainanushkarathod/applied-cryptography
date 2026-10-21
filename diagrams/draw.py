"""Draw every figure used in the modules.  Run:  python3 diagrams/draw.py"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from lib import Diagram, STYLES, INK, MUTED  # noqa: E402

ROOT = os.path.join(os.path.dirname(__file__), "..", "images")
FIGS = {}


def fig(name):
    def deco(fn):
        FIGS[name] = fn
        return fn
    return deco


def out(name):
    d = os.path.join(ROOT, os.path.dirname(name))
    os.makedirs(d, exist_ok=True)
    return os.path.join(ROOT, name)


# ---------------------------------------------------------------- Module 1
@fig("01/layers")
def layers():
    D = Diagram(15, 3.4)
    D.cbox(2.4, 1.7, 4.0, 1.9, "Primitive\nfixed size, e.g. AES\n(trusted via cryptanalysis)", style="blue", fs=10.5)
    D.arrow([(4.4, 1.7), (5.5, 1.7)])
    D.cbox(7.5, 1.7, 4.0, 1.9, "Mode\ne.g. CTR\n(trusted via a proof)", style="green", fs=10.5)
    D.arrow([(9.5, 1.7), (10.6, 1.7)])
    D.cbox(12.6, 1.7, 4.0, 1.9, "Scheme\nCTR[AES_K]\nencrypts any length", style="orange", fs=10.5)
    D.save(out("01/layers"))


@fig("01/distinguisher")
def distinguisher():
    D = Diagram(14, 6.4)
    D.cbox(7.0, 5.2, 6.4, 1.4, "Distinguisher D\nq queries, t offline work\noutputs a guess: 1 (real) or 0 (ideal)",
           style="purple", fs=10.5)
    D.region(0.5, 0.4, 13.0, 2.6, "")
    D.text(7.0, 0.7, "one of the two worlds, chosen secretly", fs=9.5, color=MUTED)
    D.cbox(3.6, 1.9, 4.6, 1.2, "Real world\nthe scheme with secret key K", style="blue", fs=10.5)
    D.cbox(10.4, 1.9, 4.6, 1.2, "Ideal world\nperfectly random object", style="green", fs=10.5)
    D.arrow([(5.6, 4.5), (3.9, 2.5)], both=True, color="#777777")
    D.arrow([(8.4, 4.5), (10.1, 2.5)], both=True, color="#777777")
    D.text(4.2, 3.6, "queries / answers", fs=9.5, color=MUTED, ha="right")
    D.text(9.8, 3.6, "queries / answers", fs=9.5, color=MUTED, ha="left")
    D.save(out("01/distinguisher"))


@fig("01/keysearch")
def keysearch():
    D = Diagram(19, 2.8)
    boxes = [("1. one query\nC = O(0)", "grey"), ("2. offline: try t keys K′\nis E_K′(0) = C ?", "grey"),
             ("match: output 1 (real)\nno match: output 0", "orange"),
             ("advantage ≈ t / 2ᵏ\n⇒ at most k bits of security", "blue")]
    for i, (t, st) in enumerate(boxes):
        x = 2.2 + i * 4.85
        D.cbox(x, 1.4, 4.0, 1.5, t, style=st, fs=10.5)
        if i:
            D.arrow([(x - 2.85, 1.4), (x - 2.0, 1.4)])
    D.save(out("01/keysearch"))


# ---------------------------------------------------------------- Module 2
def grid(D, x, y, c=0.42, hl=(), hlstyle="orange", labels=None):
    for r in range(4):
        for k in range(4):
            st = hlstyle if (r, k) in hl else "white"
            D.box(x + k * c, y + (3 - r) * c, c, c, "", style=st, rounded=False)
            if labels:
                D.text(x + k * c + c / 2, y + (3 - r) * c + c / 2, labels[r][k], fs=8)


@fig("02/aes-round")
def aes_round():
    D = Diagram(19, 6.2)
    steps = [("SubBytes", "same S-box on\nevery byte", "non-linear"),
             ("ShiftRows", "row r rotates\nleft by r", "shuffling"),
             ("MixColumns", "each column ×\nfixed matrix", "mixing"),
             ("AddRoundKey", "XOR the\nround key", "key")]
    D.text(0.95, 5.6, "state", fs=10, color=MUTED)
    grid(D, 0.1, 2.6, labels=[["a"] * 4] * 4)
    x = 2.6
    letters = [list("mnop"), list("ghij"), list("wxyz"), list("bcde")]
    for i, (name, desc, role) in enumerate(steps):
        bx = x + i * 4.2
        D.arrow([(bx - 0.5, 3.45), (bx + 0.1, 3.45)])
        D.box(bx + 0.1, 4.5, 3.0, 0.8, name, style="blue", fs=11, bold=True)
        D.text(bx + 1.6, 5.6, role, fs=9, color=MUTED, italic=True)
        if i == 0:
            grid(D, bx + 0.75, 2.6, hl={(1, 2)})
        elif i == 1:
            shifted = [letters[r][r:] + letters[r][:r] for r in range(4)]
            grid(D, bx + 0.75, 2.6, labels=shifted)
        elif i == 2:
            grid(D, bx + 0.75, 2.6, hl={(r, 1) for r in range(4)}, hlstyle="green")
        else:
            grid(D, bx + 0.75, 2.6, hl={(r, k) for r in range(4) for k in range(4)}, hlstyle="purple")
        D.text(bx + 1.6, 1.7, desc, fs=9.5)
    D.arrow([(19.0 - 0.9, 3.45), (19.0 - 0.3, 3.45)])
    D.text(9.5, 0.55, "Repeated 10 / 12 / 14 times (no MixColumns in the last round). "
           "Two rounds already make every output byte depend on every input byte.", fs=9.5,
           color=MUTED)
    D.save(out("02/aes-round"))


def mode_panel(D, ox, oy, mode):
    D.text(ox + 4.2, oy + 5.3, mode, fs=13, bold=True)
    xs = [ox + 1.6, ox + 4.2, ox + 6.8]
    for i, x in enumerate(xs):
        n = i + 1
        if mode == "ECB":
            D.text(x, oy + 4.5, f"M{n}", fs=11)
            D.arrow([(x, oy + 4.2), (x, oy + 3.25)])
            D.cbox(x, oy + 2.85, 1.3, 0.8, "E_K")
            D.arrow([(x, oy + 2.45), (x, oy + 1.4)])
            D.text(x, oy + 1.1, f"C{n}", fs=11)
        elif mode == "CBC":
            D.text(x, oy + 4.6, f"M{n}", fs=11)
            D.arrow([(x, oy + 4.3), (x, oy + 3.92)])
            D.xor(x, oy + 3.7)
            D.arrow([(x, oy + 3.48), (x, oy + 3.0)])
            D.cbox(x, oy + 2.6, 1.3, 0.8, "E_K")
            D.arrow([(x, oy + 2.2), (x, oy + 1.4)])
            D.text(x, oy + 1.1, f"C{n}", fs=11)
            if i < 2:
                D.arrow([(x, oy + 1.8), (x + 1.3, oy + 1.8), (x + 1.3, oy + 3.7), (xs[i + 1] - 0.22, oy + 3.7)])
            if i == 0:
                D.text(ox + 0.25, oy + 3.7, "IV", fs=11)
                D.arrow([(ox + 0.55, oy + 3.7), (x - 0.22, oy + 3.7)])
        elif mode == "OFB":
            D.cbox(x, oy + 3.9, 1.3, 0.8, "E_K")
            if i == 0:
                D.text(ox + 0.25, oy + 3.9, "IV", fs=11)
                D.arrow([(ox + 0.55, oy + 3.9), (x - 0.65, oy + 3.9)])
            else:
                D.arrow([(xs[i - 1] + 0.65, oy + 3.9), (x - 0.65, oy + 3.9)])
            D.arrow([(x, oy + 3.5), (x, oy + 2.42)])
            D.xor(x, oy + 2.2)
            D.text(x - 1.0, oy + 2.2, f"M{n}", fs=11)
            D.arrow([(x - 0.7, oy + 2.2), (x - 0.22, oy + 2.2)])
            D.arrow([(x, oy + 1.98), (x, oy + 1.4)])
            D.text(x, oy + 1.1, f"C{n}", fs=11)
        elif mode == "CTR":
            D.text(x, oy + 4.9, f"N‖{n}", fs=11)
            D.arrow([(x, oy + 4.6), (x, oy + 4.3)])
            D.cbox(x, oy + 3.9, 1.3, 0.8, "E_K")
            D.arrow([(x, oy + 3.5), (x, oy + 2.42)])
            D.xor(x, oy + 2.2)
            D.text(x - 1.0, oy + 2.2, f"M{n}", fs=11)
            D.arrow([(x - 0.7, oy + 2.2), (x - 0.22, oy + 2.2)])
            D.arrow([(x, oy + 1.98), (x, oy + 1.4)])
            D.text(x, oy + 1.1, f"C{n}", fs=11)


@fig("02/modes")
def modes():
    D = Diagram(17.4, 12)
    mode_panel(D, 0, 6, "ECB")
    mode_panel(D, 8.9, 6, "CBC")
    mode_panel(D, 0, 0.2, "OFB")
    mode_panel(D, 8.9, 0.2, "CTR")
    D.save(out("02/modes"))


# ---------------------------------------------------------------- Module 3
@fig("03/wc-vs-ph")
def wc_vs_ph():
    D = Diagram(14, 6.6)
    # Wegman-Carter
    D.text(3.2, 6.2, "Wegman-Carter", fs=13, bold=True)
    D.text(1.8, 5.4, "M", fs=12)
    D.text(4.6, 5.4, "N", fs=12)
    D.arrow([(1.8, 5.1), (1.8, 4.5)])
    D.arrow([(4.6, 5.1), (4.6, 4.5)])
    D.cbox(1.8, 4.05, 1.5, 0.9, "H_L", style="green")
    D.cbox(4.6, 4.05, 1.5, 0.9, "F_K or E_K")
    D.arrow([(1.8, 3.6), (1.8, 2.3), (2.98, 2.3)])
    D.arrow([(4.6, 3.6), (4.6, 2.3), (3.42, 2.3)])
    D.xor(3.2, 2.3)
    D.arrow([(3.2, 2.08), (3.2, 1.3)])
    D.text(3.2, 1.0, "T", fs=12)
    D.text(3.2, 0.3, "hash masked by a one-time value", fs=9.5, color=MUTED)
    # Protected hash
    D.text(10.6, 6.2, "Protected hash", fs=13, bold=True)
    D.text(10.6, 5.4, "M", fs=12)
    D.arrow([(10.6, 5.1), (10.6, 4.5)])
    D.cbox(10.6, 4.05, 1.5, 0.9, "H_L", style="green")
    D.arrow([(10.6, 3.6), (10.6, 3.05)])
    D.cbox(10.6, 2.6, 1.9, 0.9, "F_K or E_K")
    D.arrow([(10.6, 2.15), (10.6, 1.3)])
    D.text(10.6, 1.0, "T", fs=12)
    D.text(10.6, 0.3, "no nonce: hash protected by a PRF/PRP", fs=9.5, color=MUTED)
    D.save(out("03/wc-vs-ph"))


# ---------------------------------------------------------------- Module 4
@fig("04/generic-composition")
def generic():
    D = Diagram(18, 6.4)
    titles = ["Encrypt-and-MAC", "MAC-then-Encrypt", "Encrypt-then-MAC"]
    for i, t in enumerate(titles):
        ox = i * 6.1
        D.text(ox + 2.9, 6.0, t, fs=12.5, bold=True)
        D.text(ox + (1.6 if i == 2 else 2.9), 5.25, "M", fs=12)
        if i == 0:
            D.line([(ox + 2.9, 5.0), (ox + 2.9, 4.7)])
            D.line([(ox + 1.6, 4.7), (ox + 4.2, 4.7)])
            D.arrow([(ox + 1.6, 4.7), (ox + 1.6, 4.05)])
            D.arrow([(ox + 4.2, 4.7), (ox + 4.2, 4.05)])
            D.cbox(ox + 1.6, 3.6, 1.6, 0.9, "Enc_K1")
            D.cbox(ox + 4.2, 3.6, 1.6, 0.9, "MAC_K2", style="green")
            D.arrow([(ox + 1.6, 3.15), (ox + 1.6, 2.2)])
            D.arrow([(ox + 4.2, 3.15), (ox + 4.2, 2.2)])
            D.text(ox + 1.6, 1.9, "C", fs=12)
            D.text(ox + 4.2, 1.9, "T", fs=12)
            D.text(ox + 2.9, 0.9, "tag on plaintext may leak", fs=9.5, color="#C0392B")
        elif i == 1:
            D.line([(ox + 2.9, 5.0), (ox + 2.9, 4.7)])
            D.line([(ox + 1.6, 4.7), (ox + 2.9, 4.7)])
            D.arrow([(ox + 2.9, 4.7), (ox + 4.2, 4.7), (ox + 4.2, 4.3)])
            D.cbox(ox + 4.2, 3.85, 1.6, 0.9, "MAC_K2", style="green")
            D.arrow([(ox + 1.6, 4.7), (ox + 1.6, 2.85)])
            D.arrow([(ox + 4.2, 3.4), (ox + 4.2, 3.15), (ox + 2.1, 3.15), (ox + 2.1, 2.85)])
            D.cbox(ox + 1.85, 2.4, 2.2, 0.9, "Enc_K1(M‖T)")
            D.arrow([(ox + 1.85, 1.95), (ox + 1.85, 1.45)])
            D.text(ox + 1.85, 1.15, "C", fs=12)
            D.text(ox + 2.9, 0.4, "decrypt before verify: padding oracles", fs=9.5, color="#C0392B")
        else:
            D.arrow([(ox + 1.6, 5.0), (ox + 1.6, 4.05)])
            D.cbox(ox + 1.6, 3.6, 1.6, 0.9, "Enc_K1")
            D.arrow([(ox + 1.6, 3.15), (ox + 1.6, 1.45)])
            D.text(ox + 1.6, 1.15, "C", fs=12)
            D.arrow([(ox + 1.6, 2.4), (ox + 4.2, 2.4), (ox + 4.2, 2.85)])
            D.cbox(ox + 4.2, 3.3, 1.6, 0.9, "MAC_K2", style="green")
            D.arrow([(ox + 4.2, 3.75), (ox + 4.2, 4.6)])
            D.text(ox + 4.2, 4.9, "T", fs=12)
            D.text(ox + 2.9, 0.4, "verify before decrypt: recommended", fs=9.5, color="#2E8B57")
    D.save(out("04/generic-composition"))


@fig("04/toy-ae")
def toy_ae():
    D = Diagram(11, 6.4)
    D.text(3.0, 6.0, "N", fs=12)
    D.arrow([(3.0, 5.7), (3.0, 5.15)])
    D.cbox(3.0, 4.7, 1.6, 0.9, "F_K")
    D.line([(3.0, 4.25), (3.0, 3.95)])
    D.line([(2.0, 3.95), (4.6, 3.95)])
    D.text(1.65, 3.6, "Z1", fs=10, color=MUTED)
    D.text(5.0, 3.6, "Z2", fs=10, color=MUTED)
    D.arrow([(2.0, 3.95), (2.0, 2.62)])
    D.xor(2.0, 2.4)
    D.text(0.4, 2.4, "M", fs=12)
    D.arrow([(0.65, 2.4), (1.78, 2.4)])
    D.arrow([(2.0, 2.18), (2.0, 1.1)])
    D.text(2.0, 0.8, "C = M ⊕ Z1", fs=11)
    # tag path
    D.line([(1.1, 2.4), (1.1, 1.6), (6.6, 1.6)])
    D.arrow([(6.6, 1.6), (6.6, 2.0)])
    D.op(6.6, 2.25, "⊗")
    D.text(7.6, 2.25, "L", fs=12)
    D.arrow([(7.35, 2.25), (6.85, 2.25)])
    D.arrow([(6.6, 2.5), (6.6, 3.95), (4.82, 3.95)])
    D.xor(4.6, 3.95)
    D.arrow([(4.6, 3.73), (4.6, 1.1)])
    D.text(4.6, 0.8, "T = Z2 ⊕ (M ⊗ L)", fs=11)
    D.save(out("04/toy-ae"))


@fig("04/gcm")
def gcm():
    D = Diagram(17, 9.6)
    xs = [1.5, 5.1, 8.7, 12.3]
    labels = ["J0 = N‖0…01", "N‖…2", "N‖…3", "N‖…ℓ+1"]
    for i, x in enumerate(xs):
        D.text(x, 9.2, labels[i], fs=10)
        D.arrow([(x, 8.9), (x, 8.45)])
        D.cbox(x, 8.0, 1.4, 0.85, "E_K")
    # J0 output goes down to tag
    for i, x in enumerate(xs[1:], start=1):
        D.arrow([(x, 7.57), (x, 6.62)])
        D.xor(x, 6.4)
        D.text(x - 1.1, 6.4, f"M{i if i < 3 else 'ℓ'}", fs=11)
        D.arrow([(x - 0.8, 6.4), (x - 0.22, 6.4)])
        D.arrow([(x, 6.18), (x, 5.3)])
        D.text(x + 0.45, 5.6, f"C{i if i < 3 else 'ℓ'}", fs=10.5)
    D.text(10.5, 8.0, "…", fs=14)
    # GHASH chain
    D.box(3.0, 3.7, 11.0, 1.3, "", style="green")
    D.text(8.5, 4.6, "GHASH_L over  A, C1, …, Cℓ, len(A)‖len(C)", fs=11)
    D.text(8.5, 4.05, "(polynomial evaluation in GF(2¹²⁸),  L = E_K(0¹²⁸))", fs=9.5, color=MUTED)
    D.text(2.35, 4.35, "A", fs=12)
    D.arrow([(2.6, 4.35), (3.0, 4.35)])
    for x in xs[1:]:
        D.arrow([(x, 5.3), (x, 5.0)])
    D.arrow([(8.5, 3.7), (8.5, 2.12)])
    D.arrow([(xs[0], 7.57), (xs[0], 1.9), (8.28, 1.9)])
    D.xor(8.5, 1.9)
    D.arrow([(8.5, 1.68), (8.5, 0.8)])
    D.text(8.5, 0.5, "T", fs=12)
    D.text(xs[0] + 0.3, 2.3, "E_K(J0)", fs=10, ha="left", color=MUTED)
    D.save(out("04/gcm"))


@fig("04/gcm-siv")
def gcm_siv():
    D = Diagram(16, 8.2)
    D.text(1.0, 7.6, "N", fs=12)
    D.arrow([(1.0, 7.3), (1.0, 6.85)])
    D.cbox(1.0, 6.4, 1.7, 0.9, "derive keys", style="purple", fs=10)
    D.text(1.0, 5.55, "L, K′", fs=10, color=MUTED)
    # hash
    D.text(4.2, 7.6, "A,  M", fs=12)
    D.arrow([(4.2, 7.3), (4.2, 6.85)])
    D.cbox(4.2, 6.4, 2.2, 0.9, "universal hash_L", style="green", fs=10)
    D.arrow([(4.2, 5.95), (4.2, 5.12)])
    D.xor(4.2, 4.9)
    D.text(2.9, 4.9, "N", fs=11)
    D.arrow([(3.15, 4.9), (3.98, 4.9)])
    D.arrow([(4.2, 4.68), (4.2, 4.0)])
    D.cbox(4.2, 3.55, 1.6, 0.9, "E_K′")
    D.arrow([(4.2, 3.1), (4.2, 1.2)])
    D.text(4.2, 0.85, "T  (tag = synthetic IV)", fs=11)
    # CTR with T
    D.arrow([(4.2, 2.3), (7.2, 2.3), (7.2, 3.1)])
    D.text(7.6, 2.0, "T as initial counter", fs=9.5, color=MUTED, ha="left")
    xs = [7.2, 10.2, 13.2]
    for i, x in enumerate(xs):
        D.cbox(x, 3.55, 1.5, 0.9, "E_K′")
        if i:
            D.text(x, 2.6, f"T+{i}", fs=10)
            D.arrow([(x, 2.85), (x, 3.1)])
        D.arrow([(x, 4.0), (x, 4.68)])
        D.xor(x, 4.9)
        D.text(x - 1.0, 4.9, f"M{i + 1}", fs=11)
        D.arrow([(x - 0.7, 4.9), (x - 0.22, 4.9)])
        D.arrow([(x, 5.12), (x, 5.8)])
        D.text(x, 6.1, f"C{i + 1}", fs=11)
    D.text(10.2, 7.5, "pass 2: CTR encryption", fs=10.5, bold=True)
    D.text(4.2, 8.15, "pass 1: tag over everything", fs=10.5, bold=True)
    D.save(out("04/gcm-siv"))


# ---------------------------------------------------------------- Module 5
@fig("05/thetacb")
def thetacb():
    D = Diagram(17, 6.8)
    xs = [1.6, 4.6, 7.6]
    for i, x in enumerate(xs):
        n = i + 1
        D.text(x, 6.3, f"M{n}", fs=11)
        D.arrow([(x, 6.0), (x, 5.3)])
        D.cbox(x, 4.8, 1.9, 1.0, "", style="blue")
        D.text(x, 4.95, "Ẽ_K", fs=11)
        D.text(x, 4.55, f"(N, {n})", fs=9, color=MUTED)
        D.arrow([(x, 4.3), (x, 3.5)])
        D.text(x, 3.2, f"C{n}", fs=11)
        D.line([(x, 5.75), (x + 0.9, 5.75)], color="#999999", ls="--")
    D.line([(xs[0] + 0.9, 5.75), (10.6, 5.75)], color="#999999", ls="--")
    D.arrow([(10.6, 5.75), (10.6, 5.12)], color="#999999", ls="--")
    D.op(10.6, 4.9, "Σ")
    D.text(10.6, 6.15, "checksum = M1 ⊕ M2 ⊕ M3", fs=9.5, color=MUTED)
    D.arrow([(10.6, 4.66), (10.6, 4.1)])
    D.cbox(10.6, 3.6, 1.9, 1.0, "")
    D.text(10.6, 3.75, "Ẽ_K", fs=11)
    D.text(10.6, 3.35, "(N, tag)", fs=9, color=MUTED)
    D.arrow([(10.6, 3.1), (10.6, 2.12)])
    D.xor(10.6, 1.9)
    D.arrow([(10.6, 1.68), (10.6, 1.0)])
    D.text(10.6, 0.7, "T", fs=12)
    D.cbox(14.5, 3.6, 2.6, 1.0, "", style="green")
    D.text(14.5, 3.75, "hash of A", fs=10.5)
    D.text(14.5, 3.35, "Ẽ_K under (N, A-position)", fs=8.5, color=MUTED)
    D.text(14.5, 4.75, "A", fs=12)
    D.arrow([(14.5, 4.45), (14.5, 4.1)])
    D.arrow([(14.5, 3.1), (14.5, 1.9), (10.82, 1.9)])
    D.text(4.6, 1.6, "every call uses a unique tweak (nonce, position)", fs=10, color=MUTED)
    D.save(out("05/thetacb"))


@fig("05/lrw")
def lrw():
    D = Diagram(15, 6.6)
    # LRW1
    D.text(3.0, 6.2, "LRW1", fs=13, bold=True)
    D.text(3.0, 5.5, "M", fs=12)
    D.arrow([(3.0, 5.2), (3.0, 4.75)])
    D.cbox(3.0, 4.35, 1.3, 0.8, "E_K")
    D.arrow([(3.0, 3.95), (3.0, 3.42)])
    D.xor(3.0, 3.2)
    D.text(1.3, 3.2, "T", fs=12)
    D.arrow([(1.6, 3.2), (2.78, 3.2)])
    D.arrow([(3.0, 2.98), (3.0, 2.45)])
    D.cbox(3.0, 2.05, 1.3, 0.8, "E_K")
    D.arrow([(3.0, 1.65), (3.0, 1.0)])
    D.text(3.0, 0.7, "C", fs=12)
    # LRW2
    D.text(10.5, 6.2, "LRW2", fs=13, bold=True)
    D.text(10.5, 5.6, "M", fs=12)
    D.arrow([(10.5, 5.3), (10.5, 4.92)])
    D.xor(10.5, 4.7)
    D.arrow([(10.5, 4.48), (10.5, 3.95)])
    D.cbox(10.5, 3.55, 1.3, 0.8, "E_K")
    D.arrow([(10.5, 3.15), (10.5, 2.62)])
    D.xor(10.5, 2.4)
    D.arrow([(10.5, 2.18), (10.5, 1.0)])
    D.text(10.5, 0.7, "C", fs=12)
    D.text(7.2, 3.55, "T", fs=12)
    D.arrow([(7.45, 3.55), (7.9, 3.55)])
    D.cbox(8.45, 3.55, 1.1, 0.8, "h", style="green")
    D.arrow([(8.45, 3.95), (8.45, 4.7), (10.28, 4.7)])
    D.arrow([(8.45, 3.15), (8.45, 2.4), (10.28, 2.4)])
    D.text(12.7, 3.55, "h(T) = L ⊗ T\nblinds input\nand output", fs=9.5, color=MUTED)
    D.save(out("05/lrw"))


@fig("05/xts")
def xts():
    D = Diagram(16, 7)
    D.text(1.4, 6.6, "sector i", fs=11)
    D.arrow([(1.4, 6.3), (1.4, 5.85)])
    D.cbox(1.4, 5.4, 1.4, 0.85, "E_K2")
    D.arrow([(1.4, 4.97), (1.4, 4.2)])
    D.text(1.4, 3.9, "Δ = E_K2(i) ⊗ 2ʲ", fs=10, color=MUTED)
    xs = [5.0, 8.6, 12.2]
    for k, x in enumerate(xs):
        j = ["0", "1", "31"][k]
        D.text(x, 6.6, f"M(i,{j})", fs=11)
        D.arrow([(x, 6.3), (x, 5.92)])
        D.xor(x, 5.7)
        D.arrow([(x, 5.48), (x, 4.95)])
        D.cbox(x, 4.5, 1.4, 0.85, "E_K1")
        D.arrow([(x, 4.07), (x, 3.52)])
        D.xor(x, 3.3)
        D.arrow([(x, 3.08), (x, 2.4)])
        D.text(x, 2.1, f"C(i,{j})", fs=11)
        D.line([(x - 1.0, 5.7), (x - 1.0, 3.3)], color="#3B6FD8")
        D.arrow([(x - 1.0, 5.7), (x - 0.22, 5.7)], color="#3B6FD8")
        D.arrow([(x - 1.0, 3.3), (x - 0.22, 3.3)], color="#3B6FD8")
        D.text(x - 1.25, 4.5, f"Δ·2^{j}" if j != "0" else "Δ", fs=9.5, color="#3B6FD8", ha="right")
    D.text(10.4, 4.5, "…", fs=14)
    D.text(8.6, 1.0, "one 512-byte sector = 32 AES blocks;  "
           "a partial last block uses ciphertext stealing", fs=10, color=MUTED)
    D.save(out("05/xts"))



# ---------------------------------------------------------------- sponge helper
def chain(D, x0, yo, yi, items, init=None, lanes_label=True, pw=0.8):
    """Draw a sponge/duplex-like chain.

    yo / yi: y of outer and inner lane.  items: list of tuples
      ("P", label, style)            permutation box
      ("in", label, where)           XOR input; where in {"o", "i", "oi"}
      ("out", label)                 output arrow from outer lane
      ("gap", dx)                    horizontal space
      ("sep", label_left, label_right)  dashed separator
      ("dots",)
    """
    x = x0
    top, bot = yo + 0.75, yi - 0.75
    if init is not None:
        D.box(x, bot + 0.15, 0.75, top - bot - 0.3, "", style="grey", rounded=False)
        D.line([(x, (yo + yi) / 2), (x + 0.75, (yo + yi) / 2)], color="#999999", ls="--")
        D.text(x + 0.375, yo, init[0], fs=9.5)
        D.text(x + 0.375, yi, init[1], fs=9.5)
        if lanes_label:
            D.text(x + 1.05, yo + 0.22, "r", fs=9, color=MUTED, italic=True)
            D.text(x + 1.05, yi + 0.22, "c", fs=9, color=MUTED, italic=True)
        x += 0.75
    xstart = x
    for it in items:
        k = it[0]
        if k == "P":
            x += 0.45
            D.box(x, bot, pw, top - bot, it[1], style=it[2] if len(it) > 2 else "blue", fs=11)
            x += pw
        elif k == "in":
            x += 0.55
            lab, where = it[1], it[2]
            if "o" in where:
                D.xor(x, yo)
            if "i" in where:
                D.xor(x, yi)
            if where == "i":
                D.text(x, yi - 0.95, lab, fs=10)
                D.arrow([(x, yi - 0.7), (x, yi - 0.22)])
            else:
                D.text(x, yo + 1.35, lab, fs=10)
                D.arrow([(x, yo + 1.1), (x, yo + 0.22)])
                if where == "oi":
                    D.line([(x, yo + 0.85), (x - 0.35, yo + 0.85), (x - 0.35, yi)], color="#999999")
                    D.arrow([(x - 0.35, yi), (x - 0.22, yi)], color="#999999")
        elif k == "out":
            x += 0.5
            D.line([(x, yo), (x, yo)])
            D.arrow([(x, yo), (x, yo + 1.1)])
            D.text(x, yo + 1.35, it[1], fs=10)
        elif k == "gap":
            x += it[1]
        elif k == "dots":
            x += 0.4
            D.text(x, (yo + yi) / 2, "…", fs=14, z=6)
            x += 0.4
        elif k == "sep":
            x += 0.35
            D.line([(x, bot - 0.2), (x, top + 1.25)], color="#AAAAAA", ls="--")
            D.text(x - 0.15, bot - 0.5, it[1], fs=9, color=MUTED, ha="right")
            D.text(x + 0.15, bot - 0.5, it[2], fs=9, color=MUTED, ha="left")
            x += 0.15
    x += 0.4
    D.line([(xstart, yo), (x, yo)])
    D.line([(xstart, yi), (x, yi)])
    return x


@fig("06/sponge")
def sponge():
    D = Diagram(15, 6.4)
    chain(D, 0.3, 3.9, 2.0, [
        ("in", "M1", "o"), ("P", "P"), ("in", "M2", "o"), ("P", "P"), ("in", "M3", "o"), ("P", "P"),
        ("sep", "absorbing", "squeezing"),
        ("out", "Z1"), ("P", "P"), ("out", "Z2"), ("P", "P"), ("out", "Z3"),
    ], init=("0", "0"))
    D.text(7.5, 0.25, "outer part: r bits (rate)    ·    inner part: c bits (capacity), never output",
           fs=9.5, color=MUTED)
    D.save(out("06/sponge"))


@fig("06/merkle-damgard")
def merkle_damgard():
    D = Diagram(15, 4.6)
    y = 2.0
    D.text(0.6, y, "IV", fs=12)
    xs = [2.6, 5.6, 8.6, 11.6]
    labels = ["M1", "M2", "…", "Mℓ ‖ length"]
    prev = 0.95
    for i, x in enumerate(xs):
        D.arrow([(prev, y), (x - 0.6, y)])
        D.cbox(x, y, 1.2, 1.1, "F", style="blue", fs=12)
        D.text(x, 4.1, labels[i], fs=11)
        D.arrow([(x, 3.8), (x, 2.55)])
        if i < 3:
            D.text((x + 0.6 + xs[i + 1] - 0.6) / 2, y + 0.3, f"h{i + 1}" if i < 2 else "", fs=10, color=MUTED)
        prev = x + 0.6
    D.arrow([(prev, y), (13.6, y)])
    D.text(14.2, y, "H(M)", fs=12)
    D.text(7.0, 0.5, "the output is the last chaining value, so anyone can continue the chain: "
           "length extension", fs=9.5, color=MUTED)
    D.save(out("06/merkle-damgard"))


@fig("06/indifferentiability")
def indiff():
    D = Diagram(14, 6.4)
    D.text(3.4, 6.0, "Real world", fs=12.5, bold=True)
    D.text(10.6, 6.0, "Ideal world", fs=12.5, bold=True)
    D.cbox(2.2, 4.6, 2.0, 0.9, "$H^{P}$", style="blue")
    D.text(2.2, 4.6, "", fs=1)
    D.cbox(4.8, 4.6, 1.6, 0.9, "P", style="blue")
    D.arrow([(4.0, 4.6), (3.2, 4.6)])
    D.cbox(9.4, 4.6, 1.6, 0.9, "RO", style="green")
    D.cbox(12.0, 4.6, 2.0, 0.9, "$S^{RO}$", style="orange")
    D.arrow([(11.0, 4.6), (10.2, 4.6)])
    D.cbox(7.0, 1.4, 3.6, 0.95, "distinguisher D", style="purple")
    for x in (2.2, 4.8, 9.4, 12.0):
        D.arrow([(7.0 + (x - 7.0) * 0.25, 1.88), (x, 4.15)], both=True, color="#777777")
    D.text(2.2, 3.7, "construction", fs=9, color=MUTED)
    D.text(4.8, 3.7, "primitive", fs=9, color=MUTED)
    D.text(9.4, 3.7, "random oracle", fs=9, color=MUTED)
    D.text(12.0, 3.7, "simulator", fs=9, color=MUTED)
    D.line([(7.0, 2.6), (7.0, 6.2)], color="#AAAAAA", ls="--")
    D.save(out("06/indifferentiability"))


# ---------------------------------------------------------------- Module 7
@fig("07/hmac")
def hmac():
    D = Diagram(13, 5.4)
    D.cbox(1.5, 4.3, 2.2, 0.8, "K ⊕ ipad", style="orange", fs=10)
    D.text(3.15, 4.3, "‖ M", fs=11, ha="left")
    D.arrow([(2.3, 3.9), (2.3, 3.3)])
    D.cbox(2.3, 2.85, 1.3, 0.9, "H", style="blue", fs=12)
    D.arrow([(2.95, 2.85), (7.95, 2.85)])
    D.text(4.9, 3.15, "inner hash value", fs=9, color=MUTED)
    D.text(8.0, 5.0, "prepended to the inner hash value", fs=9, color=MUTED)
    D.cbox(8.0, 4.3, 2.2, 0.8, "K ⊕ opad", style="orange", fs=10)
    D.arrow([(8.0, 3.9), (8.0, 3.3)])
    D.cbox(8.6, 2.85, 1.3, 0.9, "H", style="blue", fs=12)
    D.arrow([(9.25, 2.85), (11.0, 2.85)])
    D.text(11.9, 2.85, "HMAC(K, M)", fs=11)
    D.text(6.5, 1.0, "the outer hash hides the inner chaining value, so length extension fails", fs=9.5,
           color=MUTED)
    D.save(out("07/hmac"))


@fig("07/hkdf")
def hkdf():
    D = Diagram(16, 6.4)
    D.text(1.3, 5.6, "salt,  IKM", fs=11)
    D.arrow([(1.3, 5.3), (1.3, 4.65)])
    D.cbox(1.3, 4.2, 1.8, 0.9, "HMAC", style="green")
    D.text(1.3, 3.2, "Extract", fs=10, bold=True)
    D.arrow([(2.2, 4.2), (3.4, 4.2)])
    D.text(2.8, 4.5, "PRK", fs=9.5, color=MUTED)
    xs = [5.0, 8.6, 12.2]
    prev = None
    for i, x in enumerate(xs):
        n = i + 1
        D.cbox(x, 4.2, 1.8, 0.9, "HMAC_PRK", style="blue", fs=10)
        D.text(x, 5.6, f"info ‖ {n}", fs=10)
        D.arrow([(x, 5.3), (x, 4.65)])
        if i == 0:
            D.arrow([(3.4, 4.2), (4.1, 4.2)])
        else:
            D.arrow([(xs[i - 1], 3.75), (xs[i - 1], 3.2), (x - 1.25, 3.2), (x - 1.25, 4.2), (x - 0.9, 4.2)])
        D.arrow([(x, 3.75), (x, 1.6)])
        D.text(x, 1.3, f"T{n}", fs=11)
    D.text(8.6, 6.15, "Expand", fs=10, bold=True)
    D.text(8.6, 0.5, "OKM = T1 ‖ T2 ‖ T3 ‖ …   (each block feeds into the next)", fs=10, color=MUTED)
    D.save(out("07/hkdf"))


@fig("07/pbkdf2")
def pbkdf2():
    D = Diagram(16, 6.0)
    D.text(1.2, 5.4, "S ‖ i", fs=11)
    xs = [1.2, 4.2, 7.2, 11.2]
    for k, x in enumerate(xs):
        D.cbox(x, 4.0, 1.7, 0.9, "PRF_P", style="blue", fs=10)
        if k == 0:
            D.arrow([(x, 5.1), (x, 4.45)])
        elif k < 3:
            D.arrow([(xs[k - 1] + 0.85, 4.0), (x - 0.85, 4.0)])
        if k == 3:
            D.arrow([(9.7, 4.0), (x - 0.85, 4.0)])
        lab = ["U1", "U2", "U3", "Uc"][k]
        D.text(x + 0.35, 3.2, lab, fs=10, color=MUTED)
        D.arrow([(x, 3.55), (x, 2.12)])
        D.xor(x, 1.9)
    D.text(9.2, 4.0, "…", fs=14)
    D.line([(xs[0] + 0.22, 1.9), (xs[1] - 0.22, 1.9)])
    D.line([(xs[1] + 0.22, 1.9), (xs[2] - 0.22, 1.9)])
    D.line([(xs[2] + 0.22, 1.9), (xs[3] - 0.22, 1.9)])
    D.arrow([(xs[3] + 0.22, 1.9), (13.4, 1.9)])
    D.text(14.4, 1.9, "T_i", fs=12)
    D.text(7.2, 0.6, "c sequential PRF calls per output block, all XORed together;  "
           "P = password, S = salt", fs=9.5, color=MUTED)
    D.save(out("07/pbkdf2"))


@fig("07/disk-encryption")
def disk():
    D = Diagram(15, 4.6)
    D.cbox(1.8, 2.0, 2.6, 1.2, "PRNG\n(e.g. interrupts)", style="grey", fs=10)
    D.arrow([(3.1, 2.0), (5.3, 2.0)])
    D.text(4.2, 2.3, "salt", fs=10)
    D.text(4.2, 1.7, "512 bits", fs=8.5, color=MUTED)
    D.cbox(6.4, 2.0, 2.2, 1.2, "KDF\nPBKDF2", style="orange", fs=10.5)
    D.text(6.4, 4.0, "password", fs=11)
    D.arrow([(6.4, 3.7), (6.4, 2.6)])
    D.arrow([(7.5, 2.0), (9.7, 2.0)])
    D.text(8.6, 2.3, "key", fs=10)
    D.cbox(10.9, 2.0, 2.4, 1.2, "encryption\nXTS-AES", style="blue", fs=10.5)
    D.text(10.9, 4.0, "disk", fs=11)
    D.arrow([(10.9, 3.7), (10.9, 2.6)])
    D.arrow([(12.1, 2.0), (13.2, 2.0)])
    D.text(14.1, 2.0, "encrypted\ndisk", fs=10.5)
    D.save(out("07/disk-encryption"))


# ---------------------------------------------------------------- Module 8
@fig("08/keyed-sponges")
def keyed_sponges():
    D = Diagram(16, 16)
    panels = [
        ("Outer-keyed sponge (OKS):  key absorbed through the outer part", ("0", "0"),
         [("in", "K", "o"), ("P", "P"), ("in", "M1", "o"), ("P", "P"), ("in", "M2", "o"), ("P", "P"),
          ("sep", "", ""), ("out", "Z1"), ("P", "P"), ("out", "Z2")]),
        ("Inner-keyed sponge (IKS):  key in the inner part of the initial state", ("0", "K"),
         [("in", "M1", "o"), ("P", "P"), ("in", "M2", "o"), ("P", "P"), ("in", "M3", "o"), ("P", "P"),
          ("sep", "", ""), ("out", "Z1"), ("P", "P"), ("out", "Z2")]),
        ("Full-keyed sponge (FKS):  key in the inner part, message absorbed into the full state",
         ("0", "K"),
         [("in", "M1", "oi"), ("P", "P"), ("in", "M2", "oi"), ("P", "P"), ("in", "M3", "oi"), ("P", "P"),
          ("sep", "", ""), ("out", "Z1"), ("P", "P"), ("out", "Z2")]),
    ]
    for i, (title, init, items) in enumerate(panels):
        oy = 10.9 - i * 5.1
        D.text(0.3, oy + 4.3, title, fs=11.5, bold=True, ha="left")
        chain(D, 0.4, oy + 2.1, oy + 0.5, items, init=init)
    D.save(out("08/keyed-sponges"))


@fig("08/duplex")
def duplex():
    D = Diagram(14, 5.4)
    chain(D, 0.3, 3.0, 1.2, [
        ("in", "K‖M1", "o"), ("P", "P"), ("out", "Z1"), ("in", "M2", "o"), ("P", "P"), ("out", "Z2"),
        ("in", "M3", "o"), ("P", "P"), ("out", "Z3"), ("dots",)], init=("0", "0"))
    D.text(7.0, 0.0, "each duplex call: absorb one padded block (≤ r − 1 bits), apply P, squeeze ≤ r bits",
           fs=9.5, color=MUTED)
    D.save(out("08/duplex"))


@fig("08/spongewrap")
def spongewrap():
    D = Diagram(18, 6.2)
    yo, yi = 3.3, 1.5
    chain(D, 0.3, yo, yi, [
        ("P", "P"), ("in", "A1", "o"), ("in", "0", "i"), ("P", "P"), ("dots",),
        ("in", "M1", "o"), ("in", "1", "i"), ("P", "P"), ("out", "C1"), ("in", "M2", "o"), ("in", "1", "i"),
        ("P", "P"), ("out", "C2"), ("in", "pad", "o"), ("in", "0", "i"), ("P", "P"), ("out", "T"),
    ], init=("K,N", ""))
    D.text(9.0, 0.0, "Ci = Mi ⊕ (outer bits), then Mi is absorbed;  "
           "inner bits 0 / 1 are the domain separation bits", fs=9.5, color=MUTED)
    D.save(out("08/spongewrap"))


@fig("08/ascon")
def ascon():
    D = Diagram(19, 6.6)
    yo, yi = 3.4, 1.6
    chain(D, 0.3, yo, yi, [
        ("P", "pᵃ", "purple"), ("in", "0*‖K", "i"), ("gap", 0.2), ("in", "A1", "o"), ("P", "pᵇ"),
        ("in", "0*‖1", "i"), ("gap", 0.2),
        ("in", "P1", "o"), ("out", "C1"), ("P", "pᵇ"), ("in", "P2", "o"), ("out", "C2"),
        ("in", "K‖0*", "i"), ("P", "pᵃ", "purple"), ("in", "0*‖K", "i"), ("gap", 0.3), ("out", "T"),
    ], init=("IV", "K‖N"), lanes_label=False)
    D.text(6.6, 0.0, "pᵃ: 12 rounds (strong, keyed edges)    pᵇ: 6 rounds (fast, data)    "
           "key blinding: K XORed in four times", fs=9.5, color=MUTED)
    D.text(1.9, 5.9, "initialisation", fs=9.5, color=MUTED)
    D.text(4.4, 5.9, "associated data", fs=9.5, color=MUTED)
    D.text(7.3, 5.9, "plaintext", fs=9.5, color=MUTED)
    D.text(11.2, 5.9, "finalisation", fs=9.5, color=MUTED)
    D.save(out("08/ascon"))


@fig("08/suks")
def suks():
    D = Diagram(15, 5.6)
    yo, yi = 3.2, 1.4
    chain(D, 0.3, yo, yi, [
        ("in", "M1", "o"), ("P", "P"), ("in", "M2", "o"), ("P", "P"), ("in", "M3", "o"), ("P", "P"),
        ("gap", 0.3), ("P", "G", "orange"), ("P", "P"), ("out", "T"),
    ], init=("0", "0"))
    D.text(7.6, 5.2, "K", fs=12)
    D.arrow([(7.6, 4.9), (7.6, 3.95)])
    D.text(3.6, 0.0, "unkeyed absorption: nothing secret to leak", fs=9.5, color=MUTED)
    D.text(8.6, 0.0, "key added once, at the end", fs=9.5, color=MUTED)
    D.save(out("08/suks"))



# ---------------------------------------------------------------- sequence helper
def seq(D, actors, top, bottom, msgs, notes=()):
    """actors: {name: (x, style)}; msgs: (from, to, y, label); notes: (x, y, text, ha)."""
    for name, (x, st) in actors.items():
        D.cbox(x, top, 2.6, 0.75, name, style=st, fs=11, bold=True)
        D.line([(x, top - 0.4), (x, bottom)], color="#AAAAAA", ls="--")
    for a, b, y, lab in msgs:
        xa, xb = actors[a][0], actors[b][0]
        D.arrow([(xa, y), (xb, y)])
        D.text((xa + xb) / 2, y + 0.28, lab, fs=10)
    for x, y, t, ha in notes:
        D.text(x, y, t, fs=9.5, color=MUTED, ha=ha, bg=True)


# ---------------------------------------------------------------- Module 9
@fig("09/reduction")
def reduction():
    D = Diagram(14, 6.6)
    D.box(3.0, 0.8, 8.0, 4.8, "", style="green")
    D.text(7.0, 5.2, "reduction / simulator B", fs=11.5, bold=True)
    D.cbox(8.6, 3.0, 2.6, 1.6, "adversary A\n(breaks the\nscheme)", style="purple", fs=10)
    D.cbox(4.8, 3.0, 2.6, 1.6, "simulated\nscheme with\ninstance embedded", style="white", fs=9.5)
    D.arrow([(6.1, 3.35), (7.3, 3.35)])
    D.arrow([(7.3, 2.65), (6.1, 2.65)])
    D.text(6.7, 3.65, "answers", fs=8.5, color=MUTED)
    D.text(6.7, 2.35, "queries", fs=8.5, color=MUTED)
    D.text(1.2, 3.0, "problem\ninstance", fs=10.5)
    D.arrow([(2.0, 3.0), (3.5, 3.0)])
    D.arrow([(9.9, 3.0), (11.0, 3.0), (11.9, 3.0)])
    D.text(12.9, 3.0, "solution", fs=10.5)
    D.text(7.0, 0.2, "A breaks the scheme in (t, ε)   ⇒   B solves the problem in (t + T, ε / L)",
           fs=10, color=MUTED)
    D.save(out("09/reduction"))


@fig("09/ind-cpa")
def ind_cpa():
    D = Diagram(13, 7.0)
    seq(D, {"Challenger": (2.5, "green"), "Adversary A": (10.5, "purple")}, 6.4, 0.6, [
        ("Challenger", "Adversary A", 5.2, "pk"),
        ("Adversary A", "Challenger", 4.0, "M0, M1  (equal length)"),
        ("Challenger", "Adversary A", 2.8, "C* = Enc(pk, M_b)"),
    ], notes=[(2.3, 1.8, "(pk, sk) ← KGen\nb ← {0, 1} at random", "center"),
              (10.5, 1.5, "outputs a guess b′\nwins if b′ = b", "center")])
    D.save(out("09/ind-cpa"))


# ---------------------------------------------------------------- Module 10
@fig("10/kem")
def kem():
    D = Diagram(13, 6.0)
    seq(D, {"Sender": (2.5, "blue"), "Receiver": (10.5, "green")}, 5.4, 0.6, [
        ("Receiver", "Sender", 4.2, "pk"),
        ("Sender", "Receiver", 2.5, "C"),
    ], notes=[(2.5, 3.2, "(K, C) ← Encaps(pk)", "center"),
              (10.5, 5.0 - 1.6, "(pk, sk) ← KGen", "center"),
              (10.5, 1.7, "K ← Decaps(sk, C)", "center"),
              (6.5, 0.5, "both now hold the same symmetric key K; data is then protected with AE", "center")])
    D.save(out("10/kem"))


@fig("10/fo-kem")
def fo_kem():
    D = Diagram(16, 9.2)
    D.text(4.0, 8.8, "Encaps(pk)", fs=12, bold=True)
    D.cbox(1.6, 7.6, 2.2, 0.8, "random X", style="grey", fs=10)
    D.arrow([(2.7, 7.6), (3.6, 7.6)])
    D.cbox(4.3, 7.6, 1.3, 0.8, "G", style="orange")
    D.arrow([(4.95, 7.6), (5.9, 7.6)])
    D.text(5.4, 7.9, "R", fs=10)
    D.cbox(7.0, 7.6, 2.1, 0.8, "Enc(pk, X; R)", style="blue", fs=9.5)
    D.arrow([(1.6, 7.2), (1.6, 6.6), (7.0, 6.6), (7.0, 7.2)])
    D.arrow([(8.05, 7.6), (9.2, 7.6)])
    D.text(9.5, 7.6, "C", fs=12)
    D.arrow([(1.6, 6.6), (1.6, 5.75)])
    D.cbox(1.6, 5.35, 1.4, 0.8, "KDF", style="orange")
    D.arrow([(2.3, 5.35), (3.2, 5.35)])
    D.text(3.5, 5.35, "K", fs=12)

    D.text(4.0, 4.1, "Decaps(sk, C)", fs=12, bold=True)
    D.text(0.6, 2.9, "C", fs=12)
    D.arrow([(0.85, 2.9), (1.5, 2.9)])
    D.cbox(2.5, 2.9, 2.0, 0.8, "Dec(sk, ·)", style="green", fs=10)
    D.arrow([(3.5, 2.9), (4.4, 2.9)])
    D.text(3.95, 3.2, "X′", fs=10)
    D.cbox(5.0, 2.9, 1.2, 0.8, "G", style="orange")
    D.arrow([(5.6, 2.9), (6.5, 2.9)])
    D.text(6.05, 3.2, "R′", fs=10)
    D.cbox(7.8, 2.9, 2.6, 0.8, "Enc(pk, X′; R′)", style="blue", fs=9.5)
    D.arrow([(9.1, 2.9), (10.1, 2.9)])
    D.cbox(11.1, 2.9, 2.0, 0.8, "= C ?", style="white", fs=10.5)
    D.arrow([(11.1, 3.3), (11.1, 4.0)])
    D.text(11.1, 4.3, "no: reject (⊥ or H(z, C))", fs=9.5, color="#C0392B")
    D.arrow([(12.1, 2.9), (13.0, 2.9)])
    D.text(12.55, 3.2, "yes", fs=9, color="#2E8B57")
    D.cbox(14.1, 2.9, 2.0, 0.8, "K = KDF(X′)", style="orange", fs=9.5)
    D.text(8.0, 1.2, "re-encryption check: only ciphertexts produced honestly from some X′ are accepted",
           fs=9.5, color=MUTED)
    D.save(out("10/fo-kem"))


# ---------------------------------------------------------------- Module 11
@fig("11/rsa-pss")
def rsa_pss():
    D = Diagram(15, 7.0)
    D.text(1.4, 6.5, "salt", fs=11)
    D.text(3.0, 6.5, "M", fs=11)
    D.arrow([(1.4, 6.2), (2.0, 5.55)])
    D.arrow([(3.0, 6.2), (2.5, 5.55)])
    D.cbox(2.25, 5.1, 1.3, 0.85, "H", style="blue", fs=12)
    D.arrow([(2.25, 4.67), (2.25, 2.1)])
    D.text(2.55, 3.9, "w", fs=11)
    D.arrow([(2.25, 3.6), (5.4, 3.6)])
    D.cbox(6.1, 3.6, 1.3, 0.85, "G", style="orange", fs=12)
    D.arrow([(6.75, 3.6), (8.7, 3.6)])
    D.xor(8.9, 3.6)
    D.text(8.9, 5.0, "salt ‖ 00…0", fs=10)
    D.arrow([(8.9, 4.7), (8.9, 3.82)])
    D.arrow([(8.9, 3.38), (8.9, 2.1)])
    y = 1.1
    D.box(0.4, y, 0.9, 0.9, "0", style="grey", rounded=False)
    D.box(1.3, y, 1.9, 0.9, "w", style="blue", rounded=False)
    D.box(3.2, y, 11.0, 0.9, "G(w) ⊕ (salt ‖ 00…0)", style="orange", rounded=False)
    D.text(7.3, 0.4, "μ(M) = 0 ‖ w ‖ masked salt;   signature σ = μ(M)ᵈ mod N", fs=10, color=MUTED)
    D.save(out("11/rsa-pss"))


# ---------------------------------------------------------------- Module 13
@fig("13/lamport")
def lamport():
    D = Diagram(15, 6.6)
    m = "011"
    D.text(0.9, 4.6, "sk", fs=12, bold=True)
    D.text(0.9, 1.6, "pk", fs=12, bold=True)
    for i in range(3):
        for b in range(2):
            x = 2.2 + i * 2.6
            sel = int(m[i]) == b
            D.cbox(x, 5.1 - b * 1.0, 1.9, 0.75, f"x({i + 1},{b})", style="orange" if sel else "white", fs=10)
            D.cbox(x, 2.1 - b * 1.0, 1.9, 0.75, f"y({i + 1},{b})", style="green" if sel else "white", fs=10)
        D.arrow([(2.2 + i * 2.6, 3.95), (2.2 + i * 2.6, 2.55)], color="#999999")
        D.text(2.55 + i * 2.6, 3.25, "H", fs=10, color=MUTED)
        D.text(2.2 + i * 2.6, 6.1, f"m{i + 1} = {m[i]}", fs=11)
    D.text(11.6, 4.6, "signature on m = 011:\n(x(1,0), x(2,1), x(3,1))", fs=10.5)
    D.text(11.6, 1.6, "verify: H(σi) = y(i, mi)\nfor every i", fs=10.5)
    D.text(7.0, 0.1, "each signature reveals one of the two secrets per position, so a key may sign only once",
           fs=9.5, color=MUTED)
    D.save(out("13/lamport"))


@fig("13/merkle-tree")
def merkle_tree():
    D = Diagram(16, 7.4)
    leaves = [1.2 + i * 1.95 for i in range(8)]
    i_sel = 2
    path = {(0, 2), (1, 1), (2, 0), (3, 0)}
    auth = {(0, 3), (1, 0), (2, 1)}
    levels = [leaves]
    for _ in range(3):
        prev = levels[-1]
        levels.append([(prev[2 * k] + prev[2 * k + 1]) / 2 for k in range(len(prev) // 2)])
    ys = [2.0, 3.6, 5.0, 6.4]
    for lv, xs in enumerate(levels):
        for k, x in enumerate(xs):
            st = "orange" if (lv, k) in path else "green" if (lv, k) in auth else "white"
            lab = "root = pk" if lv == 3 else ("H(Y%d)" % k if lv == 0 else "")
            D.cbox(x, ys[lv], 1.6 if lv < 3 else 2.2, 0.7, lab, style=st, fs=9.5)
            if lv > 0:
                for c in (2 * k, 2 * k + 1):
                    D.line([(x, ys[lv] - 0.35), (levels[lv - 1][c], ys[lv - 1] + 0.35)], color="#999999")
    for k, x in enumerate(leaves):
        D.line([(x, 1.65), (x, 1.15)], color="#999999")
        D.text(x, 0.85, f"OTS {k}", fs=9, color=MUTED)
    D.text(15.0, 6.4, "■ path from leaf 2", fs=9.5, color="#D9822B", ha="right")
    D.text(15.0, 5.9, "■ authentication path", fs=9.5, color="#2E8B57", ha="right")
    D.text(8.0, 0.2, "signing with leaf 2 sends the green siblings, so the verifier can recompute the root",
           fs=9.5, color=MUTED)
    D.save(out("13/merkle-tree"))


@fig("13/wots")
def wots():
    D = Diagram(15, 8.8)
    chains = [("chunk 1 = 13", 13), ("chunk 2 = 2", 2), ("chunk 64 = 7", 7), ("checksum", 9)]
    xs = [1.8, 5.0, 9.0, 12.6]
    rows = [(0, "x"), (1, "H(x)"), (2, "H²(x)"), (None, "⋮"), (14, "H¹⁴(x)"), (15, "H¹⁵(x) = y")]
    ys = [1.0, 2.2, 3.4, 4.45, 5.5, 6.7]
    for (lab, v), x in zip(chains, xs):
        for (h, t), y in zip(rows, ys):
            if h is None:
                D.text(x, y, "⋮", fs=12, color=MUTED)
                continue
            st = "green" if h == 15 else "grey"
            D.cbox(x, y, 2.4, 0.7, t, style=st, fs=9.5)
        for y0, y1 in zip(ys[:-1], ys[1:]):
            D.arrow([(x, y0 + 0.36), (x, y1 - 0.36)], color="#999999")
        D.text(x, 7.9, lab, fs=10.5, bold=True)
        sup = str(v).translate(str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹"))
        D.text(x, 7.45, f"signature value σ = H{sup}(x)", fs=9, color="#D9822B")
    D.text(7.0, 4.45, "…", fs=14)
    D.text(7.5, 0.1, "signing walks each chain up to the chunk value; verifying walks the rest of the way to y. "
           "The checksum chains stop forging by walking forward.", fs=9.0, color=MUTED)
    D.save(out("13/wots"))


# ---------------------------------------------------------------- Module 14
@fig("14/mitm")
def mitm():
    D = Diagram(16, 6.4)
    seq(D, {"Alice": (2.2, "blue"), "Eve": (8.0, "red"), "Bob": (13.8, "green")}, 5.8, 0.6, [
        ("Alice", "Eve", 4.6, "A = gᵃ"),
        ("Eve", "Bob", 4.6, "E = gᵉ"),
        ("Bob", "Eve", 3.4, "B = gᵇ"),
        ("Eve", "Alice", 3.4, "E′ = gᵉ′"),
    ], notes=[(2.2, 1.8, "K = gᵃᵉ′\nthinks it is shared with Bob", "center"),
              (8.0, 1.8, "knows gᵃᵉ′ and gᵇᵉ:\nreads and modifies everything", "center"),
              (13.8, 1.8, "K = gᵇᵉ\nthinks it is shared with Alice", "center")])
    D.save(out("14/mitm"))


@fig("14/tls12")
def tls12():
    D = Diagram(15, 9.6)
    seq(D, {"Client": (2.5, "blue"), "Server": (12.5, "green")}, 9.0, 0.4, [
        ("Client", "Server", 7.9, "ClientHello: r_C, supported ciphersuites"),
        ("Server", "Client", 6.7, "ServerHello: r_S, chosen suite;  Certificate"),
        ("Server", "Client", 5.7, "ServerKeyExchange: B,  Sign_skS(r_C, r_S, B)"),
        ("Client", "Server", 4.5, "ClientKeyExchange: A"),
        ("Client", "Server", 3.3, "Finished: MAC over the whole transcript"),
        ("Server", "Client", 2.1, "Finished: MAC over the whole transcript"),
        ("Client", "Server", 1.0, "encrypted application data"),
    ])
    D.text(0.3, 6.2, "negotiation\n+ key exchange", fs=9, color=MUTED, ha="left")
    D.text(0.3, 2.7, "authentication", fs=9, color=MUTED, ha="left")
    D.save(out("14/tls12"))


# ---------------------------------------------------------------- Module 15
@fig("15/hierarchy")
def hierarchy():
    D = Diagram(17, 6.4)
    D.text(3.2, 6.0, "2-layer", fs=12, bold=True)
    D.cbox(3.2, 4.8, 2.2, 0.8, "(M)KEK", style="purple")
    for x in (1.0, 3.2, 5.4):
        D.cbox(x, 1.6, 1.4, 0.7, "KD", style="green")
        D.arrow([(3.2, 4.4), (x, 1.95)], color="#777777")
    D.text(10.0, 6.0, "3-layer", fs=12, bold=True)
    D.cbox(10.0, 5.0, 2.0, 0.8, "MKEK", style="purple")
    for kx, kids in ((8.6, (7.6, 9.6)), (11.4, (11.4,))):
        D.cbox(kx, 3.3, 1.6, 0.75, "KEK", style="orange")
        D.arrow([(10.0, 4.6), (kx, 3.68)], color="#777777")
        for x in kids:
            D.cbox(x, 1.6, 1.4, 0.7, "KD", style="green")
            D.arrow([(kx, 2.92), (x, 1.95)], color="#777777")
    D.text(13.3, 5.0, "master KEK: manual distribution,\nencrypts KEKs", fs=9.5, ha="left")
    D.text(13.3, 3.3, "KEK: automated distribution,\nencrypts data keys", fs=9.5, ha="left")
    D.text(13.3, 1.6, "data key: automated,\nprotects data", fs=9.5, ha="left")
    D.save(out("15/hierarchy"))


@fig("15/shamir")
def shamir():
    import numpy as np
    D = Diagram(12, 6.4)
    ax = D.ax
    xs = np.linspace(0.6, 10.5, 200)
    f = lambda x: 3.6 - 1.05 * (x - 0.6) + 0.13 * (x - 0.6) ** 2  # noqa: E731
    ax.plot(xs, f(xs), color="#3B6FD8", lw=2, zorder=2)
    D.line([(0.6, 0.6), (11.2, 0.6)], color="#999999")
    D.line([(0.6, 0.6), (0.6, 6.0)], color="#999999")
    D.ax.add_patch(__import__("matplotlib.patches", fromlist=["Circle"]).Circle(
        (0.6, f(0.6)), 0.16, color="#C0392B", zorder=4))
    D.text(1.0, f(0.6) + 0.35, "f(0) = K  (secret)", fs=10.5, ha="left", color="#C0392B")
    for i, x in enumerate((2.6, 4.6, 6.6, 8.6, 10.1)):
        D.ax.add_patch(__import__("matplotlib.patches", fromlist=["Circle"]).Circle(
            (x, f(x)), 0.13, color=INK, zorder=4))
        D.text(x, f(x) - 0.45, f"share {i + 1}", fs=9.5)
    D.text(6.0, 0.1, "degree k − 1 polynomial: any k shares determine it, k − 1 reveal nothing about K",
           fs=9.5, color=MUTED)
    D.save(out("15/shamir"))


@fig("15/smartcard")
def smartcard():
    D = Diagram(18.6, 8.6)
    steps = [
        (2.4, 6.6, "1. storage key", "K_ST from master key\ngeneration key;\ncomponents to a safe,\nloaded into HSM", "purple"),
        (6.9, 6.6, "2. transport key", "K_TR as components;\nHSM stores only\nE_KST(K_TR)", "orange"),
        (11.4, 6.6, "3. card keys in HSM", "K_i = E_KM(ID_i);\nexported as\nE_KTR(K_i) on USB", "blue"),
        (15.9, 6.6, "4. personalisation", "secure room: decipher\nwith K_TR, load\n(ID_i, K_i) into card i", "green"),
    ]
    for x, y, t, body, st in steps:
        D.cbox(x, y + 0.85, 4.0, 0.7, t, style=st, fs=10.5, bold=True)
        D.cbox(x, y - 0.75, 4.0, 2.2, body, style="white", fs=9.5)
    for a, b in ((4.4, 4.9), (8.9, 9.4), (13.4, 13.9)):
        D.arrow([(a, 6.6), (b, 6.6)])
    D.cbox(5.5, 1.9, 4.6, 1.6, "card i\ncomputes a cryptogram\nwith K_i", style="green", fs=10)
    D.cbox(13.0, 1.9, 5.2, 1.6, "bank HSM (holds K_M)\nrecomputes K_i = E_KM(ID_i)\nand verifies", style="blue", fs=10)
    D.arrow([(7.8, 1.9), (10.4, 1.9)])
    D.text(9.1, 2.25, "ID_i, cryptogram", fs=9.5)
    D.text(9.1, 0.4, "5. use: every card has its own key, the bank stores only K_M", fs=10, bold=True)
    D.arrow([(15.9, 4.75), (15.9, 4.0), (5.5, 4.0), (5.5, 2.7)], color="#999999")
    D.save(out("15/smartcard"))


if __name__ == "__main__":
    only = sys.argv[1:]
    for name, fn in FIGS.items():
        if not only or any(name.startswith(o) for o in only):
            fn()
            print("drew", name)
