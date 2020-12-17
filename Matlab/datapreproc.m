global infinity;
infinity = 10^8;
numstds = 5383;
maxgsize = 6;
mingsize = 6;

issenior = randomSenior(numstds);
[numg, G] = randomlyGroup(numstds, maxgsize, mingsize);

S = getGroupSizes(numg, G);
numseniors = numSeniors(issenior);

priorityscore = getPriorityScore(numg, G, issenior, S);
filename = strcat('basketball-outputs-',int2str(mingsize), '-', int2str(maxgsize));
[match, cap, C, alpha] = seatAssign(filename, priorityscore, S, numg, maxgsize, issenior, G);

function [match, cap, C, alpha] = seatAssign(fname, priorityscore, S, numg, maxgsize, issenior, G)
    [match(:,1), cap, C, alpha] = greedyOneGame(priorityscore, S, numg, 1, 4, maxgsize);
    [match(:,2), ~, ~, ~] = greedyOneGame(priorityscore, S, numg, 2, 3, maxgsize);
    [match(:,3), ~, ~, ~] = greedyOneGame(priorityscore, S, numg, 2, 4, maxgsize);
    
    nummatchedgroups = zeros(1,3);
    nummatchedstds = zeros(1,3);
    nummatchedseniors = zeros(1,3);
    count = zeros(maxgsize,3);
    for i = 1:3
        nummatchedgroups(1,i) = numMatchedFamilies(match(:,i));
        nummatchedstds(1,i) = numMatchedSeats(match(:,i), S);
        nummatchedseniors(1,i) = numMatchedSeniors(match(:,i), G, issenior);
        count(:,i) = countSizes(match(:, i), S, maxgsize); 
        %nummatchedgroups/numg
        %nummatchedstds/cap
        %nummatchedseniors/numseniors
    end
    
    sheet = 1;
    xlRange = 'A1';
    xlswrite(fname, [{'Statistics'}, {''}, {''}, {'1r & 4s'}, {'2r & 3s'}, {'2r & 4s'}], sheet, xlRange);
    
    xlRange = 'A2';
    xlswrite(fname, {'Number of matched groups'}, sheet, xlRange);
    
    xlRange = 'D2';
    xlswrite(fname, nummatchedgroups, sheet, xlRange);
    
    xlRange = 'A3';
    xlswrite(fname, {'Number of matched students'}, sheet, xlRange); 
    
    xlRange = 'A4';
    xlswrite(fname, {'Number of matched seniors'}, sheet, xlRange); 
    
    xlRange = 'D3';
    xlswrite(fname, nummatchedstds, sheet, xlRange);
    
    xlRange = 'D4';
    xlswrite(fname, nummatchedseniors, sheet, xlRange);
    
    xlRange = 'A5';
    xlswrite(fname, {'Size 1'}, sheet, xlRange); 
    
    xlRange = 'A6';
    xlswrite(fname, {'Size 2'}, sheet, xlRange); 
    
    xlRange = 'A7';
    xlswrite(fname, {'Size 3'}, sheet, xlRange); 
    
    xlRange = 'A8';
    xlswrite(fname, {'Size 4'}, sheet, xlRange); 
    
    xlRange = 'A9';
    xlswrite(fname, {'Size 5'}, sheet, xlRange); 
    
    xlRange = 'A10';
    xlswrite(fname, {'Size 6'}, sheet, xlRange); 
    
    xlRange = 'D5';
    xlswrite(fname, count, sheet, xlRange);
    
end

function [match, cap, C, alpha] = greedyOneGame(priorityscore, S, numg, emptyrows, emptyseats, maxgsize)
    alpha = zeros(1, maxgsize);
    for i = 1:maxgsize
        alpha(i) = i + emptyseats;
    end
    
    A = getSeatData("seat-data.xlsx");
    [covidcap, cap, C]  = getCapacity(A, emptyrows);
    proposers = true(numg, 1);
    
    match = greedyRanking(proposers, priorityscore, S, covidcap, alpha);
end


% Calculate all group sizes
function S = getGroupSizes(numg, G)
    S = zeros(1, numg);
    for i = 1:numg
        S(i) = length(find(G(i,:) > 0));
    end
end

% Get the capacity: start from the back
function [covidcap, cap, C]  = getCapacity(A, emptyrows)
    C = A(1:(emptyrows+1):end, :);
    covidcap = sum(sum(C));
    cap = sum(sum(A));
end

% Read data from file
function A = getSeatData(fname)
    A = xlsread(fname,'B2:L26');
    A(isnan(A)) =0;
end


% Randomly assign 25% of students to be senior
function issenior = randomSenior(numstds)
    issenior = false(1, numstds);
    for i = 1:numstds
        temp = randi(4);
        if (temp == 1)
            issenior(i) = true;
        end
    end
end

% Randomly group students into groups of size 2-6
function [numg, G] = randomlyGroup(numstds, maxgsize, mingsize)
    G = [];
    numg = 0;
    count = 0;
    diff = maxgsize - mingsize + 1;
    while(count < numstds)
        gsize = mingsize - 1 + randi(diff); % group size is at least 2
        numg = numg + 1;
        G(numg, :) = zeros(1, maxgsize);
        for i = 1:gsize
            if ((count + i) <= numstds)
                G(numg, i) = count + i;
            end
        end
        count = count + gsize; 
    end
end

%% Ranking over groups
function priorityscore = getPriorityScore(numg, G, issenior, S)
    priorityscore = zeros(1, numg);
    for i = 1:numg
        priorityscore(i) = groupScore(i, G, issenior, S);
    end
    priorityscore = priorityscore - (min(priorityscore) -1);
end

function score = groupScore(gid, G, issenior, S)
    score = (6 - countSenior(gid, G, issenior)) * 10^5 + (6 - groupSize(gid, S)) * 10^4 + gid;
end


% Get group size of a group 
function val = groupSize(gid, S)
    val = S(gid);
end

% Count the number of seniors in a group
function count = countSenior(gid, G, issenior)
    count = 0;
    g = G(gid, :);
    for i = 1:length(g)
        if g(i) > 0
            if issenior(g(i))
                count = count + 1;
            end
        end
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

function val = numSeniors(issenior)
    val = sum(sum(issenior));
end

function val = numMatchedSeniors(match, G, issenior)
    [numg, ~] = size(G);
    val = 0;
    for i = 1:numg
        if match(i)
            val = val + countSenior(i, G, issenior);
        end
    end
end


function count = countSizes(match, S, maxgsize)
    S = S';
    [~, n] = size(match);
    count = zeros(maxgsize,n);
    
    for k = 1:n
        temp = S(match(:, k));
        for i = 1:maxgsize
            count(i,k) = length(find(temp == i));
        end
    end
end
