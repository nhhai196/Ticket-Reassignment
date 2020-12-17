
function [S, numgroupsprob] = gendata(numg, numgroup, fsprob, numswaps, mingroupsize, maxgroupsize)

% Family size 
S = (zeros(numgroup, 1));

% Generate family size so that the average is 2.5
%fsprob = [0.2 0.3 0.35 0.1 0.05];
%fsprob = [0.15 0.35 0.3 0.15 0.05];
numgroupsprob = floor(numgroup * fsprob);
len = length(numgroupsprob);
numgroupsprob(len) = numgroup - sum(numgroupsprob(1:len-1));
endi = 0;
sum(numgroupsprob)

for i = 1:5
    starti = endi+1
    endi = endi + numgroupsprob(i)
    S(starti:endi) = i;
end
S

%numppl = sum(S);
seniors = randomSeniors(S);


% Generate family (group) preferences over games
initpref = randperm(numg);
famPref = repmat(initpref, numgroup, 1);

% Randomly permute few pairs
% numswaps = 2; 
for f = 1:numgroup
    if (numswaps > 0)
        num = randi(numswaps);
    
        for r = 1:num
            famPref(f, :) = swap(famPref(f, :), randi(numg), randi(numg));  
        end
    end
end

% Randomly generate group size
groupsize = zeros(numgroup, 1);
for i = 1:numgroup
    groupsize(i) = randi([mingroupsize, maxgroupsize]);
end

% Create family preference
numfam = sum(groupsize);
fp = zeros(numfam,numg);
endi = 0;
fsize = zeros(numfam, 1);
fseniors = zeros(numfam, 1);




for i = 1:numgroup
    starti = endi + 1;
    endi = endi + groupsize(i);
    fp(starti:endi, :) = repmat(famPref(i, :), groupsize(i), 1);
    fsize(starti:endi, :) =repmat(S(i), groupsize(i), 1);
    fseniors(starti:endi, :) =repmat(seniors(i), groupsize(i), 1);
end
numfam
size(fsize)

% Save the result to an excel file
filename = 'data.xlsx';
sheet = 1;
%for i = 1:2
%t = xlsread(filename, i);
%if ~isempty(t)
%    xlswrite(filename,zeros(size(t))*nan);
%end
%end

xlRange = 'A1';
xlswrite(filename, {'Group Preference'}, sheet, xlRange);

xlRange = 'A2';
xlswrite(filename, famPref, sheet, xlRange);

xlRange = 'H1';
xlswrite(filename, {'Family Size'}, sheet, xlRange);

xlRange = 'H2';
xlswrite(filename, S, sheet, xlRange);

xlRange = 'J1';
xlswrite(filename, {'Num Seniors'}, sheet, xlRange);

xlRange = 'J2';
xlswrite(filename, seniors, sheet, xlRange);

xlRange = 'L1';
xlswrite(filename, {'Number of copies'}, sheet, xlRange);

xlRange = 'L2';
xlswrite(filename, groupsize, sheet, xlRange);


%%
sheet = 2;

xlRange = 'A1';
xlswrite(filename, {'Family Preference'}, sheet, xlRange);

xlRange = 'A2';
xlswrite(filename, fp, sheet, xlRange);

xlRange = 'H1';
xlswrite(filename, {'Family Size'}, sheet, xlRange);

xlRange = 'H2';
xlswrite(filename, fsize, sheet, xlRange);

xlRange = 'J1';
xlswrite(filename, {'Num Seniors'}, sheet, xlRange);

xlRange = 'J2';
xlswrite(filename, fseniors, sheet, xlRange);



end

% Randomly assign 25% of students to be senior
function seniors = randomSeniors(S)
    n = length(S);
    seniors = zeros(n, 1);    
    for i = 1:n
        count = 0;
        for j = 1: S(i)
            temp = randi(4);
            if (temp == 1)
                count = count + 1;
            end
        end
        seniors(i) = count;
    end
end

function v = swap(v, i ,j)
    temp = v(i);
    v(i) = v(j);
    v(j) = temp;
end



