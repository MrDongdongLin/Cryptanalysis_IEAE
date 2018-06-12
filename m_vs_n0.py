from math import *
import numpy as np
import collections as cl
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib as mpl
from matplotlib import rc
rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
rc('text', usetex=True)

def bicoeff(n, k):
    C=cl.defaultdict(int)
    for row in range(n+1):
        C[row,0]=1
        for col in range(1,k+1):
            if col <= row:
                C[row,col]=C[row-1,col-1]+C[row-1,col]
    return C[n, k]

def PowerOfTen(n):
    res = 0
    for i in range(n+1):
        bico = bicoeff(n, i)
        res = (bico << (3*n - 2*i)) + res

    return res

def OneBitInPowerOfTen(n):
    """
    See https://mrdongdonglin.github.io/power-of-ten-simplify
    """
    ind = []
    oneBit = []
    ind.append(0)
    oneBit.append(1)
    num = 1

    for x in range(1, n):
        num += num << 2
        oneBit.append(sum(map(int, bin(num)[2:])))
        ind.append(x)
    return ind, oneBit

def logg(m):
    return m*log(10, 2)

m, n0 = OneBitInPowerOfTen(51)
lg = [0] + map(ceil, map(logg, np.array(m[1:])))

# plt.style.use('ggplot')
z1 = np.polyfit(m, n0, 1)
p1 = np.poly1d(z1)
yvals=np.polyval(z1, m)

fig = plt.figure()
fig.set_canvas(plt.gcf().canvas)
ax = plt.subplot(111)
ax.tick_params(labelsize=18, colors='black',left='on')

# plot figure
plt.plot(m, n0, '--o', linewidth=2)
plt.plot(m, lg, "--s", linewidth=2)

ax.set_axisbelow(True)
plt.grid(which='both', linewidth=0.02, color='gray')
plt.ylim(0, 170)
plt.yticks([0,20,40,60,80,100,120,140,160,170])
plt.legend(loc = 'upper left',
        labels = [r'$y=n_0$',r'$y=\lceil m \log_2(10) \rceil$'],
        fancybox = True,
        # shadow = True,
        fontsize = 16)
ax.xaxis.set_major_locator(ticker.MultipleLocator(5.00))
ax.xaxis.set_minor_locator(ticker.MultipleLocator(1.00))

font = {'family': 'serif',
        'color':  'black',
        'size': 22}
plt.xlabel(r'$m$', fontdict=font)
plt.ylabel(r'$y$', fontdict=font)

fig.savefig("m_vs_n0.pdf", bbox_inches='tight', pad_inches = 0)
plt.show()
# plt.close()