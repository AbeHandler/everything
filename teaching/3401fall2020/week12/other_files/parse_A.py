from bs4 import BeautifulSoup

with open("some_html.html", "r") as inf: 
    dt = inf.read()

soup = BeautifulSoup(dt, 'html.parser')
items = soup.select("div > a")
print(len(items))

total = 0
for c in items:
    total += 1 

print(total)
