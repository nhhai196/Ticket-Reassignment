%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%% Greedy based on rannking %%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function match = greedyRanking(proposers, clubscore, S, C, alpha)
    global infinity;    
    numfams = length(S);
    match = false(numfams, 1);
    
    clubscore(~proposers) = infinity;
    assignedseats = 0; 

    while true
        [val, f] = min(clubscore);
        if (val == infinity)
            break;
        end
        temp = assignedseats + alpha(S(f));
        if (temp <= C)
            clubscore(f) = infinity;
            match(f) = true;
            assignedseats = temp;
        else
            break;
        end
    end 
end