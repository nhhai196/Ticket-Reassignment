%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Hybrid %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function match = greedyHybrid(matchr,matchs,clubscore,secondscore,S,C,frac,alpha)
    global infinity;
    match = matchr & matchs;
    %fprintf("Size of intersection is %d\n", sum(match));
    b = xor(matchr, match);
    c = xor(matchs, match);
    
    numf = floor(frac * sum(b));
    
    scores = clubscore(b);
    
    % Take alpha fraction
    for i = 1:numf
        [val, ind] = min(scores);
        scores(ind) = infinity;
        match(clubscore == val) = true; % This requires uniqueness
    end

    
    % 
    newC = C - getUsedCapacity(match, S, alpha);
    %secondscore(~c) = infinity;
    
    temp = greedySizeRank(c, secondscore, S, newC, alpha);
    
    match = temp | match; 
    
end

