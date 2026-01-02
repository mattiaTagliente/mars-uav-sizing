function print_parameter_table(title_text, params, width)
%PRINT_PARAMETER_TABLE Stampa una tabella parametri formattata.

if nargin < 3 || isempty(width)
    width = 50;
end

fprintf('%s\n', repmat('-', 1, width));
fprintf('%s\n', title_text);
fprintf('%s\n', repmat('-', 1, width));

names = fieldnames(params);
for i = 1:numel(names)
    name = names{i};
    value = params.(name);
    if isnumeric(value) && isscalar(value)
        fprintf('  %-30s %15s\n', name, mars_uav.core.format_number(value, 4));
    else
        fprintf('  %-30s %15s\n', name, string(value));
    end
end

fprintf('%s\n', repmat('-', 1, width));
end
