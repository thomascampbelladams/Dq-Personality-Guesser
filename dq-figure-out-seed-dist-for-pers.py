import itertools
import random
import logging
import argparse
from personality_table import personality_table
from base_stats import base_stats

# Enable or disable logging
DEBUG_MODE = True

# Configure logging
log_file_path = r'D:\source\repos\ADO Custom Form Extension\Custom-Form-Extension-And-Webapi\Ado-Extension\log.txt'
if DEBUG_MODE:
    logging.basicConfig(level=logging.DEBUG, filename=log_file_path, filemode='w')
else:
    logging.basicConfig(level=logging.INFO, filename=log_file_path, filemode='w')

# Define the argument parser
parser = argparse.ArgumentParser(description='Optimize seed distribution for desired personality.')
parser.add_argument('class_name', type=str, help='Character class name')
parser.add_argument('gender', type=str, help='Character gender')
parser.add_argument('desired_personality', type=str, help='Desired personality')
parser.add_argument('initial_stats', type=str, help='Initial stats in the format "Strength:13,Agility:6,Resilience:14,Wisdom:4,Luck:6"')
parser.add_argument('--iterations', type=int, default=1000, help='Number of iterations for simulation')

args = parser.parse_args()

# Parse initial stats
initial_stats = dict(item.split(":") for item in args.initial_stats.split(","))
initial_stats = {k: int(v) for k, v in initial_stats.items()}

# Seed combinations (5 seeds, distributed across stats)
seed_combinations = list(itertools.combinations_with_replacement(["Strength", "Agility", "Resilience", "Wisdom", "Luck"], 5))

def distribute_seeds(initial_stats, seed_distribution):
    modified_stats = initial_stats.copy()
    for stat in seed_distribution:
        modified_stats[stat] += random.randint(1, 3)
    return modified_stats, seed_distribution

def calculate_growth(base, modified):
    growth = {k: max(modified[k] - base[k], 0) for k in base}
    return growth

def find_personality(class_name, base, modified, growth):
    sorted_growth = sorted(growth.items(), key=lambda x: x[1], reverse=True)
    highest, second = sorted_growth[0][0], sorted_growth[1][0]
    highest_value = modified[highest]
    for (stat1, stat2, condition), personality in personality_table[class_name].items():
        if highest == stat1 and (second == stat2 or stat2 == "Any") and eval(f"{highest_value}{condition}"):
            return personality
    return "Unknown"

def get_personalities_for_stats(character_class, gender, growth):
    possible_personalities = []
    if character_class not in personality_table:
        return possible_personalities

    sorted_growth = sorted(growth.items(), key=lambda x: x[1], reverse=True)
    highest, second = sorted_growth[0][0], sorted_growth[1][0]
    highest_value = growth[highest]

    class_table = personality_table[character_class]
    for (g, stat1, stat2, range_expr), personalities in class_table.items():
        if g == gender and highest == stat1 and (second == stat2 or stat2 == "Any"):
            if parse_range_expression(range_expr, highest_value):
                possible_personalities.extend(personalities)
    return possible_personalities

def parse_range_expression(range_expr, value):
    expr = range_expr.replace("Yes", "").replace("Yes2", "").replace("Yes3", "").replace("Yes4", "")
    expr = expr.strip()

    if "≥" in expr:
        parts = expr.split("≥")
        if len(parts) == 2:
            num = int(parts[1])
            return value >= num
    elif "≤" in expr:
        parts = expr.split("≤")
        if len(parts) == 2:
            num = int(parts[1])
            return value <= num
    elif "–" in expr:
        parts = expr.split("–")
        if len(parts) == 2:
            low, high = parts
            return int(low) <= value <= int(high)
    else:
        return False

def simulate_distribution(class_name, gender, desired_personality, initial_stats, seed_dist, iterations):
    base = base_stats[class_name][gender]
    success_count = 0
    personality_counts = {}

    for _ in range(iterations):
        modified, _ = distribute_seeds(initial_stats, seed_dist)
        growth = calculate_growth(base, modified)
        personalities = get_personalities_for_stats(class_name, gender, growth)
        for personality in personalities:
            if personality not in personality_counts:
                personality_counts[personality] = 0
            personality_counts[personality] += 1
            if desired_personality == personality:
                success_count += 1
                break

    success_rate = success_count / iterations
    personality_percentages = {k: (v / iterations) * 100 for k, v in personality_counts.items()}
    return success_rate, personality_percentages

def find_best_distribution(class_name, gender, desired_personality, initial_stats, iterations):
    best_distribution = None
    best_success_rate = 0
    best_personality_percentages = {}

    for seed_dist in seed_combinations:
        success_rate, personality_percentages = simulate_distribution(class_name, gender, desired_personality, initial_stats, seed_dist, iterations)
        if success_rate > best_success_rate:
            best_distribution = seed_dist
            best_success_rate = success_rate
            best_personality_percentages = personality_percentages

    return best_distribution, best_success_rate, best_personality_percentages

# Example usage with parsed arguments
class_name = args.class_name
gender = args.gender
desired_personality = args.desired_personality
iterations = args.iterations

best_distribution, success_rate, personality_percentages = find_best_distribution(class_name, gender, desired_personality, initial_stats, iterations)

print(f"Best seed distribution for {class_name} ({gender}) to achieve {desired_personality}: {best_distribution}")
print(f"Average success rate: {success_rate * 100:.2f}%")
print(f"Personality percentages: {personality_percentages}")
