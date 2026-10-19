def pool2(image):
    h, w = len(image), len(image[0])
    if h < 2 or w < 2:
        raise ValueError("Need a complete 2 by 2 window")
    maxima, means = [], []
    for r in range(0, h - 1, 2):
        max_row, mean_row = [], []
        for c in range(0, w - 1, 2):
            values = [image[r+i][c+j]
                      for i in range(2) for j in range(2)]
            max_row.append(max(values))
            mean_row.append(sum(values) / 4)
        maxima.append(max_row)
        means.append(mean_row)
    return maxima, means

x = [[1, 4, 2, 0], [3, 2, 5, 1],
     [0, 6, 1, 3], [2, 4, 2, 7]]
assert pool2(x) == ([[4, 5], [6, 7]],
                    [[2.5, 2], [3, 3.25]])
# Complete collision, boundary and movement probes under the same rule.
left = [[4,0],[0,0]]
right = [[0,4],[0,0]]
print('different positions, same summaries', pool2(left), pool2(right))
print('all-negative window', pool2([[-4,-2],[-7,-3]]))
print('ignored incomplete boundary', pool2([[1,2,99],[3,4,99],[99,99,99]]))
before = [[0,8,0,0],[0,0,0,0]]
after = [[0,0,8,0],[0,0,0,0]]
pre_max, pre_mean = pool2(before)
post_max, post_mean = pool2(after)
print('cross boundary before max/mean', pre_max,pre_mean)
print('cross boundary after max/mean', post_max,post_mean)
# One explicitly constructed head proves a prediction need not be shift-invariant.
print('head class1 if left max>0:', int(pre_max[0][0]>0),int(post_max[0][0]>0))
def max_with_position(window):
    candidates = [(value, r, c) for r,row in enumerate(window) for c,value in enumerate(row)]
    # Row-major first position wins a tie; these two probes have a unique maximum.
    value, r, c = max(candidates, key=lambda item: item[0])
    return value, (r,c)

print('max plus position still collides:',
      max_with_position([[5,1],[2,3]]),max_with_position([[5,0],[0,0]]))
# Valid nonempty rectangular numeric maps assumed; no padding or hidden ReLU.
