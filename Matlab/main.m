%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%% Set Up Parameters %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
clear, clc;
global infinity numf;
infinity = 10^9;

mydir  = pwd;
idcs   = strfind(mydir,filesep);
newdir = mydir(1:idcs(end)-1);

filename = strcat(newdir, '\data-swap-big.xlsx');
[numf, numg, FP, S, SE, alpha, capacity] = getdata(filename);

% Club Ranking: uniformly random
clubrank = randperm(numf); % family: index - val : score

% Generate ranking based on size first then club rank
scrank = genSizePointRank(clubrank, S, numf);

% Number of seats needed for each family size
%alpha = [10 11 12 14 15];

%%%%%%%%%%%%%%%%%%%%%%%%%%% Multiple Games %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%

frac = 0.5;
[matchrank6, proposed, C] = greedyMultipleGames(1, numf, numg, clubrank, scrank, FP, S, capacity, frac, alpha);

[matchsize6, proposed, C] = greedyMultipleGames(2, numf, numg, clubrank, scrank, FP, S, capacity, frac, alpha);

[matchhybrid1, proposed, C] = greedyMultipleGames(3, numf, numg, clubrank, scrank, FP, S, capacity, 0.25, alpha);

[matchhybrid2, proposed, C] = greedyMultipleGames(3, numf, numg, clubrank, scrank, FP, S, capacity, 0.5, alpha);

[matchhybrid3, proposed, C] = greedyMultipleGames(3, numf, numg, clubrank, scrank, FP, S, capacity, 0.75, alpha);


%% 
matching(:, 1:numg) = matchrank6;
matching(:, (1*numg+1):(2*numg)) = matchsize6;
matching(:, (2*numg+1):(3*numg)) = matchhybrid1;
matching(:, (3*numg+1):(4*numg)) = matchhybrid2;
matching(:, (4*numg+1):(5*numg)) = matchhybrid3;

%% Statistics multiple games

matchedfams = numMatchedFamilies(matching);
matchedseats = numMatchedSeats(matching, S);
matchedsizes = countTypes(matching, S);

% Average
matchedfams_avg = zeros(1, 5);
matchedseats_avg = zeros(1, 5);
matchedsizes_avg = zeros(5, 5);
numgMatched = zeros(numg, 5);
numgMatchedPeople = zeros(numg, 5);
for i = 1:5
    si = 1+(i-1)*numg;
    ei = i * numg;
    matchedfams_avg(i) = round(mean(matchedfams(si:ei)));
    matchedseats_avg(i) = round(mean(matchedseats(si:ei)));
    matchedsizes_avg(:, i) = round(mean(matchedsizes(:, si:ei), 2));
    numgMatched(:, i) = countMatchedGames(matching(:, si:ei));
    numgMatchedPeople(:, i) = countMatchedGamesPeople(matching(:, si:ei), S);
end

% Preferences
firstchoicefam = zeros(numg, 5);
firstchoiceppl = zeros(numg, 5);
avg_matchedpref = zeros(1, 5);
preffam = zeros(numg, 5);
prefppl = zeros(numg, 5);
for i = 1:5
    si = 1+(i-1)*numg;
    ei = i * numg;
    currmatch = matching(:, si:ei);
    firstchoicefam(:, i) = countBestChoiceFamily(currmatch, FP);
    firstchoiceppl(:, i) = countBestChoicePeople(currmatch, FP, S);
    avg_matchedpref(i) = averegeMatchedPref(currmatch, FP);
    preffam(:, i) = countPrefFamily(currmatch, FP);
    prefppl(:, i) = countPrefPeople(currmatch, FP, S);
end




%% Save to file

% Export Statistics
filename = strcat(newdir, '\new-outputs-',int2str(numf), '-families-', int2str(numg), '-games.xlsx');

%t = xlsread(filename);
%if ~isempty(t)
%    xlswrite(filename,zeros(size(t))*nan);
%end

sheet = 1;

xlRange = 'A1';
xlswrite(filename, {'Family'}, sheet, xlRange);
xlRange = 'A3';
temp = (1:numf)';
xlswrite(filename, temp, sheet, xlRange);

xlRange = 'B1';
xlswrite(filename, {'Size'}, sheet, xlRange);

xlRange = 'B3';
xlswrite(filename, S, sheet, xlRange);

xlRange = 'C1';
xlswrite(filename, {'Club rank'}, sheet, xlRange);

xlRange = 'C3';
xlswrite(filename, clubrank', sheet, xlRange);

xlRange = 'D1';
xlswrite(filename, {'Alg 1'}, sheet, xlRange);

xlRange = 'D2:I2';
xlswrite(filename, [{'G 1'}, {'G 2'} , {'G 3'}, {'G 4'}, {'G 5'}, {'G 6'}], sheet, xlRange);

xlRange = 'D3';
xlswrite(filename, int16(matchrank6), sheet, xlRange);

xlRange = 'K1';
xlswrite(filename, {'Alg 2'}, sheet, xlRange);

xlRange = 'K2:P2';
xlswrite(filename, [{'G 1'}, {'G 2'} , {'G 3'}, {'G 4'}, {'G 5'}, {'G 6'}], sheet, xlRange);

xlRange = 'K3';
xlswrite(filename, int16(matchsize6), sheet, xlRange);

xlRange = 'R1';
xlswrite(filename, {'Hybrid 0.25'}, sheet, xlRange);
xlRange = 'R2:W2';
xlswrite(filename, [{'G 1'}, {'G 2'} , {'G 3'}, {'G 4'}, {'G 5'}, {'G 6'}], sheet, xlRange);
xlRange = 'R3';
xlswrite(filename, int16(matchhybrid1), sheet, xlRange);

xlRange = 'Y1';
xlswrite(filename, {'Hybrid 0.5'}, sheet, xlRange);
xlRange = 'Y2:AD2';
xlswrite(filename, [{'G 1'}, {'G 2'} , {'G 3'}, {'G 4'}, {'G 5'}, {'G 6'}], sheet, xlRange);
xlRange = 'Y3';
xlswrite(filename, int16(matchhybrid2), sheet, xlRange);

xlRange = 'AF1';
xlswrite(filename, {'Hybrid 0.75'}, sheet, xlRange);
xlRange = 'AF2:AK2';
xlswrite(filename, [{'G 1'}, {'G 2'} , {'G 3'}, {'G 4'}, {'G 5'}, {'G 6'}], sheet, xlRange);
xlRange = 'AF3';
xlswrite(filename, int16(matchhybrid3), sheet, xlRange);

% Fam Preference
sheet = 2;
xlRange = 'A1';
xlswrite(filename, {'Family Preference'}, sheet, xlRange);

xlRange = 'A2';
xlswrite(filename, FP, sheet, xlRange);


% Statistics
sheet = 3;
xlRange = 'A1';
xlswrite(filename, {'Statistics'}, sheet, xlRange);
xlRange = 'A3';
xlswrite(filename, {'Number of matched families'}, sheet, xlRange);
xlRange = 'A4';
xlswrite(filename, {'Number of matched people'}, sheet, xlRange);


xlRange = 'A6';
xlswrite(filename, {'Size 1'}, sheet, xlRange);
xlRange = 'A7';
xlswrite(filename, {'Size 2'}, sheet, xlRange);
xlRange = 'A8';
xlswrite(filename, {'Size 3'}, sheet, xlRange);
xlRange = 'A9';
xlswrite(filename, {'Size 4'}, sheet, xlRange);
xlRange = 'A10';
xlswrite(filename, {'Size 5'}, sheet, xlRange);

xlRange = 'D3';
xlswrite(filename, matchedfams, sheet, xlRange);

xlRange = 'D4';
xlswrite(filename, matchedseats, sheet, xlRange);

xlRange = 'D6';
xlswrite(filename, matchedsizes, sheet, xlRange);

% Average
xlRange = 'A13';
xlswrite(filename, [{'Average'}, {''} , {''}, {'Alg1'}, {'Alg2'}, {'Hybrid 0.25'}, {'Hybrid 0.5'}, {'Hybrid 0.75'}], sheet, xlRange);

xlRange = 'A14';
xlswrite(filename, [{'Matched familes'}; {'Matched people'} ; {}; {'Size 1'}; {'Size 2'}; {'Size 3'}; {'Size 4'}; {'Size 5'}], sheet, xlRange);

xlRange = 'D14';
xlswrite(filename, matchedfams_avg, sheet, xlRange);


xlRange = 'D15';
xlswrite(filename, matchedseats_avg, sheet, xlRange);

xlRange = 'D16';
xlswrite(filename, matchedsizes_avg, sheet, xlRange);

xlRange = 'A22';
xlswrite(filename, {'number of families get i games'}, sheet, xlRange);
xlRange = 'A23';
xlswrite(filename, [{'1 games'}; {'2 games'} ; {'3 games'}; {'4 games'}; {'5 games'}; {'6 games'}], sheet, xlRange);
xlRange = 'D23';
xlswrite(filename, numgMatched, sheet, xlRange);

xlRange = 'A31';
xlswrite(filename, {'number of people get i games'}, sheet, xlRange);
xlRange = 'A32';
xlswrite(filename, [{'1 games'}; {'2 games'} ; {'3 games'}; {'4 games'}; {'5 games'}; {'6 games'}], sheet, xlRange);
xlRange = 'D32';
xlswrite(filename, numgMatchedPeople, sheet, xlRange);

sheet = 4;
xlRange = 'A1';
xlswrite(filename, [{'Best matched'}, {''} , {''}, {'Alg1'}, {'Alg2'}, {'Hybrid 0.25'}, {'Hybrid 0.5'}, {'Hybrid 0.75'}], sheet, xlRange);

xlRange = 'A2';
xlswrite(filename, [{'Family'}; {'1 games'}; {'2 games'} ; {'3 games'}; {'4 games'}; {'5 games'}; {'6 games'}], sheet, xlRange);

xlRange = 'D3';
xlswrite(filename, firstchoicefam , sheet, xlRange); 

xlRange = 'A10';
xlswrite(filename, [{'People'};{'1 games'}; {'2 games'} ; {'3 games'}; {'4 games'}; {'5 games'}; {'6 games'}], sheet, xlRange);
xlRange = 'D11';
xlswrite(filename, firstchoiceppl , sheet, xlRange);

xlRange = 'A18';
xlswrite(filename, [{'Family'}; {'1 choice'}; {'2 choice'} ; {'3 choice'}; {'4 choice'}; {'5 choice'}; {'6 choice'}], sheet, xlRange);

xlRange = 'D19';
xlswrite(filename, preffam , sheet, xlRange); 

xlRange = 'A27';
xlswrite(filename, [{'People'};{'1 choice'}; {'2 choice'} ; {'3 choice'}; {'4 choice'}; {'5 choice'}; {'6 choice'}], sheet, xlRange);
xlRange = 'D28';
xlswrite(filename, prefppl , sheet, xlRange);


xlRange = 'A36';
xlswrite(filename, {'Average matched rank'}, sheet, xlRange);

xlRange = 'D36';
xlswrite(filename, round(avg_matchedpref, 2), sheet, xlRange);
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%% Preferences %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function count = countMatchedGames(match)
    [nf, ng] = size(match);
    match = sum(match, 2);
    
    count = zeros(1, ng);
    for f = 1:nf
        if (match(f) > 0)
            count(match(f)) = count(match(f)) + 1;
        end
    end
end

function count = countMatchedGamesPeople(match,S)
    [nf, ng] = size(match);
    match = sum(match, 2);
    
    count = zeros(1, ng);
    for f = 1:nf
        if (match(f) > 0)
            count(match(f)) = count(match(f)) + S(f);
        end
    end
end

function val = averegeMatchedPref(match, FP)
    count = sum(sum(match));
    val = sum(sum(FP(match)))/count;
end
function count = countPrefFamily(match, FP)
    [m, n] = size(match);
    count = zeros(1, n);
   
    for f = 1:m
        for g = 1:n
            if match(f,g)
                p = FP(f,g);
                count(p) = count(p) + 1;
            end
        end
    end
end

function count = countPrefPeople(match, FP, S)
    [m, n] = size(match);
    count = zeros(1, n);
   
    for f = 1:m
        for g = 1:n
            if match(f,g)
                p = FP(f,g);
                count(p) = count(p) + S(f);
            end
        end
    end
end

function count = countBestChoiceFamily(match, FP)
    [m,n] = size(match);
    count = zeros(1, n);
    for f = 1: m
        ind = match(f,:);
        val = min(FP(f, ind));
        if ~isempty(val)
            if (val >=1 && val <= n)
                count(val) = count(val) + 1;
            end
        end
    end
end

function count = countBestChoicePeople(match, FP, S)
    [m,n] = size(match);
    count = zeros(1, n);
    for f = 1: m
        ind = match(f,:);
        val = min(FP(f, ind));
        if ~isempty(val)
            if (val >=1 && val <= n)
                count(val) = count(val) + S(f);
            end
        end
    end
end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%
function [match, proposed, cap] = greedyMultipleGames(alg, numf, numg, clubrank, scrank, FP, S, C, frac, alpha)
match = false(numf, numg);
proposed = false(numf, numg);
    
cap = C * ones(1,numg);
outerloop = 1;    
while true
    fprintf('============ Outerloop = %d =================\n', outerloop);
    round = 1;
    proposers = true(numf,1);
    tempMatch = false(numf, numg);
    matchrank = zeros(numf, 1);
    
    while true
        fprintf("++++ Round = %d\n", round);
        [currP, proposed] = familyPropose(proposed, FP, proposers);
        fprintf('total proposers: %d\n', sum(sum(currP >= 1)));
        for g = 1:numg
            proposers = (currP == g);
            fprintf("%d families proposing to family %d\n", sum(proposers), g);
            if any(proposers)
                if (alg == 1)
                    temp = greedyRanking(proposers, clubrank, S, cap(g), alpha);
                elseif (alg == 2)
                    temp = greedySizeRank(proposers, scrank, S, cap(g), alpha);
                else % alg == 3
                    matchr = greedyRanking(proposers, clubrank, S, cap(g), alpha);
                    matchs = greedySizeRank(proposers, scrank, S, cap(g), alpha);

                    temp = greedyHybrid(matchr,matchs,clubrank,scrank,S,cap(g),frac,alpha);
                end
                fprintf('     %d accepted ', sum(temp));
                tempMatch(:, g) = tempMatch(:, g) | temp; 
                
                % Store the rank of matched families
                matchrank(temp) = round;
                
                % Update capacity
                seats = getUsedCapacity(temp, S, alpha);
                fprintf("using %d seats\n", seats)
                cap(g) = cap(g) - seats;
            end 
        end
        
        matched = any(tempMatch, 2);
        proposers = ~matched;
        fprintf("Matched %d families\n", sum(sum(tempMatch)));

        if all(matched) || all(all(proposed(~matched, :)))
            break;
        end
        
        % Update Club Score
        %[clubrank, scrank] = updateClubRank(clubrank, matchrank, S, numf, numg);
        
        round = round + 1;
    end
    
    % Aggregate 
    match = match | tempMatch;
    
    outerloop = outerloop + 1;
    
    if all(all(proposed))
        break;
    end
end
    
end

function [currP, proposed] = familyPropose(proposed, FP, proposers)
    global infinity numf;
    FP(proposed) = infinity;
    
    [~, currP] = min(FP, [], 2);
    currP(currP == infinity) = 0;
    currP(~proposers) = 0;
    
    for f = 1:numf
        if currP(f)
            proposed(f,currP(f)) = true;
        end
    end
end

% Modify the Club point ranking of the families, so that all the families 
% that assigned to the low ranked games are now on top.
function [clubrank, scrank] = updateClubRank(clubrank, matchrank, S, numf, numg)
    fprintf('Updating clubrank \n');
    offset = max(clubrank) + 1;
    
    for f = 1:length(clubrank)
        if (matchrank(f) >= 1)
            clubrank(f) = clubrank(f) + (numg - matchrank(f))* offset;
        end
    end
    
    scrank = genSizePointRank(clubrank, S, numf);
    
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function scrank = genSizePointRank(clubrank, S, numf)
    scrank = zeros(1, numf);
    for i = 1:numf
        scrank(i) = (5 - S(i)) * (numf + 1) + clubrank(i);
    end
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%% Functions for Statistics %%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function  val = numMatchedFamilies(match)
    val = sum(match);
end

function val = numMatchedSeats(match, S)
    S = S';
    [~, n] = size(match);
    val = zeros(1, n);
    for i = 1:n
        val(i) = sum(S(match(:, i)));
    end
end

function count = countTypes(match, S)
    S = S';
    [~, n] = size(match);
    count = zeros(5,n);
    
    for k = 1:n
        temp = S(match(:, k));
        for i = 1: 5
            count(i,k) = length(find(temp == i));
        end
    end
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function v = swap(v, i ,j)
    temp = v(i);
    v(i) = v(j);
    v(j) = temp;
end


function saveToFileOne(filename)
%% Export to excel file
sheet = 1;
xlRange = 'A1';
xlswrite(filename, {'Family'}, sheet, xlRange);
xlRange = 'A2:A10001';
temp = (1:numf)';
xlswrite(filename, temp, sheet, xlRange);

xlRange = 'B1';
xlswrite(filename, {'Size'}, sheet, xlRange);

xlRange = 'B2:B10001';
xlswrite(filename, S', sheet, xlRange);

xlRange = 'C1';
xlswrite(filename, {'Club rank'}, sheet, xlRange);

xlRange = 'C2:C10001';
xlswrite(filename, clubrank', sheet, xlRange);

xlRange = 'D1';
xlswrite(filename, {'Alg 1'}, sheet, xlRange);

xlRange = 'D2:D10001';
xlswrite(filename, int16(matchrank), sheet, xlRange);

xlRange = 'E1';
xlswrite(filename, {'Alg 2'}, sheet, xlRange);

xlRange = 'E2:E10001';
xlswrite(filename, int16(matchsize), sheet, xlRange);

xlRange = 'F1';
xlswrite(filename, {'Hybrid 0.25'}, sheet, xlRange);
xlRange = 'G1';
xlswrite(filename, {'Hybrid 0.5'}, sheet, xlRange);
xlRange = 'H1';
xlswrite(filename, {'Hybrid 0.75'}, sheet, xlRange);

xlRange = 'F2:H10001';
xlswrite(filename, int16(matchhybrid'), sheet, xlRange);

% Export Statistics
sheet = 2;
xlRange = 'A1';
xlswrite(filename, {'Statistics'}, sheet, xlRange);
xlRange = 'A2';
xlswrite(filename, {'Number of matched families'}, sheet, xlRange);
xlRange = 'A3';
xlswrite(filename, {'Number of matched people'}, sheet, xlRange);

xlRange = 'D1';
xlswrite(filename, {'Alg 1'}, sheet, xlRange);
xlRange = 'D2';
xlswrite(filename, matchedfamiliesrank, sheet, xlRange);
xlRange = 'D3';
xlswrite(filename, matchedseatsrank, sheet, xlRange);

xlRange = 'E1';
xlswrite(filename, {'Alg 2'}, sheet, xlRange);
xlRange = 'E2';
xlswrite(filename, matchedfamiliessize, sheet, xlRange);
xlRange = 'E3';
xlswrite(filename, matchedseatssize, sheet, xlRange);

xlRange = 'F1';
xlswrite(filename, {'Hybrid 0.25'}, sheet, xlRange);
xlRange = 'G1';
xlswrite(filename, {'Hybrid 0.5'}, sheet, xlRange);
xlRange = 'H1';
xlswrite(filename, {'Hybrid 0.75'}, sheet, xlRange);
xlRange = 'F2:H2';
xlswrite(filename, matchedfamilieshybrid, sheet, xlRange);
xlRange = 'F3:H3';
xlswrite(filename, matchedseatshybrid, sheet, xlRange);


xlRange = 'A5';
xlswrite(filename, {'Size 1'}, sheet, xlRange);
xlRange = 'A6';
xlswrite(filename, {'Size 2'}, sheet, xlRange);
xlRange = 'A7';
xlswrite(filename, {'Size 3'}, sheet, xlRange);
xlRange = 'A8';
xlswrite(filename, {'Size 4'}, sheet, xlRange);
xlRange = 'A9';
xlswrite(filename, {'Size 5'}, sheet, xlRange);

xlRange = 'D5:D9';
xlswrite(filename, typesrank', sheet, xlRange);
xlRange = 'E5:E9';
xlswrite(filename, typessize', sheet, xlRange);

xlRange = 'F5:H9';
xlswrite(filename, typeshybrid', sheet, xlRange);



end
