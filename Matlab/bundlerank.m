function [brank, bwrank, avg, avgwrank, count, countbyp] = bundlerank(match, BR, famsize, alpha)
    [numf, ~] = size(match);
    brank = zeros(numf, 1);
    [~, numb] = size(BR);
    
    bwrank = zeros(sum(famsize), 1);
    
    for f = 1:numf 
        b = match(f,:);
        if any(b)
            bundle = vector2bundle(b, alpha(famsize(f)));
            brank(f) = findrank(bundle, BR(f, :));
        end
    end
    
    avg = round(mean(brank(brank > 0)), 1);
    
    ind = 1;
    for f = 1:numf
        %s = s +  brank(f) * famsize(f);
        for j = 1:famsize(f)
            bwrank(ind) = brank(f);
            ind = ind + 1;
        end
    end
    avgwrank = mean(bwrank); %s/sum(famsize);

    brank(brank == 0) = numb + 1;
    % count by rank
    count = zeros(1, numb+1);
    countbyp = zeros(1, numb+1);
    for f = 1:numf
        count(brank(f)) = count(brank(f)) + 1;
        countbyp(brank(f)) = countbyp(brank(f)) + famsize(f);
    end
    
    % count number of unmatched
    count(numb+1) = numf - sum(count(1:numb));
end

function bundle = vector2bundle(v, fsize)
    numg = length(v);
    bundle = '';
        
    for i = 1:numg
        if v(i)
            bundle = strcat(bundle, int2str(fsize), ',');
        else
            bundle = strcat(bundle, '0', ',');
        end
    end
    % remove the comma at the end
    bundle(length(bundle)) = [];
end


function r = findrank(bundle, bundlelist)
    r = 1;
    for i = 1:length(bundlelist)
        if strcmp(bundle, bundlelist(i))
            r = i;
            break;
        end
    end
end