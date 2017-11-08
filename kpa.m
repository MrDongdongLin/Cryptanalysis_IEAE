function aimg = kpa(cimg, vD, blk_coeff)
%KPA 此处显示有关此函数的摘要
%   此处显示详细说明

cimg = double(cimg);
[m, n] = size(cimg);
aimg = zeros(m,n);
[r1, r2] = size(vD);
p1=m/r1; p2=n/r2;
bm=r1*ones(1,p1); bn=r2*ones(1,p2);
blk_cimg=mat2cell(cimg, bm, bn);
blk_aimg=mat2cell(aimg, bm, bn);
% coeff = cell2mat(blk_coeff);
% coeff = [zeros(1,r1*r2); coeff(1:end-1,:)];

blk_aimg = reshape(blk_aimg', 1, r1*r2);
for i = 1:r1
    for j = 1:r2
        sb = zeros(r1,r2);
        if i==1 && j==1
            blk_aimg{1,(i-1)*r2+j} = mod(blk_cimg{i,j} - vD{i,j}, 256);
        else
            row = (i-1)*r2+j;
            for x = 1:row-1
                sb = sb + mod(blk_coeff{row, x} * blk_aimg{1, x}, 256);
            end
            blk_aimg{1,(i-1)*r2+j} = mod(blk_cimg{i,j} - vD{i,j} - sb, 256);
        end
    end
end

blk_aimg = reshape(blk_aimg, 16, 16)';

aimg = cell2mat(blk_aimg);
imshow(uint8(mod(aimg,256)));
end