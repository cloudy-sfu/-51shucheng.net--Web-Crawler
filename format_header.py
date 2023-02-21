lines = []
while (not lines) or lines[-1]:
    lines.append(input())
lines.pop()
header = {}
for x in lines:
    x_pieces = x.split(':', maxsplit=1)
    header[x_pieces[0]] = x_pieces[1].strip()
print(header.__str__())
