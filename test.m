function coeff = test(m, n, T)
coeff = tril(ones(m, n));
for i = 1:T-1
    for j = 2:n
        coeff(j,:) = coeff(j,:)+coeff(j-1,:);
    end
end
end