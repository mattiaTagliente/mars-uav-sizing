function area_m2 = disk_area_from_loading(weight_n, disk_loading)
%DISK_AREA_FROM_LOADING Calcola area disco rotore da peso e carico disco.

if nargin < 2 || isempty(disk_loading)
    disk_loading = mars_uav.config.get_param('geometry.rotor.disk_loading_N_m2');
end
area_m2 = weight_n / disk_loading;
end
