%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%% Greedy based on family size first then rank %%%%%%%%%%%
function match = greedySizeRank(proposers, secondscore, S, C, alpha)
    global infinity;
    numfams = length(S);
    match = false(numfams,1);
    
    secondscore(~proposers) = infinity;
    
    assignedseats = 0; 

    while true
        [val, f] = min(secondscore);
        if (val == infinity)
            break;
        end
        
        temp = assignedseats + alpha(S(f));
        if (temp <= C)
            secondscore(f) = infinity;
            match(f) = true;
            assignedseats = assignedseats + alpha(S(f));
        else
            break;
        end
    end 
end

% A function to rank families based on family size first then club rank
% function [newscore, newrank] = sizeClubRank(clubscore, numtypes)
%     len = length(clubscore);
%     newrank = int16(zeros(1, len));
%     starti = 1;
%     endi= numtypes(1);
%     
%     for i = 1:5
%         [~, temp] = sort(clubscore(starti:endi), 'descend');
%         
%         newrank(starti:endi) = (starti - 1) + int16(temp);
%         
%         if (i < 5)
%             starti = starti + numtypes(i); 
%             endi = endi + numtypes(i+1);  
%         end
%     end
%     
%     newrank = flip(newrank);
%     newscore = zeros(1, len);
%     for i = 1:len
%         f = newrank(i);
%         newscore(f) = i;
%     end
% end