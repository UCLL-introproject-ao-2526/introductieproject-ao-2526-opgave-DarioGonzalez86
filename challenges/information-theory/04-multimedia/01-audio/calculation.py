samples = 44100
bits = 16
channels = 2

spotify_compressed = 160000


def saving_bandwith(samples, bits, channels, spotify):
    bitrate = samples * bits * channels
    saved_bandwith = bitrate / spotify
    return saved_bandwith


print(saving_bandwith(samples, bits, channels, spotify_compressed))
