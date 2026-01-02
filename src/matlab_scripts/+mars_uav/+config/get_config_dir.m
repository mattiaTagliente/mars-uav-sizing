function config_dir = get_config_dir()
%GET_CONFIG_DIR Risolve la directory config con fallback portabili.

env_config = getenv('MARS_UAV_CONFIG_DIR');
if ~isempty(env_config) && exist(env_config, 'dir') == 7
    config_dir = env_config;
    return;
end

candidates = {};
env_root = getenv('MARS_UAV_ROOT');
if ~isempty(env_root)
    candidates = [candidates, { ...
        fullfile(env_root, 'src', 'mars_uav_sizing', 'config'), ...
        fullfile(env_root, 'src', 'matlab_scripts', 'config'), ...
        fullfile(env_root, 'config') ...
    }];
end

this_file = mfilename('fullpath');
matlab_pkg_dir = fileparts(fileparts(this_file));
matlab_scripts_dir = fileparts(matlab_pkg_dir);
src_dir = fileparts(matlab_scripts_dir);
repo_root = fileparts(src_dir);

candidates = [candidates, { ...
    fullfile(matlab_scripts_dir, 'config'), ...
    fullfile(src_dir, 'mars_uav_sizing', 'config'), ...
    fullfile(repo_root, 'config'), ...
    fullfile(repo_root, 'src', 'mars_uav_sizing', 'config') ...
}];

config_dir = '';
for i = 1:numel(candidates)
    candidate = char(candidates{i});
    if exist(candidate, 'dir') == 7
        if exist(fullfile(candidate, 'physical_constants.yaml'), 'file') == 2
            config_dir = candidate;
            break;
        end
    end
end

if isempty(config_dir)
    error('get_config_dir:NotFound', ...
        ['Directory config non trovata. Impostare MARS_UAV_CONFIG_DIR ' ...
         'oppure copiare src/mars_uav_sizing/config accanto al batch.']);
end

config_dir = char(java.io.File(config_dir).getCanonicalPath());
end
