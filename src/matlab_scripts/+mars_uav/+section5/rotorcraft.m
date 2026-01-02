classdef rotorcraft
    %ROTORCRAFT Analisi configurazione a rotore.

    methods(Static)
        function v_i = induced_velocity(thrust_n, rho, disk_area_m2)
            v_i = sqrt(thrust_n / (2 * rho * disk_area_m2));
        end

        function v_i = induced_velocity_from_disk_loading(disk_loading, rho)
            v_i = sqrt(disk_loading / (2 * rho));
        end

        function p_ideal = ideal_hover_power(weight_n, rho, disk_area_m2)
            p_ideal = (weight_n ^ 1.5) / sqrt(2 * rho * disk_area_m2);
        end

        function p_hover = actual_hover_power(weight_n, rho, disk_area_m2, figure_of_merit)
            if nargin < 4 || isempty(figure_of_merit)
                figure_of_merit = mars_uav.config.get_propulsion_efficiencies().figure_of_merit;
            end
            p_ideal = mars_uav.section5.rotorcraft.ideal_hover_power(weight_n, rho, disk_area_m2);
            p_hover = p_ideal / figure_of_merit;
        end

        function p_elec = electric_hover_power(weight_n, rho, disk_area_m2, figure_of_merit, eta_motor, eta_esc)
            g_mars = mars_uav.config.get_mars_gravity();
            prop = mars_uav.config.get_propulsion_efficiencies();

            if nargin < 1 || isempty(weight_n)
                weight_n = mars_uav.config.get_mtow() * g_mars;
            end
            if nargin < 2 || isempty(rho)
                rho = mars_uav.config.get_density();
            end
            if nargin < 4 || isempty(figure_of_merit)
                figure_of_merit = prop.figure_of_merit;
            end
            if nargin < 5 || isempty(eta_motor)
                eta_motor = prop.eta_motor;
            end
            if nargin < 6 || isempty(eta_esc)
                eta_esc = prop.eta_esc;
            end
            if nargin < 3 || isempty(disk_area_m2)
                disk_loading = mars_uav.config.get_param('geometry.rotor.disk_loading_N_m2');
                disk_area_m2 = weight_n / disk_loading;
            end

            p_hover = mars_uav.section5.rotorcraft.actual_hover_power( ...
                weight_n, rho, disk_area_m2, figure_of_merit);
            p_elec = p_hover / (eta_motor * eta_esc);
        end

        function pw = hover_power_loading(disk_loading, rho, figure_of_merit, eta_motor, eta_esc)
            prop = mars_uav.config.get_propulsion_efficiencies();

            if nargin < 1 || isempty(disk_loading)
                disk_loading = mars_uav.config.get_param('geometry.rotor.disk_loading_N_m2');
            end
            if nargin < 2 || isempty(rho)
                rho = mars_uav.config.get_density();
            end
            if nargin < 3 || isempty(figure_of_merit)
                figure_of_merit = prop.figure_of_merit;
            end
            if nargin < 4 || isempty(eta_motor)
                eta_motor = prop.eta_motor;
            end
            if nargin < 5 || isempty(eta_esc)
                eta_esc = prop.eta_esc;
            end

            eta_hover = figure_of_merit * eta_motor * eta_esc;
            v_i = mars_uav.section5.rotorcraft.induced_velocity_from_disk_loading(disk_loading, rho);
            pw = v_i / eta_hover;
        end

        function p_mech = forward_flight_power(weight_n, velocity, ld_effective)
            if nargin < 3 || isempty(ld_effective)
                ld_effective = mars_uav.config.get_aerodynamic_params().ld_eff_rotorcraft;
            end
            p_mech = (weight_n * velocity) / ld_effective;
        end

        function p_elec = electric_forward_flight_power(weight_n, velocity, ld_effective, eta_motor, eta_esc)
            g_mars = mars_uav.config.get_mars_gravity();
            prop = mars_uav.config.get_propulsion_efficiencies();
            mission = mars_uav.config.get_mission_params();

            if nargin < 1 || isempty(weight_n)
                weight_n = mars_uav.config.get_mtow() * g_mars;
            end
            if nargin < 2 || isempty(velocity)
                velocity = mission.v_cruise;
            end
            if nargin < 3 || isempty(ld_effective)
                ld_effective = mars_uav.config.get_aerodynamic_params().ld_eff_rotorcraft;
            end
            if nargin < 4 || isempty(eta_motor)
                eta_motor = prop.eta_motor;
            end
            if nargin < 5 || isempty(eta_esc)
                eta_esc = prop.eta_esc;
            end

            p_mech = mars_uav.section5.rotorcraft.forward_flight_power(weight_n, velocity, ld_effective);
            p_elec = p_mech / (eta_motor * eta_esc);
        end

        function t_endurance_s = rotorcraft_endurance_seconds()
            g_mars = mars_uav.config.get_mars_gravity();
            prop = mars_uav.config.get_propulsion_efficiencies();
            batt = mars_uav.config.get_battery_params();
            mission = mars_uav.config.get_mission_params();
            aero = mars_uav.config.get_aerodynamic_params();

            e_spec_j_kg = batt.e_spec_Wh_kg * 3600;

            numerator = mission.f_batt * e_spec_j_kg * batt.dod * batt.eta_discharge ...
                * aero.ld_eff_rotorcraft * prop.eta_motor * prop.eta_esc;
            denominator = g_mars * mission.v_cruise;

            t_endurance_s = numerator / denominator;
        end

        function results = rotorcraft_feasibility_analysis()
            g_mars = mars_uav.config.get_mars_gravity();
            rho = mars_uav.config.get_density();
            mtow_kg = mars_uav.config.get_mtow();
            prop = mars_uav.config.get_propulsion_efficiencies();
            batt = mars_uav.config.get_battery_params();
            mission = mars_uav.config.get_mission_params();
            aero = mars_uav.config.get_aerodynamic_params();
            disk_loading = mars_uav.config.get_param('geometry.rotor.disk_loading_N_m2');
            endurance_req = mars_uav.config.get_param('mission.requirements.endurance_min');

            weight_n = mtow_kg * g_mars;
            disk_area_m2 = weight_n / disk_loading;
            v_cruise = mission.v_cruise;
            hover_time_s = mission.t_hover_s;
            reserve_fraction = mission.energy_reserve;
            f_batt = mission.f_batt;

            p_hover_elec = mars_uav.section5.rotorcraft.electric_hover_power( ...
                weight_n, rho, disk_area_m2, prop.figure_of_merit, prop.eta_motor, prop.eta_esc);

            p_cruise_elec = mars_uav.section5.rotorcraft.electric_forward_flight_power( ...
                weight_n, v_cruise, aero.ld_eff_rotorcraft, prop.eta_motor, prop.eta_esc);

            battery_mass_kg = f_batt * mtow_kg;
            total_energy_wh = battery_mass_kg * batt.e_spec_Wh_kg;
            usable_energy_wh = total_energy_wh * batt.dod * batt.eta_discharge;
            energy_after_reserve = usable_energy_wh * (1 - reserve_fraction);

            hover_energy_wh = p_hover_elec * (hover_time_s / 3600);
            cruise_energy_wh = energy_after_reserve - hover_energy_wh;

            if cruise_energy_wh > 0
                cruise_time_s = (cruise_energy_wh / p_cruise_elec) * 3600;
                cruise_time_min = cruise_time_s / 60;
            else
                cruise_time_s = 0;
                cruise_time_min = 0;
            end

            total_endurance_min = (hover_time_s / 60) + cruise_time_min;
            range_km = (v_cruise * cruise_time_s) / 1000;

            feasible = total_endurance_min >= endurance_req;
            margin_percent = ((total_endurance_min / endurance_req) - 1) * 100;

            v_i = mars_uav.section5.rotorcraft.induced_velocity(weight_n, rho, disk_area_m2);
            eta_hover = prop.figure_of_merit * prop.eta_motor * prop.eta_esc;
            eta_cruise = prop.eta_motor * prop.eta_esc;

            results = struct( ...
                'mtow_kg', mtow_kg, ...
                'weight_n', weight_n, ...
                'disk_loading_n_m2', disk_loading, ...
                'disk_area_m2', disk_area_m2, ...
                'rho_kg_m3', rho, ...
                'v_cruise_m_s', v_cruise, ...
                'figure_of_merit', prop.figure_of_merit, ...
                'eta_motor', prop.eta_motor, ...
                'eta_esc', prop.eta_esc, ...
                'eta_hover', eta_hover, ...
                'eta_cruise', eta_cruise, ...
                'ld_effective', aero.ld_eff_rotorcraft, ...
                'induced_velocity_m_s', v_i, ...
                'hover_power_w', p_hover_elec, ...
                'cruise_power_w', p_cruise_elec, ...
                'power_loading_w_per_n', p_hover_elec / weight_n, ...
                'power_loading_w_per_kg', p_hover_elec / mtow_kg, ...
                'battery_mass_kg', battery_mass_kg, ...
                'total_energy_wh', total_energy_wh, ...
                'usable_energy_wh', usable_energy_wh, ...
                'energy_after_reserve_wh', energy_after_reserve, ...
                'hover_energy_wh', hover_energy_wh, ...
                'cruise_energy_wh', cruise_energy_wh, ...
                'hover_time_min', hover_time_s / 60, ...
                'cruise_time_min', cruise_time_min, ...
                'endurance_min', total_endurance_min, ...
                'range_km', range_km, ...
                'requirement_min', endurance_req, ...
                'feasible', feasible, ...
                'margin_percent', margin_percent ...
            );
        end

        function print_analysis(results)
            if nargin < 1 || isempty(results)
                results = mars_uav.section5.rotorcraft.rotorcraft_feasibility_analysis();
            end
            fmt = @(value, decimals) mars_uav.core.format_number(value, decimals);

            fprintf('%s\n', repmat('=', 1, 80));
            fprintf('ANALISI DI FATTIBILITA VELIVOLO A ROTORE (Sezione 5.1)\n');
            fprintf('%s\n', repmat('=', 1, 80));
            fprintf('Calcolato: %s\n', datestr(now, 'yyyy-mm-dd HH:MM:SS'));
            fprintf('Config:    Valori da file YAML in config/\n\n');

            fprintf('PARAMETRI DI INGRESSO (da configurazione)\n');
            fprintf('%s\n', repmat('-', 1, 50));
            fprintf('  MTOW:               %s kg\n', fmt(results.mtow_kg, 2));
            fprintf('  Gravita Marte:      %s m/s^2\n', fmt(mars_uav.config.get_mars_gravity(), 3));
            fprintf('  Peso:               %s N\n', fmt(results.weight_n, 2));
            fprintf('  Carico disco:       %s N/m^2\n', fmt(results.disk_loading_n_m2, 1));
            fprintf('  Densita aria:       %s kg/m^3\n', fmt(results.rho_kg_m3, 4));
            fprintf('  Velocita crociera:  %s m/s\n\n', fmt(results.v_cruise_m_s, 1));

            fprintf('EFFICIENZE PROPULSIONE\n');
            fprintf('%s\n', repmat('-', 1, 50));
            fprintf('  Figura di merito:   %s\n', fmt(results.figure_of_merit, 2));
            fprintf('  Efficienza motore:  %s\n', fmt(results.eta_motor, 2));
            fprintf('  Efficienza ESC:     %s\n', fmt(results.eta_esc, 2));
            fprintf('  Eta hovering combinata: %s\n', fmt(results.eta_hover, 4));
            fprintf('  L/D equivalente:    %s\n\n', fmt(results.ld_effective, 1));

            fprintf('ANALISI HOVERING\n');
            fprintf('%s\n', repmat('-', 1, 50));
            fprintf('  Area disco:         %s m^2\n', fmt(results.disk_area_m2, 3));
            fprintf('  Velocita indotta:   %s m/s\n', fmt(results.induced_velocity_m_s, 2));
            fprintf('  Potenza elettrica:  %s W\n', fmt(results.hover_power_w, 0));
            fprintf('  Carico di potenza:  %s W/kg\n\n', fmt(results.power_loading_w_per_kg, 0));

            fprintf('ANALISI VOLO IN AVANTI\n');
            fprintf('%s\n', repmat('-', 1, 50));
            fprintf('  Potenza crociera:   %s W\n\n', fmt(results.cruise_power_w, 1));

            fprintf('BILANCIO ENERGETICO\n');
            fprintf('%s\n', repmat('-', 1, 50));
            fprintf('  Massa batteria:     %s kg\n', fmt(results.battery_mass_kg, 2));
            fprintf('  Capacita totale:    %s Wh\n', fmt(results.total_energy_wh, 1));
            fprintf('  Utilizzabile (DoD): %s Wh\n', fmt(results.usable_energy_wh, 1));
            fprintf('  Dopo riserva:       %s Wh\n', fmt(results.energy_after_reserve_wh, 1));
            fprintf('  Energia hovering:   %s Wh (%s min)\n', ...
                fmt(results.hover_energy_wh, 1), fmt(results.hover_time_min, 0));
            fprintf('  Energia crociera:   %s Wh\n\n', fmt(results.cruise_energy_wh, 1));

            fprintf('PRESTAZIONI\n');
            fprintf('%s\n', repmat('-', 1, 50));
            fprintf('  Tempo crociera:     %s min\n', fmt(results.cruise_time_min, 1));
            fprintf('  Autonomia totale:   %s min\n', fmt(results.endurance_min, 1));
            fprintf('  Raggio:             %s km\n\n', fmt(results.range_km, 0));

            fprintf('VALUTAZIONE FATTIBILITA\n');
            fprintf('%s\n', repmat('-', 1, 50));
            if results.feasible
                status = '[OK]';
            else
                status = '[NO]';
            end
            fprintf('  Requisito:          %s min autonomia\n', fmt(results.requirement_min, 0));
            fprintf('  Risultato:          %s min\n', fmt(results.endurance_min, 1));
            fprintf('  Margine:            %s%%\n', fmt(results.margin_percent, 1));
            fprintf('  Esito:              %s\n\n', status);

            if ~results.feasible
                fprintf('CONCLUSIONE: La configurazione a rotore non soddisfa il requisito di autonomia.\n');
            elseif results.margin_percent < 10
                fprintf('CONCLUSIONE: Il velivolo a rotore soddisfa il requisito con margine ridotto.\n');
            else
                fprintf('CONCLUSIONE: Il velivolo a rotore soddisfa il requisito con margine %s%%.\n', ...
                    fmt(results.margin_percent, 1));
            end

            fprintf('%s\n', repmat('=', 1, 80));
        end
    end
end

