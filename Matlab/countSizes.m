function count = countSizes(match, S)
    S = S';
    [~, n] = size(match);
    count = zeros(6,n);
    
    for k = 1:n
        temp = S(match(:, k));
        for i = 1:6
            count(i,k) = length(find(temp == i));
        end
    end
end