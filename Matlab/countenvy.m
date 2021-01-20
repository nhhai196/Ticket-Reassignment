function [envy, numenvy, wenvy] = countenvy(brank, S)
    nF = length(S);
    envy = zeros(nF, 1);
    numenvy = zeros(nF,1);
    wenvy = zeros(nF,1);
    
    for i=1:nF
        maxdiff = 0;
        sum = 0;
        count = 0;
        for j=1:nF
            if (i~=j) && (S(i) == S(j)) && (brank(i)> brank(j))
                currdiff = brank(i) - brank(j);
                numenvy(i) = numenvy(i)+1;
                sum = sum + currdiff;
                
				if (maxdiff < currdiff)
                    maxdiff = currdiff;
                end
            end
            
            if S(i) == S(j)
                count = count + 1;
            end
        end
		envy(i) = maxdiff;
        if count > 1
            wenvy(i) = sum/(count -1);
        end
    end
end