function text = format_value(value, unit, decimals)
%FORMAT_VALUE Formatta un valore numerico con unita.

if nargin < 3 || isempty(decimals)
    decimals = 2;
end

text = sprintf('%s %s', mars_uav.core.format_number(value, decimals), unit);
end
