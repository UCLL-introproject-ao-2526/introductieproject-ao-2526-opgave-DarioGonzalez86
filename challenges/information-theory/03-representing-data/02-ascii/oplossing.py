def binary_to_text(binary_string):
    # nakijken of de string deelbaar is door 8, anders wordt het moeilijk :)
    if len(binary_string) % 8 != 0:
        raise ValueError("String moet een veelvoudzijn van 8")

    chars = [
        chr(int(binary_string[i:i+8], 2))
        for i in range(0, len(binary_string), 8)  # stapgrootte van 8
    ]
    return "".join(chars)


binary = "01000011011011110111001001110010011001010110001101110100"
print(binary_to_text(binary))
