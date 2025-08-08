import random

def simulate_fight(char1, char2):
    # Tambahkan randomness ke power level
    power1 = char1["power_level"] * random.uniform(0.8, 1.2)
    power2 = char2["power_level"] * random.uniform(0.8, 1.2)
    
    winner = char1 if power1 > power2 else char2
    return {
        "winner": winner["name"],
        "details": f"{char1['name']} ({int(power1)}) vs {char2['name']} ({int(power2)})"
    }