"""Python scanner generator."""

# Maximum character.
NUM_SYMBOLS = 0x100

# Alphabet of symbols.
SIGMA = ''.join(chr(c) for c in range(NUM_SYMBOLS))
