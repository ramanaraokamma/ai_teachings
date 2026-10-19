def local_filter(image, kernel, stride=1):
    h, w = len(image), len(image[0])
    kh, kw = len(kernel), len(kernel[0])
    if kh > h or kw > w:
        raise ValueError("Kernel does not fit")
    out = []
    for r in range(0, h - kh + 1, stride):
        row = []
        for c in range(0, w - kw + 1, stride):
            value = sum(image[r+i][c+j] * kernel[i][j]
                        for i in range(kh) for j in range(kw))
            row.append(value)
        out.append(row)
    return out

x = [[1, 2, 0], [0, 1, 3], [2, 0, 1]]
k = [[1, -1], [0, 1]]
assert local_filter(x, k) == [[0, 5], [-1, -1]]
assert local_filter(x, k, 2) == [[0]]
# Complete declared one-factor probes, with original source function above.
changed = [row[:] for row in x]
changed[0][0] = 4
print('original', local_filter(x,k))
print('one input changed', local_filter(changed,k))
print('stride 2', local_filter(x,k,2))
padded = [[0]*5] + [[0]+row+[0] for row in x] + [[0]*5]
print('one zero border', local_filter(padded,k))
flipped = [row[::-1] for row in k[::-1]]
print('flipped kernel', flipped, 'map', local_filter(x,flipped))
raw_map = local_filter(x,k)
print('ReLU after raw sums', [[max(0,v) for v in row] for row in raw_map])
print('shared bias 2', [[v+2 for v in row] for row in raw_map])
print('4 shared weights, 16 products, 5 parameters if one shared bias is added')
# Nonempty rectangular numeric arrays and positive integer stride assumed.
