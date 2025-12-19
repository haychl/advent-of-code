from pathlib import Path
from collections.abc import Iterable

INPUT_PATH = Path(__file__).parent / "day02_sample_input.txt"

IdRange = tuple[int, int]
Limits = tuple[int, int]
Invalids = set[int]


def parse_input(input_file: Path) -> list[IdRange]:
    text = input_file.read_text().strip()
    id_ranges = []
    for chunk in text.split(","):
        start, end = map(int, chunk.split("-",1))
        id_ranges.append((start, end))
    return id_ranges


def sort_ranges_by_len(id_ranges: list[IdRange]) -> dict[int, list[IdRange]]:
    ranges_by_len: dict[int, list[IdRange]] = {}
    for start, end in id_ranges:
        for id_len in range(len(str(start)), len(str(end)) + 1):
            ranges_by_len.setdefault(id_len, []).append((start, end))
    return ranges_by_len


def get_limits_per_len(ranges_by_len: dict[int, list[IdRange]]) -> dict[int, Limits]:
    limits_per_len: dict[int, Limits] = {}
    for id_len, id_ranges in ranges_by_len.items():
        starts, ends = zip(*id_ranges)
        len_floor = 10 ** (id_len - 1)
        len_ceiling = (10 ** id_len) - 1
        lo = max(min(starts), len_floor)
        hi = min(max(ends), len_ceiling)
        limits_per_len[id_len] = (lo, hi)
    return limits_per_len


def get_seq_lens(id_len: int, part: int) -> set[int]:
    seq_lens = [n for n in range(1, id_len // 2 + 1) if (id_len % n == 0)]
    nonredundant_seq_lens = []
    for seq_len in seq_lens:
        if not any(other_len > seq_len and other_len % seq_len == 0 for other_len in seq_lens):
            nonredundant_seq_lens.append(seq_len)
    half_len = id_len // 2 if id_len % 2 == 0 else None
    if part == 1:
        return [half_len] if half_len is not None else []
    else:
        return [seq_len for seq_len in nonredundant_seq_lens if seq_len != half_len]


def iter_candidates_per_len(id_len: int, limits: Limits, part: int) -> Iterable[int]:
    lo_str, hi_str = map(str, limits)
    for seq_len in get_seq_lens(id_len, part):
        lo_seq, hi_seq = int(lo_str[:seq_len]), int(hi_str[:seq_len])
        sequences = range(lo_seq, hi_seq + 1)
        seq_repeats = id_len // seq_len
        for seq in sequences:
            candidate = int(str(seq) * seq_repeats)
            yield candidate


def get_all_invalids(ranges_by_len: dict[int, list[IdRange]], limits_per_len: dict[int, Limits]) -> tuple[Invalids, Invalids]:
    invalids_per_part: dict[int, Invalids] = {1: set(), 2: set()}
    for id_len, id_ranges in ranges_by_len.items():
        limits = limits_per_len[id_len]
        for part, invalids in invalids_per_part.items():
            for candidate in iter_candidates_per_len(id_len, limits, part):
                if any(start <= candidate <= end for start, end in id_ranges):   
                    invalids.add(candidate)
    invalids_per_part[2] |= invalids_per_part[1]
    return invalids_per_part[1], invalids_per_part[2]


def solve(input_file: Path) -> tuple[int, int]:
    id_ranges = parse_input(input_file)
    ranges_by_len = sort_ranges_by_len(id_ranges)
    limits_per_len = get_limits_per_len(ranges_by_len)
    invalids_part1, invalids_part2 = get_all_invalids(ranges_by_len, limits_per_len)
    return sum(invalids_part1), sum(invalids_part2)


def main() -> None:
    part1, part2 = solve(INPUT_PATH)
    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")


if __name__ == "__main__":
    main()