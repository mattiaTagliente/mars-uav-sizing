function usable_wh = usable_battery_energy(mtow_kg)
%USABLE_BATTERY_ENERGY Energia batteria utilizzabile in Wh.

if nargin < 1 || isempty(mtow_kg)
    mtow_kg = mars_uav.config.get_mtow();
end

f_batt = mars_uav.config.get_param('mission.mass_fractions.f_battery');
batt = mars_uav.config.get_battery_params();

usable_wh = f_batt * mtow_kg * batt.e_spec_Wh_kg * batt.dod * batt.eta_discharge;
end
