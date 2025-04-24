# test_coverage_stats.py

import random
from collections import Counter, defaultdict
from cards import ATTACK_CARDS, DEFENSE_MAP, DEFENSE_CARDS
from game import select_player_cards

def test_defense_coverage_with_stats(trials=100):
    random.seed(0)

    # Счётчики
    attack_counts = Counter()                    # сколько раз встретилась каждая атака
    defense_cover_counts = defaultdict(Counter)  # для каждой атаки — Counter защит, которые её покрыли

    for t in range(1, trials + 1):
        hacker_deck = random.sample(ATTACK_CARDS, 10)
        player_deck = select_player_cards(hacker_deck)

        print(f"\n=== Trial {t} ===")
        print("Hacker deck:", hacker_deck)
        print("Player deck:", player_deck)

        # Проверяем каждую атаку
        for attack in hacker_deck:
            attack_counts[attack] += 1
            valid = set(DEFENSE_MAP[attack].keys())
            matched = valid.intersection(player_deck)

            if matched:
                # Если найдено несколько, перечисляем их
                print(f"  Attack '{attack}' is covered by: {sorted(matched)}")
                for d in matched:
                    defense_cover_counts[attack][d] += 1
            else:
                print(f"  [FAIL] Attack '{attack}' has NO coverage! Expected one of {valid}")

    # Итоговая статистика
    print("\n" + "="*30 + "\nSUMMARY STATISTICS\n" + "="*30)
    for attack in sorted(attack_counts):
        total = attack_counts[attack]
        covers = defense_cover_counts[attack]
        print(f"\nAttack '{attack}': seen {total} times")
        if covers:
            for defense, cnt in covers.most_common():
                pct = cnt / total * 100
                print(f"  Covered by '{defense}': {cnt} times ({pct:.1f}%)")
        else:
            print("  NEVER covered!")

if __name__ == "__main__":
    test_defense_coverage_with_stats(trials=100)