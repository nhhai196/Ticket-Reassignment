
function [numf, numg, FP, S, SE, alpha, capacity, BR] = getdata(filename)
    M = xlsread(filename);
    
    %display(M);
    
    [numf, n] = size(M);
    numg = n - 6;
    
    % bundle rank
    [~, ~, BR] = xlsread(filename);
    [~, n] = size(BR);
    BR = BR(2:numf+1, numg+6:n);
    
    
    [~, tFP] = sort(M(:, 1:numg), 2, 'descend');
    FP = zeros(size(tFP));
    for f = 1: numf
        for g = 1:numg
            FP(f, tFP(f, g)) = g;
        end
    end
    S = M(:, numg + 2);
    display(S)
    SE = M(:, numg+4);
    
    
    sheet = 3;
    N = xlsread(filename, sheet);
    capacity = N(1);
    alpha = N(1, 2:length(N));

end