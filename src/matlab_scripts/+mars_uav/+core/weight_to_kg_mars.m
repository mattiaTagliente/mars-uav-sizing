function mass_kg = weight_to_kg_mars(weight_n)
%WEIGHT_TO_KG_MARS Converte peso (N) in massa (kg) su Marte.

g_mars = mars_uav.config.get_mars_gravity();
mass_kg = weight_n / g_mars;
end
