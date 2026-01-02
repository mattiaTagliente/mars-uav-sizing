function eta = efficiency_cruise()
%EFFICIENCY_CRUISE Efficienza crociera combinata.

prop = mars_uav.config.get_propulsion_efficiencies();
eta = prop.eta_prop * prop.eta_motor * prop.eta_esc;
end
