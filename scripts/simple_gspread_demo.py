import gspread

### https://gspread.readthedocs.io/en/latest/oauth2.html#oauth-client-id
gc = gspread.oauth()

# This needs to exist already 
sh = gc.open("Example spreadsheet")

content = open('p1.tsv', 'r').read()

# fills Example spreadsheet with the rows of content
gc.import_csv(sh.id, content)