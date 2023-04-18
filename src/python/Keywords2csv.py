import pandas as pd

# Pull down Daniel's keywords list and convert it to a list
f = open("data/keywords_filtered.txt")
keywords = f.read()
f.close()
output = keywords.split("\n")
keywords = [item.split(':')[0] for item in output]
# print(keywords)

# Save the keyword list to a CSV file
with open('data/keywords.csv', 'w') as f:
    for keyword in keywords:
        f.write(f"{keyword}\n")
