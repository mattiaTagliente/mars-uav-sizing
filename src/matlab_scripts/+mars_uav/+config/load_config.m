function config = load_config(reload)
%LOAD_CONFIG Carica e mette in cache i file YAML di configurazione.

persistent config_cache

if nargin < 1
    reload = false;
end

if ~reload && ~isempty(config_cache)
    config = config_cache;
    return;
end

config_dir = mars_uav.config.get_config_dir();

files = struct();
files.physical = 'physical_constants.yaml';
files.environment = 'mars_environment.yaml';
files.propulsion = 'propulsion_parameters.yaml';
files.battery = 'battery_parameters.yaml';
files.aerodynamic = 'aerodynamic_parameters.yaml';
files.geometry = 'geometry_parameters.yaml';
files.mission = 'mission_parameters.yaml';
files.design = 'design_decisions.yaml';

config = struct();
keys = fieldnames(files);
for i = 1:numel(keys)
    key = keys{i};
    file_path = fullfile(config_dir, files.(key));
    if exist(file_path, 'file') ~= 2
        warning('load_config:MissingFile', 'File di configurazione mancante: %s', file_path);
        config.(key) = struct();
        continue;
    end
    config.(key) = mars_uav.config.read_yaml(file_path);
end

config_cache = config;
end
