function envy = countenvy(brank, S)
    nF = length(S);
    envy = zeros(nF, 1);
    
    for i=1:nF
        maxdiff = 0;
        for j=1:nF
            if (i~=j) && (S(i) == S(j)) && (brank(i)> brank(j))
                currdiff = brank(i) - brank(j);
                
				if (maxdiff < currdiff)
                    maxdiff = currdiff;
                end
            end
        end
		envy(i) = maxdiff;   
    end
end