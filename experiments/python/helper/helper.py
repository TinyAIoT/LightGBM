from matplotlib.cm import viridis
from matplotlib.colors import Normalize

def __init__(self):
    self.init = True
    
def rgb_to_hex(r, g, b):
    r_int = int(r * 255)
    g_int = int(g * 255)
    b_int = int(b * 255)
    return ('{:02X}' * 3).format(r_int, g_int, b_int)

def generatecolors(rangeint):
    norm2 = Normalize(vmin=0, vmax=rangeint - 1)
    colors2 = [viridis(norm2(i)) for i in range(rangeint)]
    for x in range(rangeint):
        print(self.rgb_to_hex(colors2[x][0], colors2[x][1], colors2[x][2]))

def bits_to_kb(x):
    return x / (8 * 1024)

def bits_to_kb_str(x, pos):
    x = x / (8 * 1024)
    return f"{x:.1f} KB"

def dict_to_markdown_table(data, name):
    # Bestimme die Spaltennamen
    columns = list(data.keys())

    # Erstelle die Tabellenzeilen
    print(range(len(list(data.values()))))
    rows = []
    max_length = max([len(value) for value in data.values()])
    for i in range(max_length):
        row = []
        for column in columns:
            if i < len(data[column]):
                row.append(str(round(data[column].iloc[i], 4)))
            else:
                row.append("")
        rows.append(row)

    table = ""
    # Erstelle die Markdown-Tabelle
    if name == 'breastcancer':
        table = "|" + "|".join(columns) + "|\n"
        table += "|" + "|".join("---" for _ in columns) + "|\n"
    table += "|" + name + "|\n"
    for row in rows:
        table += "|" + "|".join(row) + "|\n"

    # writes the table to a file called markdown tables
    filename = "markdowntables.md"

    # Schreibe den String in die Datei
    if name == 'breastcancer':
        with open(filename, "w") as file:
            file.write(table)
    else:
        with open(filename, "a") as file:
            file.write(table)

    return table
