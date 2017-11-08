function [vD, blk_coeff, blk_pimg] = get_key(pimg, cimg, p1, p2, T)
%UNTITLED 此处显示有关此函数的摘要
%   此处显示详细说明
pimg = double(pimg);
cimg = double(cimg);
[m, n]=size(pimg);
r1=m/p1; r2=n/p2;
coeff = coeffI(r1*r2, r1*r2, T);

bm=r1*ones(1,p1); bn=r2*ones(1,p2);
blk_pimg=mat2cell(pimg, bm, bn);
blk_cimg=mat2cell(cimg, bm, bn);
bm_coeff=ones(1,r1*r2); bn_coeff=ones(1,r1*r2);
blk_coeff=mat2cell(coeff, bm_coeff, bn_coeff);

vD = get_vd(blk_pimg, blk_cimg, blk_coeff, p1, p2, r1, r2);

end

function coeff = coeffI(m, n, T)
coeff = tril(ones(m, n));
for i = 1:T-1
    for j = 2:n
        coeff(j,:) = coeff(j,:)+coeff(j-1,:);
    end
end
end

function vD = get_vd(pimg, cimg, coeff, p1, p2, r1, r2)
m=p1*r1; n=p2*r2;
sA = zeros(1,r1*r2);
b = ones(1,r1*r2);
sA = mat2cell(sA, 1, b);
K = zeros(m, n);
bm=r1*ones(1,p1); bn=r2*ones(1,p2);
blk_key=mat2cell(K, bm, bn);
for i=1:r1*r2
    for j=1:i
        sA{i} = sA{i} + coeff{i,j} * pimg{ceil(j/r1), mod((j-1),r2)+1};
    end
end
for i=1:r1
    for j=1:r2
        blk_key{i,j} = mod(cimg{i,j} - sA{(i-1)*r2+j}, 256);
    end
end
% vD = cell2mat(blk_key);
vD = blk_key;
end