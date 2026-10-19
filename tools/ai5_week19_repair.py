# Hand-constructed representation repair, not a training run.
def represent(width, height):
    return [max(0,width-height), max(0,height-width)]

def recover(hidden, total):
    difference = hidden[0]-hidden[1]
    return (total+difference)/2, (total-difference)/2

for width,height in [(4,2),(5,3),(2,4),(3,3)]:
    hidden = represent(width,height)
    total = width+height
    reconstructed = recover(hidden,total)
    area = reconstructed[0]*reconstructed[1]
    print('input', (width,height), 'h', hidden, 'sum', total,
          'recovered', reconstructed, 'area', area)
    assert reconstructed == (width,height)
print('h alone collides:', represent(4,2)==represent(5,3))
print('sum alone collides:', 4+2==2+4, 'but wider targets differ:', int(4>2),int(2>4))
# Assume exact valid measurements and compatible hidden/total values from this encoder.
