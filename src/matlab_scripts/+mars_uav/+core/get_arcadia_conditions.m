function state = get_arcadia_conditions()
%GET_ARCADIA_CONDITIONS Stato atmosferico ad Arcadia Planitia.

atm = mars_uav.core.MarsAtmosphere();
elevation = mars_uav.config.get_param('environment.arcadia_planitia.elevation_km');
state = atm.get_state(elevation);
end
