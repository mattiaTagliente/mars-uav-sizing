function text = format_number(value, decimals)
%FORMAT_NUMBER Formatta un numero con separatori di migliaia stile US.

if nargin < 2 || isempty(decimals)
    decimals = 0;
end

if ~isscalar(value) || ~isnumeric(value)
    error('format_number:InvalidValue', 'Valore numerico scalare richiesto.');
end

if isnan(value)
    text = 'NaN';
    return;
end
if isinf(value)
    if value < 0
        text = '-Inf';
    else
        text = 'Inf';
    end
    return;
end

fmt = sprintf('%%.%df', decimals);
raw = sprintf(fmt, value);

sign = '';
if startsWith(raw, '-')
    sign = '-';
    raw = raw(2:end);
end

parts = split(raw, '.');
int_part = parts{1};
int_len = length(int_part);
if int_len > 3
    first = mod(int_len, 3);
    if first == 0
        first = 3;
    end
    grouped = int_part(1:first);
    idx = first + 1;
    while idx <= int_len
        grouped = [grouped ',' int_part(idx:min(idx+2, int_len))];
        idx = idx + 3;
    end
    int_part = grouped;
end

if numel(parts) > 1 && decimals > 0
    frac_part = parts{2};
    text = [sign int_part '.' frac_part];
else
    text = [sign int_part];
end
end
