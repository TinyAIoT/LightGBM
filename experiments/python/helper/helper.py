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


