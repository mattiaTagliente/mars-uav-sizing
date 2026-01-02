classdef fixed_wing
    %FIXED_WING Analisi configurazione ala fissa.

    methods(Static)
        function c_l = cruise_lift_coefficient(wing_loading, rho, velocity)
            c_l = (2 * wing_loading) / (rho * velocity^2);
        end

        function c_d = drag_coefficient(c_l, c_d0, ar, e)
            aero = mars_uav.config.get_aerodynamic_params();
            if nargin < 2 || isempty(c_d0)
                c_d0 = aero.cd0;
            end
            if nargin < 3 || isempty(ar)
                ar = aero.aspect_ratio;
            end
            if nargin < 4 || isempty(e)
                e = aero.oswald_e;
            end
            k = 1 / (pi * ar * e);
            c_d = c_d0 + k * c_l^2;
        end

        function k = induced_drag_factor(ar, e)
            aero = mars_uav.config.get_aerodynamic_params();
            if nargin < 1 || isempty(ar)
                ar = aero.aspect_ratio;
            end
            if nargin < 2 || isempty(e)
                e = aero.oswald_e;
            end
            k = 1 / (pi * ar * e);
        end

        function ld = lift_to_drag(c_l, c_d0, ar, e)
            if nargin < 2
                c_d0 = [];
            end
            if nargin < 3
                ar = [];
            end
            if nargin < 4
                e = [];
            end
            c_d = mars_uav.section5.fixed_wing.drag_coefficient(c_l, c_d0, ar, e);
            ld = c_l / c_d;
        end

        function [ld_max, cl_opt] = maximum_ld(c_d0, ar, e)
            aero = mars_uav.config.get_aerodynamic_params();
            if nargin < 1 || isempty(c_d0)
                c_d0 = aero.cd0;
            end
            if nargin < 2 || isempty(ar)
                ar = aero.aspect_ratio;
            end
            if nargin < 3 || isempty(e)
                e = aero.oswald_e;
            end
            cl_opt = sqrt(pi * ar * e * c_d0);
            ld_max = 0.5 * sqrt(pi * ar * e / c_d0);
        end

        function p = cruise_power(weight_n, velocity, ld, eta_prop, eta_motor, eta_esc)
            prop = mars_uav.config.get_propulsion_efficiencies();
            if nargin < 4 || isempty(eta_prop)
                eta_prop = prop.eta_prop;
            end
            if nargin < 5 || isempty(eta_motor)
                eta_motor = prop.eta_motor;
            end
            if nargin < 6 || isempty(eta_esc)
                eta_esc = prop.eta_esc;
            end
            eta_cruise = eta_prop * eta_motor * eta_esc;
            p = (weight_n * velocity) / (ld * eta_cruise);
        end

        function pw = cruise_power_loading(velocity, ld, eta_prop, eta_motor, eta_esc)
            prop = mars_uav.config.get_propulsion_efficiencies();
            if nargin < 3 || isempty(eta_prop)
                eta_prop = prop.eta_prop;
            end
            if nargin < 4 || isempty(eta_motor)
                eta_motor = prop.eta_motor;
            end
            if nargin < 5 || isempty(eta_esc)
                eta_esc = prop.eta_esc;
            end
            eta_cruise = eta_prop * eta_motor * eta_esc;
            pw = velocity / (ld * eta_cruise);
        end

        function v_stall = stall_speed(wing_loading, rho, c_l_max)
            if nargin < 2 || isempty(rho)
                rho = mars_uav.config.get_density();
            end
            if nargin < 3 || isempty(c_l_max)
                c_l_max = mars_uav.config.get_aerodynamic_params().cl_max;
            end
            v_stall = sqrt((2 * wing_loading) / (rho * c_l_max));
        end

        function ws_max = stall_wing_loading_limit(rho, v_min, c_l_max)
            if nargin < 1 || isempty(rho)
                rho = mars_uav.config.get_density();
            end
            if nargin < 2 || isempty(v_min)
                mission = mars_uav.config.get_mission_params();
                v_min = mission.v_stall * mars_uav.config.get_param('mission.velocity.v_min_factor');
            end
            if nargin < 3 || isempty(c_l_max)
                c_l_max = mars_uav.config.get_aerodynamic_params().cl_max;
            end
            ws_max = 0.5 * rho * v_min^2 * c_l_max;
        end

        function t_endurance_s = fixed_wing_endurance_seconds()
            g_mars = mars_uav.config.get_mars_gravity();
            prop = mars_uav.config.get_propulsion_efficiencies();
            batt = mars_uav.config.get_battery_params();
            mission = mars_uav.config.get_mission_params();

            [ld_max, ~] = mars_uav.section5.fixed_wing.maximum_ld();
            eta_cruise = prop.eta_prop * prop.eta_motor * prop.eta_esc;
            e_spec_j_kg = batt.e_spec_Wh_kg * 3600;
            reserve_fraction = mission.energy_reserve;

            numerator = mission.f_batt * e_spec_j_kg * batt.dod * batt.eta_discharge ...
                * (1 - reserve_fraction) * ld_max * eta_cruise;
            denominator = g_mars * mission.v_cruise;

            t_endurance_s = numerator / denominator;
        end

        function s_to = takeoff_ground_roll(wing_loading, rho, c_l_max, acceleration)
            if nargin < 4 || isempty(acceleration)
                acceleration = 0.7;
            end
            if nargin < 2 || isempty(rho)
                rho = mars_uav.config.get_density();
            end
            if nargin < 3 || isempty(c_l_max)
                c_l_max = mars_uav.config.get_aerodynamic_params().cl_max;
            end
            if nargin < 1 || isempty(wing_loading)
                v_min = mars_uav.config.get_mission_params().v_stall * ...
                    mars_uav.config.get_param('mission.velocity.v_min_factor');
                wing_loading = mars_uav.section5.fixed_wing.stall_wing_loading_limit(rho, v_min, c_l_max);
            end

            v_stall = mars_uav.section5.fixed_wing.stall_speed(wing_loading, rho, c_l_max);
            v_to = 1.1 * v_stall;
            s_to = v_to^2 / (2 * acceleration);
        end

        function results = fixed_wing_feasibility_analysis()
            g_mars = mars_uav.config.get_mars_gravity();
            rho = mars_uav.config.get_density();
            mtow_kg = mars_uav.config.get_mtow();
            prop = mars_uav.config.get_propulsion_efficiencies();
            batt = mars_uav.config.get_battery_params();
            mission = mars_uav.config.get_mission_params();
            aero = mars_uav.config.get_aerodynamic_params();
            endurance_req = mars_uav.config.get_param('mission.requirements.endurance_min');

            weight_n = mtow_kg * g_mars;
            v_cruise = mission.v_cruise;
            f_batt = mission.f_batt;

            [ld_max, cl_opt] = mars_uav.section5.fixed_wing.maximum_ld();
            k = mars_uav.section5.fixed_wing.induced_drag_factor();

            v_min = mission.v_stall * mars_uav.config.get_param('mission.velocity.v_min_factor');
            ws_max = mars_uav.section5.fixed_wing.stall_wing_loading_limit(rho, v_min, aero.cl_max);

            cl_cruise = mars_uav.section5.fixed_wing.cruise_lift_coefficient(ws_max, rho, v_cruise);
            ld_cruise = mars_uav.section5.fixed_wing.lift_to_drag(cl_cruise);

            eta_cruise = prop.eta_prop * prop.eta_motor * prop.eta_esc;
            p_cruise = mars_uav.section5.fixed_wing.cruise_power(weight_n, v_cruise, ld_max);
            pw_cruise = mars_uav.section5.fixed_wing.cruise_power_loading(v_cruise, ld_max);

            reserve_fraction = mission.energy_reserve;
            battery_mass_kg = f_batt * mtow_kg;
            total_energy_wh = battery_mass_kg * batt.e_spec_Wh_kg;
            usable_energy_wh = total_energy_wh * batt.dod * batt.eta_discharge * (1 - reserve_fraction);

            endurance_h = usable_energy_wh / p_cruise;
            endurance_min = endurance_h * 60;
            range_km = v_cruise * endurance_h * 3.6;

            takeoff_distance = mars_uav.section5.fixed_wing.takeoff_ground_roll(ws_max, rho, aero.cl_max);
            v_stall = mars_uav.section5.fixed_wing.stall_speed(ws_max, rho, aero.cl_max);

            vtol_possible = false;
            endurance_passes = endurance_min >= endurance_req;

            results = struct( ...
                'mtow_kg', mtow_kg, ...
                'weight_n', weight_n, ...
                'rho_kg_m3', rho, ...
                'v_cruise_m_s', v_cruise, ...
                'aspect_ratio', aero.aspect_ratio, ...
                'oswald_e', aero.oswald_e, ...
                'cd0', aero.cd0, ...
                'cl_max', aero.cl_max, ...
                'k_induced', k, ...
                'ld_max', ld_max, ...
                'cl_optimal', cl_opt, ...
                'cl_cruise', cl_cruise, ...
                'ld_cruise', ld_cruise, ...
                'eta_prop', prop.eta_prop, ...
                'eta_motor', prop.eta_motor, ...
                'eta_esc', prop.eta_esc, ...
                'eta_cruise', eta_cruise, ...
                'wing_loading_max', ws_max, ...
                'v_stall', v_stall, ...
                'cruise_power_w', p_cruise, ...
                'power_loading_w_per_n', pw_cruise, ...
                'battery_mass_kg', battery_mass_kg, ...
                'total_energy_wh', total_energy_wh, ...
                'energy_reserve_fraction', reserve_fraction, ...
                'usable_energy_wh', usable_energy_wh, ...
                'endurance_min', endurance_min, ...
                'range_km', range_km, ...
                'takeoff_distance_m', takeoff_distance, ...
                'requirement_min', endurance_req, ...
                'vtol_possible', vtol_possible, ...
                'endurance_passes', endurance_passes, ...
                'feasible', vtol_possible && endurance_passes, ...
                'fail_reason', 'Requisito VTOL non soddisfatto - nessuna pista su Marte' ...
            );
        end

        function print_analysis(results)
            if nargin < 1 || isempty(results)
                results = mars_uav.section5.fixed_wing.fixed_wing_feasibility_analysis();
            end
            fmt = @(value, decimals) mars_uav.core.format_number(value, decimals);

            fprintf('%s\n', repmat('=', 1, 80));
            fprintf('ANALISI DI FATTIBILITA ALA FISSA (Sezione 5.2)\n');
            fprintf('%s\n', repmat('=', 1, 80));
            fprintf('Calcolato: %s\n', datestr(now, 'yyyy-mm-dd HH:MM:SS'));
            fprintf('Config:    Valori da file YAML in config/\n\n');

            fprintf('PARAMETRI DI INGRESSO (da configurazione)\n');
            fprintf('%s\n', repmat('-', 1, 50));
            fprintf('  MTOW:               %s kg\n', fmt(results.mtow_kg, 2));
            fprintf('  Peso:               %s N\n', fmt(results.weight_n, 2));
            fprintf('  Densita aria:       %s kg/m^3\n', fmt(results.rho_kg_m3, 4));
            fprintf('  Velocita crociera:  %s m/s\n\n', fmt(results.v_cruise_m_s, 1));

            fprintf('PARAMETRI AERODINAMICI\n');
            fprintf('%s\n', repmat('-', 1, 50));
            fprintf('  Rapporto d''aspetto: %s\n', fmt(results.aspect_ratio, 2));
            fprintf('  Efficienza Oswald:  %s\n', fmt(results.oswald_e, 4));
            fprintf('  CD0:                %s\n', fmt(results.cd0, 4));
            fprintf('  CL_max:             %s\n', fmt(results.cl_max, 2));
            fprintf('  K (indotto):        %s\n', fmt(results.k_induced, 4));
            fprintf('  (L/D)_max:          %s\n', fmt(results.ld_max, 2));
            fprintf('  CL ottimale:        %s\n\n', fmt(results.cl_optimal, 3));

            fprintf('CARICO ALARE E STALLO\n');
            fprintf('%s\n', repmat('-', 1, 50));
            fprintf('  Carico alare max:   %s N/m^2\n', fmt(results.wing_loading_max, 2));
            fprintf('  Velocita stallo:    %s m/s\n\n', fmt(results.v_stall, 1));

            fprintf('PRESTAZIONI IN CROCIERA\n');
            fprintf('%s\n', repmat('-', 1, 50));
            fprintf('  CL in crociera:     %s\n', fmt(results.cl_cruise, 3));
            fprintf('  L/D in crociera:    %s\n', fmt(results.ld_cruise, 2));
            fprintf('  Potenza crociera:   %s W\n', fmt(results.cruise_power_w, 1));
            fprintf('  Eta_crociera combinata: %s\n\n', fmt(results.eta_cruise, 4));

            fprintf('AUTONOMIA E RAGGIO\n');
            fprintf('%s\n', repmat('-', 1, 50));
            fprintf('  Energia utile:      %s Wh\n', fmt(results.usable_energy_wh, 1));
            fprintf('  Autonomia:          %s min\n', fmt(results.endurance_min, 1));
            fprintf('  Raggio:             %s km\n\n', fmt(results.range_km, 0));

            fprintf('ANALISI DECOLLO (escludente)\n');
            fprintf('%s\n', repmat('-', 1, 50));
            fprintf('  Corsa al suolo:     %s m\n', fmt(results.takeoff_distance_m, 0));
            fprintf('  Esito:              IMPRATICABILE - Nessuna pista disponibile su Marte\n\n');

            fprintf('VALUTAZIONE FATTIBILITA\n');
            fprintf('%s\n', repmat('-', 1, 50));
            if results.endurance_passes
                end_status = '[OK]';
            else
                end_status = '[NO]';
            end
            if results.vtol_possible
                vtol_status = '[OK]';
            else
                vtol_status = '[NO]';
            end
            fprintf('  Requisito autonomia: %s min -> %s min -> %s\n', ...
                fmt(results.requirement_min, 0), fmt(results.endurance_min, 0), end_status);
            fprintf('  Requisito VTOL:     Richiesto -> Non possibile -> %s\n', vtol_status);
            fprintf('  Complessivo:        [NO]\n\n');

            fprintf('CONCLUSIONE: L''ala fissa fallisce per il requisito VTOL.\n');
            fprintf('%s\n', repmat('=', 1, 80));
        end
    end
end

