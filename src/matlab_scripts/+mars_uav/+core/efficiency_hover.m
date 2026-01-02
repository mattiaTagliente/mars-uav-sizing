function eta = efficiency_hover()
%EFFICIENCY_HOVER Efficienza hovering combinata.

prop = mars_uav.config.get_propulsion_efficiencies();
eta = prop.figure_of_merit * prop.eta_motor * prop.eta_esc;
end
