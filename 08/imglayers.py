def read_img(imgfile, imgdim1, imgdim2):
    with open(imgfile, 'r') as reader:
        n = imgdim1 * imgdim2
        img = reader.readlines()[0]
        return [img[n*(i):n*(i+1)] for i in range(int(len(img) / n))]

def least_zeros(imgfile, imgdim1, imgdim2):
    min_zeros = imgdim1 * imgdim2
    ones = 0
    twos = 0
    for layer in read_img(imgfile, imgdim1, imgdim2):
        if layer.count('0') < min_zeros:
            min_zeros = layer.count('0')
            ones = layer.count('1')
            twos = layer.count('2')
    return ones * twos
    
print(least_zeros('input.txt', 25, 6))

def decode_image(imgfile, imgdim1, imgdim2):
    layers = read_img(imgfile, imgdim1, imgdim2)
    message = ''
    n = imgdim1
    for i in range(imgdim1 * imgdim2):
        p = 2
        for j in range(len(layers)):
            if layers[j][i] in ['0', '1']:
                message += layers[j][i]
                break
    for row in [message[n*(i):n*(i+1)] for i in range(int(len(message) / n))]:
        print(row.replace('0', ' ').replace('1', 'e'))

decode_image('input.txt', 25, 6)