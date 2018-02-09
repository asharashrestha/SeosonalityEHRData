import csv

patriots_wins = 0
f = open("nfl.csv", "r")
nfl = list(csv.reader(f))
for x in nfl[2]:
    print
    x
    if x == "New England Patriots":
        patriots_wins = patriots_win + 1
