# Fixed numeric preprocessing examples, not learned normalization statistics.
raw = [255,128,0]
scaled = [v/255 for v in raw]
twice = [v/255 for v in scaled]
print('raw RGB', raw)
print('scaled once', [round(v,6) for v in scaled])
print('scaled twice', [round(v,6) for v in twice])
print('undo one division', [round(v*255,6) for v in scaled])
red, green = [255,0,0], [0,255,0]
print('raw red / green', red, green)
print('simple channel means', sum(red)/3, sum(green)/3)
print('red with RGB values reversed', red[::-1])
print('boundary scaling', 0/255,255/255)
# Raw values are supplied valid RGB integers. This code does not parse or validate a file.
# The simple mean is not a perceptual luminance formula.
