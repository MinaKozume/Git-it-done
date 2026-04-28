from pathlib import Path
p = Path('favourites') / 'models.py'
print('file:', p.resolve())
text = p.read_bytes().decode('utf-8')
lines = text.splitlines()
print('total lines:', len(lines))
for i, line in enumerate(lines, 1):
    print(f'{i:03}:', repr(line))
