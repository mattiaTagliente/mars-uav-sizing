function rho = get_density()
%GET_DENSITY Densita atmosferica ad Arcadia Planitia (kg/m^3).

rho = mars_uav.config.get_param('environment.arcadia_planitia.density_kg_m3');
end
