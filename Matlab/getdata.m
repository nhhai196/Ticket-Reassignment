
function [numf, numg, FP, S, SE] = getdata(filename)
    M = xlsread(filename);
    %display(M);
    
    [numf, n] = size(M);
    numg = n - 4;
    
    
    FP = M(:, 1:numg);
    S = M(:, numg + 2);
    SE = M(:, numg+4);

end