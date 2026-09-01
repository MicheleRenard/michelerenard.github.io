#!/usr/bin/env python3
"""
Synthesise the RPG page's town theme — an original ~34 s chiptune loop.

Like the sprites, the music is generated from code so the whole page stays
reproducible and free of third-party assets. Square-wave leads, triangle
bass, a soft noise tick: the classic 16-bit palette, written as a gentle
village andante in C major.

Writes a temporary WAV (stdlib `wave`), then converts to AAC (.m4a) with
macOS's built-in `afconvert` — AAC plays everywhere, including iOS Safari.

    python3 tools/build-rpg-audio.py
"""

import subprocess
import sys
import tempfile
import wave
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "rpg" / "assets" / "audio" / "theme.m4a"

SR = 44100
BPM = 96
BEAT = 60 / BPM          # crotchet seconds
BAR = 4 * BEAT

# ---------------------------------------------------------------------------
# note helpers
# ---------------------------------------------------------------------------

A4 = 440.0
NOTES = {"C": -9, "C#": -8, "D": -7, "D#": -6, "E": -5, "F": -4,
         "F#": -3, "G": -2, "G#": -1, "A": 0, "A#": 1, "B": 2}


def freq(name):
    """'C4' -> Hz."""
    pitch, octave = name[:-1], int(name[-1])
    semis = NOTES[pitch] + (octave - 4) * 12
    return A4 * 2 ** (semis / 12)


def square(f, t, duty=0.5):
    return np.where((t * f) % 1 < duty, 1.0, -1.0)


def triangle(f, t):
    return 2 * np.abs(2 * ((t * f) % 1) - 1) - 1


def env(n, attack=0.01, release=0.08, level=1.0):
    """Simple attack/sustain/release envelope over n samples."""
    e = np.full(n, level)
    a = max(1, int(attack * SR))
    r = max(1, int(release * SR))
    e[:a] *= np.linspace(0, 1, a)
    if r < n:
        e[-r:] *= np.linspace(1, 0, r)
    return e


def render(track, wave_fn, gain, duty=None, vibrato=0.0):
    """track: list of (note_or_None, beats). Returns full mono array."""
    chunks = []
    for note, beats in track:
        n = int(beats * BEAT * SR)
        if note is None:
            chunks.append(np.zeros(n))
            continue
        t = np.arange(n) / SR
        f = freq(note)
        if vibrato:
            t = t + vibrato * np.sin(2 * np.pi * 5.5 * t) / f
        tone = wave_fn(f, t, duty) if duty is not None else wave_fn(f, t)
        chunks.append(tone * env(n, release=min(0.12, beats * BEAT * 0.3)) * gain)
    return np.concatenate(chunks)


# ---------------------------------------------------------------------------
# the tune: 16 bars, I–vi–IV–V twice, with an answering phrase
# ---------------------------------------------------------------------------

# lead (square, gentle duty 0.35, light vibrato)
L = [
    # phrase A (bars 1–4)
    ("E5", 1), ("G5", 1), ("A5", 1.5), ("G5", 0.5),
    ("E5", 1), ("C5", 1), ("D5", 2),
    ("F5", 1), ("A5", 1), ("G5", 1.5), ("E5", 0.5),
    ("D5", 1), ("E5", 1), ("C5", 2),
    # phrase A' (bars 5–8)
    ("E5", 1), ("G5", 1), ("A5", 1.5), ("C6", 0.5),
    ("B5", 1), ("G5", 1), ("A5", 2),
    ("F5", 1), ("E5", 1), ("D5", 1.5), ("E5", 0.5),
    ("C5", 3), (None, 1),
    # phrase B (bars 9–12) — quieter, questioning
    ("G5", 1.5), ("E5", 0.5), ("F5", 1), ("D5", 1),
    ("E5", 1.5), ("C5", 0.5), ("D5", 1), ("B4", 1),
    ("C5", 1), ("E5", 1), ("G5", 1), ("A5", 1),
    ("G5", 3), (None, 1),
    # phrase B' resolve (bars 13–16)
    ("A5", 1.5), ("G5", 0.5), ("E5", 1), ("G5", 1),
    ("F5", 1.5), ("E5", 0.5), ("D5", 1), ("F5", 1),
    ("E5", 1), ("D5", 1), ("C5", 1), ("D5", 1),
    ("C5", 3), (None, 1),
]

# harmony (square, hollow duty 0.25) — held chord tones
H = [
    ("C4", 4), ("A3", 4), ("F4", 4), ("G4", 4),
    ("C4", 4), ("A3", 4), ("F4", 4), ("G3", 4),
    ("E4", 4), ("C4", 4), ("F4", 4), ("G4", 4),
    ("F4", 4), ("D4", 4), ("G4", 4), ("C4", 4),
]

# bass (triangle) — roots with a passing fifth
B = []
for root, fifth in [("C3", "G3"), ("A2", "E3"), ("F2", "C3"), ("G2", "D3")] * 2 + \
                   [("C3", "G3"), ("A2", "E3"), ("F2", "C3"), ("G2", "D3")] + \
                   [("F2", "C3"), ("D3", "A3"), ("G2", "D3"), ("C3", "G3")]:
    B += [(root, 1.5), (fifth, 0.5), (root, 1), (fifth, 1)]


def main():
    lead = render(L, square, 0.16, duty=0.35, vibrato=0.002)
    harm = render(H, square, 0.055, duty=0.25)
    bass = render(B, triangle, 0.22)

    n = min(len(lead), len(harm), len(bass))
    mix = lead[:n] + harm[:n] + bass[:n]

    # soft noise tick on each beat (brushed hat)
    rng = np.random.default_rng(7)  # fixed seed: reproducible output
    beat_n = int(BEAT * SR)
    tick = rng.uniform(-1, 1, int(0.03 * SR)) * np.linspace(0.05, 0, int(0.03 * SR))
    for b in range(n // beat_n):
        s = b * beat_n
        seg = min(len(tick), n - s)
        mix[s:s + seg] += tick[:seg] * (1.0 if b % 2 == 0 else 0.55)

    # gentle echo, then soften the square edges with a one-pole low-pass
    d = int(0.75 * BEAT * SR)
    mix[d:] += 0.18 * mix[:-d].copy()
    out = np.empty_like(mix)
    acc = 0.0
    alpha = 0.35
    for i, x in enumerate(mix):          # small n; fine in pure numpy-less loop
        acc += alpha * (x - acc)
        out[i] = acc

    out /= max(1e-9, np.max(np.abs(out))) / 0.85

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        wav_path = Path(tmp.name)
    with wave.open(str(wav_path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((out * 32767).astype(np.int16).tobytes())

    OUT.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["afconvert", "-f", "m4af", "-d", "aac", "-b", "96000",
         str(wav_path), str(OUT)],
        check=True,
    )
    wav_path.unlink()
    secs = n / SR
    print(f"wrote {OUT.relative_to(ROOT)}  ({OUT.stat().st_size:,} bytes, {secs:.1f}s loop)")


if __name__ == "__main__":
    sys.exit(main())
