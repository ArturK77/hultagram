# Sorts favorites by value using .get
import csv

from collections import Counter

# Open CSV file
with open("favorites.csv", "r") as file:

    # Create DictReader
    reader = csv.DictReader(file)

    # Counts
    counts = Counter()

    # Iterate over CSV file, counting favorites
    for row in reader:
        song = row["song"]
        counts[favorite] += 1

# Print counts
for favorite, count in counts.most_common():
    print(f"Favorite Song {song}: {count}")


