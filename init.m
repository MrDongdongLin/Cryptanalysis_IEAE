function [ v, D, C0 ] = init(pimg, p1, p2, a, b, mu, mu1, mu2)
%INIT 此处显示有关此函数的摘要
%   此处显示详细说明
% a=1; b=1; w1=50; w2=50; mu=3.999; mu1=20; mu2=15; N=3; p1=16; p2=16;
[x0, y0, x0_] = init_gen();
[M, N] = size(pimg);
r1 = M/p1; r2 = N/p2;
n = M*N+256;
[sx, sy, sx_] = key_gen(a, b, mu, x0, y0, x0_, n);

r = sx_(mu1); v = sx_(mu2);
% D
D = [];
for j = 1:(M*N)/2
    D = [D sx(j+r) sy(j+r)];
end
D = reshape(D, M, N); D = D';
% C0
C0 = [];
mu3 = 226;
% mu3 = mod(sum(sum(pimg((r1-1)*p1+1:r1*p1,(r2-1)*p2+1:r2*p2))),256)+1;
for j = 1:p1*p2
    C0 = [C0 sx_(j+mu3)];
end
C0 = reshape(C0, p1, p2); C0 = C0';

end

function [x0, y0, x0_] = init_gen()
lambda = 0.00461212897750;
x0 = abs(lambda);
y0 = abs(lambda)*10^5 - floor(abs(lambda)*10^5);
x0_ = abs(lambda)*10^8 - floor(abs(lambda)*10^8);
end

function [sx, sy, sx_] = key_gen(a, b, mu, x0, y0, x0_, n)
sx = zeros(1,n); sy = zeros(1,n); sx_ = zeros(1,n);
sx(1) = arnold_map_x(a, b, x0, y0);
sy(1) = arnold_map_y(a, b, x0, y0);
sx_(1) = logistic_map(x0_, mu);
for i = 2:n
    sx(i) = arnold_map_x(a, b, sx(i-1), sy(i-1));
    sy(i) = arnold_map_y(a, b, sx(i-1), sy(i-1));
    sx_(i) = logistic_map(sx_(i-1), mu);
end
sx = mod(floor(sx*10^14),256);
sy = mod(floor(sy*10^14),256);
sx_= mod(floor(sx_*10^14),256);
end

function x = logistic_map(x0, mu)
x = mu*x0*(1-x0);
end

function x = arnold_map_x(a, ~, x0, y0)
x = mod(x0+a*y0,1);
end

function y = arnold_map_y(a, b, x0, y0)
y = mod(b*x0+(1+a*b)*y0,1);
end