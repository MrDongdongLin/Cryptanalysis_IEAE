import IEAE_ as cipher
from matplotlib import pyplot as plt

if __name__ == '__main__':
    a, b, w1, w2, mu, mu1, mu2, N = 1, 1, 50, 50, 3.999, 20, 15, 3
    lamb = 0.0046121289775
    p1, p2 = 8, 8
    image_path = "../../data/Lena.bmp"
    crypt = cipher.IEAECipher(image_path, p1, p2, a, b, mu, mu1, mu2, lamb)
    _cimage = crypt.encipher(crypt.pimage, p1, p2, crypt.v, crypt.D, crypt.C0)
    _pimage = crypt.decipher(_cimage, p1, p2, crypt.v, crypt.D, crypt.C0)
    # print crypt.pimage.shape
    # print crypt.D.shape
    # print crypt.C0.shape
    # import numpy as np
    # print np.shape(crypt.pimage)
    
    plt.subplot(131)
    plt.imshow(crypt.pimage, 'gray')
    plt.title(r'Lena')

    plt.subplot(132)
    plt.imshow(_cimage, 'gray')
    plt.title(r'Lena_e')

    plt.subplot(133)
    plt.imshow(_pimage, 'gray')
    plt.title(r'Lena_d')

    plt.show()