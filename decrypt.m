function pimg = decrypt( cimg, p1, p2, v, D, C0 )
%DECRYPT 此处显示有关此函数的摘要
%   此处显示详细说明

[m, n] = size(cimg);
r1=m/p1; r2=n/p2;
vD = v*D;
bm=r1*ones(1,p1); bn=r2*ones(1,p2);
pimg = zeros(m, n);
blk_pimg=mat2cell(pimg, bm, bn);
blk_cimg=mat2cell(cimg, bm, bn);
blk_vD=mat2cell(vD, bm, bn);
for i=1:r1
    for j=1:r2
        if i==1 && j==1
            blk_pimg{i,j} = mod(blk_cimg{i,j} - blk_vD{i,j} - C0, 256);
        elseif i==r1 && j==r2
            blk_pimg{i,j} = mod(blk_cimg{i,j} - blk_cimg{i,j-1}, 256);
        elseif j==1
            blk_pimg{i,j} = mod(blk_cimg{i,j} - blk_vD{i,j} - blk_cimg{i-1,r2}, 256);
        else
            blk_pimg{i,j} = mod(blk_cimg{i,j} - blk_vD{i,j} - blk_cimg{i,j-1}, 256);
        end
    end
end
pimg = cell2mat(blk_pimg);
% imshow(uint8(pimg));
end

