function weight_n = kg_to_weight_mars(mass_kg)
%KG_TO_WEIGHT_MARS Converte massa (kg) in peso (N) su Marte.

g_mars = mars_uav.config.get_mars_gravity();
weight_n = mass_kg * g_mars;
end
