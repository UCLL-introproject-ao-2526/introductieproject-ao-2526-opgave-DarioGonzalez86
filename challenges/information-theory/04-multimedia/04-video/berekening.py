pixel = 1920 * 1080
bits = 24
fps = 23.976
netflix = 3502 * 2**10

niet_compr = pixel * bits * fps

ratio = niet_compr / netflix
print(ratio)
