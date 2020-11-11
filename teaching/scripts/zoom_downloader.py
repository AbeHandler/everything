import re
import mechanize

br = mechanize.Browser()
br.open("https://cuboulder.zoom.us/recording")

print(br.title())