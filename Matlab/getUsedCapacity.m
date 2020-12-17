function val = getUsedCapacity(match, S, alpha)
    val = 0;
    for i = 1: length(match)
        if match(i)
            val = val + alpha(S(i));
        end
    end
end