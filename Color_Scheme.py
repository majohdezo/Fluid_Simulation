from matplotlib.colors import LinearSegmentedColormap

colors1 = [(0, 0, 0), (0.9, 0.9, 0.9), (1, 1, 1)] 
colors2 = [(0, 0, 0.05), (0.1, 0.1, 0.4),(0.2, 0.8, 0.9), (1, 1, 1)] #Cold
colors3 = [(0, 0, 0),(1, 0, 0), (0.9, 0.5, 0.1), (1, 0.7, 0.15), (1, 1, 0)] #Fire
colors4 = [(0.8, 0.8, 0.8), (0.01, 0.5, 0.08), (0.1, 0.95, 0.12), (1, 1, 0)] #Greens fondo claro
colors5 = [(0.8, 0.8, 0.8), (0.1, 0.1, 0.4),(0.2, 0.8, 0.9), (1, 1, 1)] #Cold fondo claro
colors6 = [(0, 0, 0),(1, 0, 1), (0.1, 1, 1)] #Magenta to cyan
colors7 = [(0.07, 0.03, 0.08),(0.10, 0.18, 0.2), (0.1, 0.4, 0.3), 
            (0.7, 0.6, 0.3),(0.85, 0.5, 0.8), (0.79, 0.9, 0.95), (1, 1, 1)] 
colors8 = [(0.6, 0.1, 0.25),(0.95, 0.58, 0.35), (0.99, 0.8, 0.5), 
                (0.8, 0.9, 0.63),(0.25, 0.63, 0.7), (0.75, 0.78, 0.7)] #Colores
colors9 = [(0.15, 0.15, 0.2),(0.4, 0.41, 0.52), (0.6, 0.7, 0.75), (1, 1, 1)] 
colors10 = [(1, 1, 1),(0.6, 0.7, 0.75), (0.4, 0.41, 0.52),(0.15, 0.15, 0.2)]  
colors11 = [(0, 0, 0),(0.6, 0, 0.6), (1, 0.8, 1), (1, 1, 1)]  
colors12 = [(0.9, 0.87, 0.9), (0.42, 0.55, 0.75),(0.68, 0.3, 0.33), (0.2, 0.08, 0.22)] 
colors13 = [(0.4, 0.4, 0.4), (0.1, 0.1, 0.4),(0.2, 0.8, 0.9), (1, 1, 0)] 
colors14 = [(0.2, 0.2, 0.2),(1, 0, 1), (0.9, 0.5, 0.1),  (1, 1, 0)]
colors15 = [(0.2, 0.08, 0.22),(0.42, 0.55, 0.75), (0.9, 0.87, 0.9), (0.68, 0.3, 0.33)] 

cmap_name = 'my_list'

def selectColor(a):
    if(a==1):
        cmap = LinearSegmentedColormap.from_list(cmap_name, colors1, N=100)
    if(a==2):
        cmap = LinearSegmentedColormap.from_list(cmap_name, colors2, N=100)
    if(a==3):
        cmap = LinearSegmentedColormap.from_list(cmap_name, colors3, N=100)
    if(a==4):
        cmap = LinearSegmentedColormap.from_list(cmap_name, colors4, N=100)
    if(a==5):
        cmap = LinearSegmentedColormap.from_list(cmap_name, colors5, N=100)
    if(a==6):
        cmap = LinearSegmentedColormap.from_list(cmap_name, colors6, N=100)
    if(a==7):
        cmap = LinearSegmentedColormap.from_list(cmap_name, colors7, N=100)
    if(a==8):
        cmap = LinearSegmentedColormap.from_list(cmap_name, colors8, N=100)
    
    if(a==9):
        cmap = LinearSegmentedColormap.from_list(cmap_name, colors9, N=100)
    if(a==10):
        cmap = LinearSegmentedColormap.from_list(cmap_name, colors10, N=100)
    if(a==11):
        cmap = LinearSegmentedColormap.from_list(cmap_name, colors11, N=100)
    if(a==12):
        cmap = LinearSegmentedColormap.from_list(cmap_name, colors12, N=100)
    if(a==13):
        cmap = LinearSegmentedColormap.from_list(cmap_name, colors13, N=100)
    if(a==14):
        cmap = LinearSegmentedColormap.from_list(cmap_name, colors14, N=100)
    if(a==15):
        cmap = LinearSegmentedColormap.from_list(cmap_name, colors15, N=100)


    return cmap