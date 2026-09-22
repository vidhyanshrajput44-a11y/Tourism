with open('frontend/ui1.html', 'r') as f:
    content = f.read()

ids = ['btnBack', 'brandHome', 'navDestinations', 'predictForm']
for i in ids:
    if f'id="{i}"' in content:
        print(f'{i} found')
    else:
        print(f'{i} NOT FOUND')
