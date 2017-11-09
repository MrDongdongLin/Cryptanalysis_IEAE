# Cryptanalyzing an image encryption algorithm based on autoblocking and electrocardiography

Codes of cryptanalysis of image encryption algorithm based on autoblocking and electrocardiography (IEAE), more info about the paper can be found [here](https://arxiv.org/abs/1711.01858).

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