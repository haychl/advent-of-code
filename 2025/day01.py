from pathlib import Path


DIAL_SIZE = 100
START_POS = 50
INPUT_PATH = Path(__file__).parent / "day01_sample_input.txt"


def parse_input(input_file: Path) -> list[int]:
    spins = []
    with input_file.open() as f:
        for line in f:
            instruction = line.strip()
            spin_dir, spin_clicks = instruction[0], int(instruction[1:])
            spin = spin_clicks if spin_dir == "R" else -spin_clicks
            spins.append(spin)
    return spins


def count_zero_passes(pos_old: int, pos_new: int, spin: int) -> int:
    full_spins = abs(spin) // DIAL_SIZE
    spin_R = spin > 0
    pos_both_zero = (pos_old == 0) and (pos_new == 0)
    remainder_zero_pass_R = spin_R and pos_new != 0 and pos_new < pos_old
    remainder_zero_pass_L = (not spin_R) and pos_old != 0 and pos_new > pos_old
    if pos_both_zero and full_spins > 0:
        zero_passes = full_spins - 1
    elif remainder_zero_pass_R or remainder_zero_pass_L:
        zero_passes = full_spins + 1
    else: 
        zero_passes = full_spins
    return zero_passes


def solve_part1(spins: list[int]) -> int:
    pos = START_POS
    password = 0
    for spin in spins:
        pos = (pos + spin) % DIAL_SIZE
        if pos == 0:
            password += 1
    return password


def solve_part2(spins: list[int]) -> int:
    pos = START_POS
    zero_passes = 0
    for spin in spins:
        pos_old = pos
        pos = (pos + spin) % DIAL_SIZE
        zero_passes += count_zero_passes(pos_old, pos, spin)
    return zero_passes


def main():
    spins = parse_input(INPUT_PATH)
    password = solve_part1(spins) + solve_part2(spins)
    print(password)


if __name__ == "__main__":
    main()