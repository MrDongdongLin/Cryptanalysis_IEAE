import numpy as np

class IEAECipher(object):
    def __init__(self, image_path, p1=8, p2=8, a=1, b=1, 
                 mu=3.999, mu1=20, mu2=15, lamb=0.0046121289775):
        import cv2
        # Initial state of Arnold map and Logistic map
        _x0 = np.abs(lamb)
        _y0 = np.abs(lamb) * np.power(10,5) - np.floor(np.abs(lamb) * np.power(10,5))
        _x = np.abs(lamb) * np.power(10,8) - np.floor(np.abs(lamb) * np.power(10,8))
        
        # Read an image with OpenCV
        _image = cv2.imread(image_path, 0)
        _A = np.mat(_image)
        _m, _n = np.shape(_A)
        _r1, _r2 = _m/p1, _n/p2

        # Length of the generated sequences
        _slen = _m*_n+256
        _sx, _sy, _sxx = self._rand_str_gen(_x0, _y0, _x, _slen, a, b, mu)

        # Control parameter $r$ and $v$ and psedorandom matrix D
        _r, _v = _sxx[mu1], _sxx[mu2]
        _sD = []
        for i in xrange(0, _m*_n/2):
            _sD.append(_sx[_r+1+i])
            _sD.append(_sy[_r+1+i])
        _DMatrix = np.array(_sD).reshape(_m, _n)
        _D = np.mat(_DMatrix)

        # Psedorandom matrix C0
        _C0 = self._get_matrix_c(_A, _sxx, p1, p2, _r1, _r2)

        # Member variables
        self.pimage = _image
        self.cimage = []
        self.v = _v
        self.D = _D
        self.C0 = _C0

    def encipher(self, pimage, p1, p2):
        m, n = np.shape(pimage)
        r1, r2 = m/p1, n/p2
        cimage = np.zeros((m, n))
        for i in xrange(0, r1):
            for j in xrange(0, r2):
                if i+j == 0:
                    cimage[0:p1,0:p2] = (pimage[0:p1,0:p2] + self.v*self.D[0:p1,0:p2] + self.C0) % 256
                elif i+j == r1+r2-2:
                    cimage[i*p1:m,j*p2:n] = (pimage[i*p1:m,j*p2:n] + cimage[i*p1:m,(j-1)*p2:n-p2]) % 256
                elif j == 0:
                    cimage[i*p1:(i+1)*p1,j*p2:(j+1)*p2] = (pimage[i*p1:(i+1)*p1,j*p2:(j+1)*p2] + \
                    self.v*self.D[i*p1:(i+1)*p1,j*p2:(j+1)*p2] + cimage[(i-1)*p1:i*p1,(r2-1)*p2:r2*p2]) % 256
                else:
                    cimage[i*p1:(i+1)*p1,j*p2:(j+1)*p2] = (pimage[i*p1:(i+1)*p1,j*p2:(j+1)*p2] + \
                    self.v*self.D[i*p1:(i+1)*p1,j*p2:(j+1)*p2] + cimage[i*p1:(i+1)*p1,(j-1)*p2:j*p2]) % 256
        return cimage

    def decipher(self, cimage, p1, p2):
        m, n = np.shape(cimage)
        r1, r2 = m/p1, n/p2
        pimage = np.zeros((m, n))
        for i in xrange(0, r1):
            for j in xrange(0, r2):
                if i+j == 0:
                    pimage[0:p1,0:p2] = (cimage[0:p1,0:p2] - self.v*self.D[0:p1,0:p2] - self.C0) % 256
                elif i+j == r1+r2-2:
                    pimage[i*p1:m,j*p2:n] = (cimage[i*p1:m,j*p2:n] - cimage[i*p1:m,(j-1)*p2:n-p2]) % 256
                elif j == 0:
                    pimage[i*p1:(i+1)*p1,j*p2:(j+1)*p2] = (cimage[i*p1:(i+1)*p1,j*p2:(j+1)*p2] - \
                    self.v*self.D[i*p1:(i+1)*p1,j*p2:(j+1)*p2] - cimage[(i-1)*p1:i*p1,(r2-1)*p2:r2*p2]) % 256
                else:
                    pimage[i*p1:(i+1)*p1,j*p2:(j+1)*p2] = (cimage[i*p1:(i+1)*p1,j*p2:(j+1)*p2] - \
                    self.v*self.D[i*p1:(i+1)*p1,j*p2:(j+1)*p2] - cimage[i*p1:(i+1)*p1,(j-1)*p2:j*p2]) % 256
        return pimage

    def _rand_str_gen(self, x0, y0, x0_, n, a=1, b=1, mu=3.999):
        sx, sy, sx_ = [], [], []
        sx.append(self._arnold_map_x(a, x0, y0))
        sy.append(self._arnold_map_y(a, b, x0, y0))
        sx_.append(self._logistic_map(x0_, mu))
        for i in range(1, n):
            sx.append(self._arnold_map_x(a, sx[i-1], sy[i-1]))
            sy.append(self._arnold_map_y(a, b, sx[i-1], sy[i-1]))
            sx_.append(self._logistic_map(sx_[i-1], mu))
        sx = map(np.uint8, map(lambda s: np.floor(s*np.power(10,14))%256, sx))
        sy = map(np.uint8, map(lambda s: np.floor(s*np.power(10,14))%256, sy))
        sx_ = map(np.uint8, map(lambda s: np.floor(s*np.power(10,14))%256, sx_))
        return sx, sy, sx_

    def _get_matrix_c(self, A, sxx, p1, p2, r1, r2):
        mu3 = np.sum(A[(r1-1)*p1-1:r1*p1-1,(r2-1)*p2-1:r2*p2-1])%256+1
        sC0 = []
        for i in xrange(mu3, (p1*p2)+mu3):
            sC0.append(sxx[i])
        C0 = np.mat(np.array(sC0).reshape(p1, p2))
        return C0

    def _arnold_map_x(self, a, x0, y0):
        return (x0+a*y0)%1

    def _arnold_map_y(self, a, b, x0, y0):
        return (b*x0+(1+a*b)*y0)%1

    def _logistic_map(self, x0, mu):
        return mu*x0*(1-x0)

class Cryptanalysis(object):
    def __init__(self, pimage, cimage, p1, p2, rounds):
        _m, _n = np.shape(pimage)
        self.pimage = pimage
        self.cimage = cimage
        self.rounds = rounds
        self.m = _m
        self.n = _n

    def _get_coeff(self):
        coeff = np.tri(self.m)
        for j in xrange(0, self.rounds-1):
            for i in xrange(1, len(coeff[0]+1)):
                coeff[i] += coeff[i-1]
        return coeff

    def _get_vd(self, pimage, cimage, coeff, p1, p2, r1, r2):
        raise NotImplementedError

    def known_plaintext_attack(self, cimage, v, D, coeff):
        raise NotImplementedError