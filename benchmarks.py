#benchmarks.py
# Define benchmark data from second document
benchmarks = {
    "gdp_per_capita": {
        "global_avg": 22450,
        "regional": {"UAE": 83900, "Saudi Arabia": 54992},
        "leading": {"Luxembourg": 140000, "Singapore": 140000}
    },
    "human_capital_index": {
        "global_avg": 0.56,
        "regional": {"Saudi Arabia": 0.58, "Middle East Avg": 0.55},
        "leading": {"Singapore": 0.88, "Japan": 0.80}
    },
    "co2_per_capita": {
        "global_avg": 4.8,
        "regional": {"Kuwait": 25, "UAE": 20, "Saudi Arabia": 18},
        "leading": {"EU Average": 6.5}
    },
    "renewables_share": {
        "global_avg": 29,
        "regional": {"Middle East Avg": 4},
        "leading": {"Brazil": 85, "Norway": 90}
    },
    "stem_graduates": {
        "global_avg": 23,
        "regional": {"Saudi Arabia": 32},
        "leading": {"Oman": 43, "Germany": 37}
    },
    "sanitation": {
        "global_avg": 75,
        "regional": {"GCC Avg": 98},
        "leading": {"North America/Europe": 99}
    },
    "education_years": {
        "expected": {"global_avg": 12, "leading": 15},
        "learning_adjusted": {"global_avg": 7.8, "leading": 11}
    },
    "energy_production": {
        "lng_target": "85% increase by 2030 (126-142M tons)",
        "global_share": "Target 25% of global LNG trade"
    },
    "tertiary_enrollment": {
        "global_avg": 40,
        "qatar_growth": "From ~20% to >40% recently"
    },
    "agriculture_value": {
        "qatar": "10-11K per worker",
        "regional": {"Oman": "~6K per worker"},
        "leading": {"Advanced economies": ">50K per worker"}
    }
}