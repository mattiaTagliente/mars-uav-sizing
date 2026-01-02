function mtow = get_mtow()
%GET_MTOW MTOW di riferimento in kg.

mtow = mars_uav.config.get_param('mission.mass.mtow_kg');
end
