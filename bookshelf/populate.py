import csv 
from bookshelf.models import Browse #Change App Name

with open('C://Users/sneha/OneDrive/Documents/PES_Stuff/SEM_4_STUFF/WF/WF PROJECT/books_new.csv', encoding='utf-8') as csvfile:   
    reader=csv.DictReader(csvfile)
    for row in reader:
            p = Browse(title=row['Title'],author=row['Author'],genre=row['Genre'],summary=row['Summary'])
            p.save()

