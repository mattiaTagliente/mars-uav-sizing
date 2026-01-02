function config_dir = get_config_dir()
%GET_CONFIG_DIR Risolve la directory config nel codice Python.

this_file = mfilename('fullpath');
matlab_pkg_dir = fileparts(fileparts(this_file));
matlab_scripts_dir = fileparts(matlab_pkg_dir);
config_dir = fullfile(matlab_scripts_dir, '..', 'mars_uav_sizing', 'config');
config_dir = char(java.io.File(config_dir).getCanonicalPath());
end
