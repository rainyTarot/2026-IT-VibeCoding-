from __future__ import annotations

import math
import random
import wave
from pathlib import Path


ROOT = Path(__file__).parent
ASSETS = ROOT / "assets"
ASSETS.mkdir(exist_ok=True)

SAMPLE_RATE = 44100


def clamp_sample(value: float) -> int:
    return max(-32767, min(32767, int(value * 32767)))


def write_wav(path: Path, samples: list[float]) -> None:
    with wave.open(path.as_posix(), "w") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(SAMPLE_RATE)
        frames = bytearray()
        for sample in samples:
            frames += clamp_sample(sample).to_bytes(2, "little", signed=True)
        wav_file.writeframes(frames)


def envelope(index: int, total: int, attack: float = 0.02, release: float = 0.12) -> float:
    progress = index / max(1, total - 1)
    if progress < attack:
        return progress / max(attack, 1e-6)
    if progress > 1.0 - release:
        return max(0.0, (1.0 - progress) / max(release, 1e-6))
    return 1.0


def tone_sweep(duration: float, start_hz: float, end_hz: float, volume: float, wobble: float = 0.0) -> list[float]:
    total = int(SAMPLE_RATE * duration)
    samples: list[float] = []
    phase = 0.0
    for index in range(total):
        t = index / SAMPLE_RATE
        hz = start_hz + (end_hz - start_hz) * (index / max(1, total - 1))
        hz += math.sin(t * 18.0) * wobble
        phase += (2.0 * math.pi * hz) / SAMPLE_RATE
        amp = envelope(index, total, attack=0.01, release=0.18)
        sample = math.sin(phase) * volume * amp
        samples.append(sample)
    return samples


def noise_burst(duration: float, volume: float) -> list[float]:
    total = int(SAMPLE_RATE * duration)
    samples: list[float] = []
    for index in range(total):
        amp = envelope(index, total, attack=0.002, release=0.35)
        sample = (random.uniform(-1.0, 1.0) * 0.7 + math.sin(index * 0.42) * 0.3) * volume * amp
        samples.append(sample)
    return samples


def layer(*tracks: list[float]) -> list[float]:
    total = max(len(track) for track in tracks)
    mixed = [0.0] * total
    for track in tracks:
        for index, sample in enumerate(track):
            mixed[index] += sample
    return [max(-1.0, min(1.0, sample)) for sample in mixed]


def make_start() -> None:
    track = layer(
        tone_sweep(0.22, 380.0, 620.0, 0.35, wobble=8.0),
        tone_sweep(0.32, 760.0, 1120.0, 0.20, wobble=14.0),
    )
    write_wav(ASSETS / "sfx_start.wav", track)


def make_hit() -> None:
    track = layer(
        tone_sweep(0.12, 1220.0, 720.0, 0.30, wobble=32.0),
        tone_sweep(0.10, 1820.0, 1280.0, 0.18, wobble=24.0),
        noise_burst(0.06, 0.10),
    )
    write_wav(ASSETS / "sfx_hit.wav", track)


def make_miss() -> None:
    track = layer(
        tone_sweep(0.14, 420.0, 250.0, 0.22, wobble=4.0),
        noise_burst(0.05, 0.06),
    )
    write_wav(ASSETS / "sfx_miss.wav", track)


def make_game_over() -> None:
    track = layer(
        tone_sweep(0.40, 510.0, 220.0, 0.26, wobble=3.0),
        tone_sweep(0.36, 300.0, 120.0, 0.16, wobble=2.0),
    )
    write_wav(ASSETS / "sfx_game_over.wav", track)


def main() -> None:
    random.seed(7)
    make_start()
    make_hit()
    make_miss()
    make_game_over()


if __name__ == "__main__":
    main()
