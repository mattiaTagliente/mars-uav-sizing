function value = get_param(path, default)
%GET_PARAM Recupera un parametro di config usando notazione con punti.

if nargin < 1 || isempty(path)
    error('get_param:MissingPath', 'Percorso parametro richiesto.');
end

config = mars_uav.config.load_config(false);
keys = split(string(path), '.');
value = config;

for i = 1:numel(keys)
    key = char(keys(i));
    if isstruct(value) && isfield(value, key)
        value = value.(key);
    else
        if nargin >= 2
            value = default;
            return;
        end
        error('get_param:NotFound', 'Percorso config non trovato: %s', path);
    end
end
end
