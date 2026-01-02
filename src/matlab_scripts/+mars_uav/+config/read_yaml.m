function data = read_yaml(file_path)
%READ_YAML Legge un file YAML con il supporto MATLAB disponibile.

if nargin < 1 || isempty(file_path)
    error('read_yaml:MissingPath', 'Percorso file YAML richiesto.');
end

if exist('readstruct', 'file') == 2
    try
        data = readstruct(file_path, "FileType", "yaml", "TextType", "char");
        return;
    catch
    end
end

if exist('yamlread', 'file') == 2
    data = yamlread(file_path);
    return;
end

data = simple_yaml_parse(file_path);
end

function data = simple_yaml_parse(file_path)
lines = readlines(file_path);
data = struct();

current_path = {};
prev_level = 0;
last_key = '';

for i = 1:numel(lines)
    line = char(lines(i));
    line = strip_comments(line);
    if isempty(strtrim(line))
        continue;
    end

    indent = length(line) - length(strtrim(line));
    level = indent / 2;

    if level < prev_level
        current_path = current_path(1:level);
    elseif level > prev_level
        if ~isempty(last_key)
            current_path = [current_path, {last_key}];
        end
    end

    [key, value, has_value] = parse_key_value(strtrim(line));
    if ~has_value
        value = struct();
    end

    data = set_nested_field(data, current_path, key, value);

    last_key = key;
    prev_level = level;
end
end

function line = strip_comments(line)
idx = strfind(line, '#');
if ~isempty(idx)
    line = line(1:idx(1)-1);
end
line = regexprep(line, '\s+$', '');
end

function [key, value, has_value] = parse_key_value(line)
parts = split(line, ':', 2);
key = strtrim(parts{1});
if numel(parts) < 2
    value = [];
    has_value = false;
    return;
end

raw_value = strtrim(parts{2});
if isempty(raw_value)
    value = [];
    has_value = false;
    return;
end

value = parse_scalar(raw_value);
has_value = true;
end

function value = parse_scalar(text)
text = strtrim(text);
if startsWith(text, '''') && endsWith(text, '''')
    value = text(2:end-1);
    return;
end
if startsWith(text, '\"') && endsWith(text, '\"')
    value = text(2:end-1);
    return;
end

lower_text = lower(text);
if strcmp(lower_text, 'true')
    value = true;
    return;
end
if strcmp(lower_text, 'false')
    value = false;
    return;
end

num = str2double(text);
if ~isnan(num)
    value = num;
    return;
end

value = text;
end

function data = set_nested_field(data, path, key, value)
if isempty(path)
    data.(key) = value;
    return;
end

head = path{1};
if ~isfield(data, head) || ~isstruct(data.(head))
    data.(head) = struct();
end
data.(head) = set_nested_field(data.(head), path(2:end), key, value);
end
