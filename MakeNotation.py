notation_list = []

with open('XN.txt', 'r') as f:
    xn_list = f.readlines()
    new_element = None
    for line in xn_list:
        if len(line) > 4:
            l = line.split()
            for element in l:
                if element[0].isupper() or element[1].isupper():
                    if element[0] == 'N':
                        new_element = element.replace('N', 'H')
                    if element[0] == 'B':
                        new_element = element.replace('B', 'E')
                    if element[0] == '-':
                        new_element = element[1] + '-' + element[2:]
                        if new_element[0] == 'N':
                            new_element = new_element.replace('N', 'H')
                        if new_element[0] == 'B':
                            new_element = new_element.replace('B', 'E')
                    if element[0] == '+':
                        new_element = element[1] + '+' + element[2:]
                        if new_element[0] == 'N':
                            new_element = new_element.replace('N', 'H')
                        if new_element[0] == 'B':
                            new_element = new_element.replace('B', 'E')
                if element[0].islower() or element[1].islower():
                    if element[0] == 'n':
                        new_element = element.replace('n', 'h')
                    if element[0] == 'b':
                        new_element = element.replace('b', 'e')
                    if element[0] == '-':
                        new_element = element[1] + '-' + element[2:]
                        if new_element[0] == 'n':
                            new_element = new_element.replace('n', 'h')
                        if new_element[0] == 'b':
                            new_element = new_element.replace('b', 'e')
                    if element[0] == '+':
                        new_element = element[1] + '+' + element[2:]
                        if new_element[0] == 'n':
                            new_element = new_element.replace('n', 'h')
                        if new_element[0] == 'b':
                            new_element = new_element.replace('b', 'e')
                if new_element:
                    notation_list.append(new_element)
                    new_element = None
                if len(element) == 4 and element[0].isalpha() and element[0] not in ('B', 'N', 'b', 'n'):
                    notation_list.append(element)
        if len(line) == 4:
            if line[0].isupper() or line[1].isupper():
                if line[0] == 'N':
                    new_element = line.replace('N', 'H')
                if line[0] == 'B':
                    new_element = line.replace('B', 'E')
                if line[0] == '-':
                    new_element = line[1] + '-' + line[2:]
                    if new_element[0] == 'N':
                        new_element = new_element.replace('N', 'H')
                    if new_element[0] == 'B':
                        new_element = new_element.replace('B', 'E')
                if line[0] == '+':
                    new_element = line[1] + '+' + line[2:]
                    if new_element[0] == 'N':
                        new_element = new_element.replace('N', 'H')
                    if new_element[0] == 'B':
                        new_element = new_element.replace('B', 'E')
            if line[0].islower() or line[1].islower():
                if line[0] == 'n':
                    new_element = line.replace('n', 'h')
                if line[0] == 'b':
                    new_element = line.replace('b', 'e')
                if line[0] == '-':
                    new_element = line[1] + '-' + line[2:]
                    if new_element[0] == 'n':
                        new_element = new_element.replace('n', 'h')
                    if new_element[0] == 'b':
                        new_element = new_element.replace('b', 'e')
                if line[0] == '+':
                    new_element = line[1] + '+' + line[2:]
                    if new_element[0] == 'n':
                        new_element = new_element.replace('n', 'h')
                    if new_element[0] == 'b':
                        new_element = new_element.replace('b', 'e')
            if new_element:
                notation_list.append(new_element)
                new_element = None
            if len(element) == 4 and element[0].isalpha() and element[0] not in ('B', 'N', 'b', 'n'):
                notation_list.append(element)

print(notation_list)

with open('new_notations.txt', 'w') as f:
    for notation in notation_list:
        f.write(f'{notation} \n')
