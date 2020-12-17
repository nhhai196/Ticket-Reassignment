% A more natural way of generating data


function lop = genpreferences(numpref, numg)
lop = zeros(numpref, numg);
for i = 1:numpref
    lop = randomper(numg);
    
end

end