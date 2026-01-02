function print_config_summary()
%PRINT_CONFIG_SUMMARY Stampa un riepilogo dei valori di configurazione.

mars_uav.config.load_config(false);

fprintf('%s\n', repmat('=', 1, 70));
fprintf('RIEPILOGO CONFIGURAZIONE UAV MARTE\n');
fprintf('%s\n', repmat('=', 1, 70));

fprintf('\n[COSTANTI FISICHE]\n');
fprintf('  Gravita Marte:      %s m/s^2\n', mars_uav.core.format_number(mars_uav.config.get_mars_gravity(), 3));

fprintf('\n[AMBIENTE - Arcadia Planitia]\n');
fprintf('  Densita:            %s kg/m^3\n', mars_uav.core.format_number(mars_uav.config.get_density(), 4));

fprintf('\n[PROPULSIONE]\n');
prop = mars_uav.config.get_propulsion_efficiencies();
fprintf('  Figura di merito:   %s\n', mars_uav.core.format_number(prop.figure_of_merit, 3));
fprintf('  Eta motore:         %s\n', mars_uav.core.format_number(prop.eta_motor, 3));
fprintf('  Eta ESC:            %s\n', mars_uav.core.format_number(prop.eta_esc, 3));
fprintf('  Eta elica:          %s\n', mars_uav.core.format_number(prop.eta_prop, 3));

fprintf('\n[BATTERIA]\n');
batt = mars_uav.config.get_battery_params();
fprintf('  Energia specifica:  %s Wh/kg\n', mars_uav.core.format_number(batt.e_spec_Wh_kg, 1));
fprintf('  Profondita scarica: %s\n', mars_uav.core.format_number(batt.dod, 2));
fprintf('  Eta scarica:        %s\n', mars_uav.core.format_number(batt.eta_discharge, 2));

fprintf('\n[AERODINAMICA]\n');
aero = mars_uav.config.get_aerodynamic_params();
fprintf('  Rapporto d''aspetto: %s\n', mars_uav.core.format_number(aero.aspect_ratio, 2));
fprintf('  Efficienza Oswald:  %s\n', mars_uav.core.format_number(aero.oswald_e, 4));
fprintf('  C_D0:               %s\n', mars_uav.core.format_number(aero.cd0, 4));
fprintf('  C_L,max:            %s\n', mars_uav.core.format_number(aero.cl_max, 2));
fprintf('  L/D effettivo (rotore): %s\n', mars_uav.core.format_number(aero.ld_eff_rotorcraft, 2));

fprintf('\n[MISSIONE]\n');
mission = mars_uav.config.get_mission_params();
fprintf('  Velocita crociera:  %s m/s\n', mars_uav.core.format_number(mission.v_cruise, 1));
fprintf('  Velocita stallo:    %s m/s\n', mars_uav.core.format_number(mission.v_stall, 1));
fprintf('  Tempo hovering:     %s s\n', mars_uav.core.format_number(mission.t_hover_s, 0));
fprintf('  Tempo crociera:     %s min\n', mars_uav.core.format_number(mission.t_cruise_min, 0));
fprintf('  Riserva energia:    %s\n', mars_uav.core.format_number(mission.energy_reserve, 2));
fprintf('  Frazione batteria:  %s\n', mars_uav.core.format_number(mission.f_batt, 2));
fprintf('  MTOW:               %s kg\n', mars_uav.core.format_number(mars_uav.config.get_mtow(), 2));

fprintf('\n[GEOMETRIA]\n');
geom = mars_uav.config.get_geometry_params();
fprintf('  Carico del disco:   %s N/m^2\n', mars_uav.core.format_number(geom.disk_loading, 1));
fprintf('  Rapporto rastremazione: %s\n', mars_uav.core.format_number(geom.taper_ratio, 2));
fprintf('  Rapporto spessore:  %s\n', mars_uav.core.format_number(geom.thickness_ratio, 2));

fprintf('%s\n', repmat('=', 1, 70));
end
