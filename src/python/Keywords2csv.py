import pandas as pd

# Your keyword list
keywords = [
    "energy",
    "heating",
    "water",
    "heat",
    "boilers",
    "air",
    "sustainability",
    "reduce",
    "efficiency",
    "hot",
    "lighting",
    "quality",
    "oil",
    "steam",
    "costs",
    "savings",
    "boiler",
    "service",
    "emissions",
    "cost",
    "repairs",
    "repair",
    "performance",
    "greenhouse",
    "gas",
    "commitment",
    "conservation",
    "largest",
    "upgrade",
    "apartments",
    "replacement",
    "fuel",
    "carbon",
    "initiative",
    "power",
    "reduction",
    "climate",
    "services",
    "homes",
    "environmental"
]

# Save the keyword list to a CSV file
with open('keywords.csv', 'w') as f:
    for keyword in keywords:
        f.write(f"{keyword}\n")
