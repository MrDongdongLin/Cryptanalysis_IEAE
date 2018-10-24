# Cryptanalyzing an image encryption algorithm based on autoblocking and electrocardiography

The paper "cryptanalysis of image encryption algorithm based on autoblocking and electrocardiography" is now available on IEEE: https://ieeexplore.ieee.org/document/8495009. This project contains codes of this paper, LaTeX source codes of this paper can be downloaded:  https://arxiv.org/abs/1711.01858. Cite this paper:

IEEE format: 

C. Li, D. Lin, J. Lu, F. Hao, "Cryptanalyzing an image encryption algorithm based on autoblocking and electrocardiography,"
IEEE MultiMedia, arXiv:1711.01858, 2018.

```bib
@ARTICLE{Cqli:block:IM18,
  author =       {Chengqing Li and Dongdong Lin and Jinhu L\"u and Feng Hao},
  title =        {Cryptanalyzing an image encryption algorithm based on autoblocking and electrocardiography},
  journal =      {IEEE MultiMedia, arXiv:1711.01858},
  year =         {2018},
  LatexSource =  {https://arxiv.org/abs/1711.01858},
}
```

## Getting Started

The matlab codes are complete and executable. To encrypt a gray scale image, please use `encrypt.m`, and use `decrypt.m` to decrypt a cipher image. The file `get_key.m` is used to get the equivalent version of the secret key of IEAE with a pair of plain image and cipher image. At last, `kpa.m` is used to decipher IEAE.

## Initlization
```matlab
pimg = imread('../../data/Baboon.bmp');
a=1; b=1; w1=50; w2=50; mu=3.999; mu1=20; mu2=15; N=3; p1=16; p2=16;
[v, D, C0] = init(pimg, p1, p2, a, b, mu, mu1, mu2);
```

## Encryption
```matlab
cimg = encrypt(pimg, p1, p2, v, D, C0);
```

## Decryption
```matlab
pimg = decrypt(cimg, p1, p2, v, D, C0)
```

## Known-plaintext Attack
- Encrypt rounds

```matlab
T = 1;
```

- Another cipher image encrypted with the same secret keys.

```matlab
lena = imread('../../data/Lena.bmp');
[lena_e, ~, ~, ~] = encrypt(lena, p1, p2, v, D, C0);
for i =1:T-1
    [lena_e, ~, ~, ~] = encrypt(lena_e, p1, p2, v, D, C0);
end
```

- Get the equivalent version of the secret key

```matlab
[vD, blk_coeff, ~] = get_key(lena, lena_e, p1, p2, T);
```

- attack

```matlab
aimg = kpa(cimg, vD, blk_coeff);
```

## TODO

python codes of IEAE in folder `cipher`