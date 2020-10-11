from bs4 import BeautifulSoup

with open("some_html.html", "r") as inf: 
    dt = inf.read()

soup = BeautifulSoup(dt, 'html.parser')

winter_items = soup.select("div > a")

total = 0
for c in winter_items:
    total += 1 

print(total)
