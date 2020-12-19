
function [numf, numg, FP, S, SE, alpha, capacity] = getdata(filename)
    M = xlsread(filename);
    %display(M);
    
    [numf, n] = size(M);
    numg = n - 4;
    
    
    FP = M(:, 1:numg);
    S = M(:, numg + 2);
    SE = M(:, numg+4);
    
    sheet = 3;
    N = xlsread(filename, sheet);
    capacity = N(1);
    alpha = N(1, 2:length(N));

end