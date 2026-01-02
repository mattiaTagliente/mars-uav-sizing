classdef propeller_sizing
    %PROPELLER_SIZING Calcoli di dimensionamento eliche.

    methods(Static)
        function a = get_speed_of_sound()
            a = mars_uav.config.get_param('environment.arcadia_planitia.speed_of_sound_m_s');
        end

        function v_tip_max = max_tip_speed(mach_limit)
            if nargin < 1 || isempty(mach_limit)
                mach_limit = 0.7;
            end
            a = mars_uav.section6.propeller_sizing.get_speed_of_sound();
            v_tip_max = mach_limit * a;
        end

        function lift = lift_propeller_sizing()
            g_mars = mars_uav.config.get_mars_gravity();
            rho = mars_uav.config.get_density();
            mtow_kg = mars_uav.config.get_mtow();
            weight_n = mtow_kg * g_mars;

            disk_loading = mars_uav.config.get_param('geometry.rotor.disk_loading_N_m2');
            n_lift_motors = mars_uav.config.get_param('geometry.propulsion_config.lift.n_motors');

            total_disk_area = weight_n / disk_loading;
            thrust_per_rotor = weight_n / n_lift_motors;
            disk_area_per_rotor = total_disk_area / n_lift_motors;

            diameter_m = 2 * sqrt(disk_area_per_rotor / pi);
            diameter_in = diameter_m * 39.37;

            v_tip_max = mars_uav.section6.propeller_sizing.max_tip_speed(0.7);
            rpm_max = (v_tip_max / (pi * diameter_m)) * 60;

            rpm_operating = 0.7 * rpm_max;
            v_tip_operating = (rpm_operating / 60) * pi * diameter_m;
            mach_tip = v_tip_operating / mars_uav.section6.propeller_sizing.get_speed_of_sound();

            prop_model = mars_uav.config.get_param('propulsion.components.lift.propeller.model');
            prop_diameter_in = mars_uav.config.get_param('propulsion.components.lift.propeller.diameter_in');

            lift = struct( ...
                'n_motors', n_lift_motors, ...
                'total_thrust_n', weight_n, ...
                'thrust_per_rotor_n', thrust_per_rotor, ...
                'disk_loading_n_m2', disk_loading, ...
                'total_disk_area_m2', total_disk_area, ...
                'disk_area_per_rotor_m2', disk_area_per_rotor, ...
                'diameter_required_m', diameter_m, ...
                'diameter_required_in', diameter_in, ...
                'rpm_max_tip_limit', rpm_max, ...
                'rpm_operating', rpm_operating, ...
                'v_tip_operating_m_s', v_tip_operating, ...
                'mach_tip', mach_tip, ...
                'selected_model', prop_model, ...
                'selected_diameter_in', prop_diameter_in ...
            );
        end

        function cruise = cruise_propeller_sizing()
            g_mars = mars_uav.config.get_mars_gravity();
            rho = mars_uav.config.get_density();
            mtow_kg = mars_uav.config.get_mtow();
            weight_n = mtow_kg * g_mars;

            v_cruise = mars_uav.config.get_mission_params().v_cruise;

            [ld_max, ~] = mars_uav.section5.fixed_wing.maximum_ld();
            ld_penalty = mars_uav.config.get_param('aerodynamic.quadplane.ld_penalty_factor');
            ld_cruise = ld_max * ld_penalty;

            cruise_thrust_n = weight_n / ld_cruise;

            n_cruise_motors = mars_uav.config.get_param('geometry.propulsion_config.cruise.n_motors');
            thrust_per_motor = cruise_thrust_n / n_cruise_motors;

            ct_typical = 0.10;
            d_min_m = sqrt(8 * cruise_thrust_n / (pi * rho * v_cruise^2 * ct_typical));
            d_min_in = d_min_m * 39.37;

            prop_model = mars_uav.config.get_param('propulsion.components.cruise.propeller.model');
            prop_diameter_in = mars_uav.config.get_param('propulsion.components.cruise.propeller.diameter_in');
            prop_pitch_in = mars_uav.config.get_param('propulsion.components.cruise.propeller.pitch_in');

            rpm_cruise = 8000;
            diameter_m = prop_diameter_in / 39.37;
            n_rps = rpm_cruise / 60;
            advance_ratio = v_cruise / (n_rps * diameter_m);

            v_tip = (rpm_cruise / 60) * pi * diameter_m;
            mach_tip = v_tip / mars_uav.section6.propeller_sizing.get_speed_of_sound();

            cruise = struct( ...
                'n_motors', n_cruise_motors, ...
                'cruise_thrust_n', cruise_thrust_n, ...
                'thrust_per_motor_n', thrust_per_motor, ...
                'ld_cruise', ld_cruise, ...
                'v_cruise_m_s', v_cruise, ...
                'diameter_min_m', d_min_m, ...
                'diameter_min_in', d_min_in, ...
                'selected_model', prop_model, ...
                'selected_diameter_in', prop_diameter_in, ...
                'selected_pitch_in', prop_pitch_in, ...
                'advance_ratio', advance_ratio, ...
                'rpm_cruise', rpm_cruise, ...
                'v_tip_m_s', v_tip, ...
                'mach_tip', mach_tip ...
            );
        end

        function results = propeller_sizing_analysis()
            lift = mars_uav.section6.propeller_sizing.lift_propeller_sizing();
            cruise = mars_uav.section6.propeller_sizing.cruise_propeller_sizing();

            geom = mars_uav.section5.matching_chart.derive_geometry();
            wingspan_m = geom.wingspan_m;

            lift_prop_dia_m = lift.selected_diameter_in / 39.37;
            cruise_prop_dia_m = cruise.selected_diameter_in / 39.37;

            envelope_width = wingspan_m;
            total_aircraft_length = mars_uav.config.get_param('design.fuselage.total_length_m');
            envelope_length = total_aircraft_length;

            results = struct( ...
                'lift', lift, ...
                'cruise', cruise, ...
                'envelope', struct( ...
                    'wingspan_m', wingspan_m, ...
                    'lift_prop_diameter_m', lift_prop_dia_m, ...
                    'cruise_prop_diameter_m', cruise_prop_dia_m, ...
                    'envelope_width_m', envelope_width, ...
                    'envelope_length_m', envelope_length ...
                ) ...
            );
        end

        function print_analysis(results)
            if nargin < 1 || isempty(results)
                results = mars_uav.section6.propeller_sizing.propeller_sizing_analysis();
            end

            lift = results.lift;
            cruise = results.cruise;
            env = results.envelope;
            fmt = @(value, decimals) mars_uav.core.format_number(value, decimals);

            fprintf('%s\n', repmat('=', 1, 70));
            fprintf('ANALISI DIMENSIONAMENTO ELICHE (Sezione 6.3)\n');
            fprintf('%s\n', repmat('=', 1, 70));
            fprintf('Calcolato: %s\n', datestr(now, 'yyyy-mm-dd HH:MM:SS'));
            fprintf('Config:    Valori da file YAML in config/\n\n');

            fprintf('DIMENSIONAMENTO ELICHE LIFT (hovering)\n');
            fprintf('%s\n', repmat('-', 1, 50));
            fprintf('  Numero rotori:         %s\n', fmt(lift.n_motors, 0));
            fprintf('  Spinta hovering totale: %s N\n', fmt(lift.total_thrust_n, 2));
            fprintf('  Spinta per rotore:     %s N\n', fmt(lift.thrust_per_rotor_n, 2));
            fprintf('  Carico disco:          %s N/m^2\n', fmt(lift.disk_loading_n_m2, 1));
            fprintf('  Area disco totale:     %s m^2\n', fmt(lift.total_disk_area_m2, 3));
            fprintf('  Area disco per rotore: %s m^2\n', fmt(lift.disk_area_per_rotor_m2, 4));
            fprintf('  Diametro richiesto:    %s m (%s in)\n', ...
                fmt(lift.diameter_required_m, 3), fmt(lift.diameter_required_in, 1));
            fprintf('  Elica selezionata:     %s (%s in)\n', lift.selected_model, fmt(lift.selected_diameter_in, 1));
            fprintf('  Mach di punta (oper.): %s\n\n', fmt(lift.mach_tip, 3));

            fprintf('DIMENSIONAMENTO ELICHE CROCIERA (volo in avanti)\n');
            fprintf('%s\n', repmat('-', 1, 50));
            fprintf('  Numero motori:         %s\n', fmt(cruise.n_motors, 0));
            fprintf('  Velocita crociera:     %s m/s\n', fmt(cruise.v_cruise_m_s, 1));
            fprintf('  L/D crociera:          %s\n', fmt(cruise.ld_cruise, 2));
            fprintf('  Spinta crociera tot:   %s N\n', fmt(cruise.cruise_thrust_n, 2));
            fprintf('  Spinta per motore:     %s N\n', fmt(cruise.thrust_per_motor_n, 2));
            fprintf('  Diametro minimo:       %s m (%s in)\n', ...
                fmt(cruise.diameter_min_m, 3), fmt(cruise.diameter_min_in, 1));
            fprintf('  Elica selezionata:     %s (%s in)\n', cruise.selected_model, fmt(cruise.selected_diameter_in, 1));
            fprintf('  Rapporto di avanzam. J: %s\n', fmt(cruise.advance_ratio, 2));
            fprintf('  Mach di punta (croc.): %s\n\n', fmt(cruise.mach_tip, 3));

            fprintf('INGOMBRO UAV (per hangar)\n');
            fprintf('%s\n', repmat('-', 1, 50));
            fprintf('  Apertura alare:        %s m\n', fmt(env.wingspan_m, 2));
            fprintf('  Diametro elica lift:   %s m\n', fmt(env.lift_prop_diameter_m, 3));
            fprintf('  Diametro elica croc.:  %s m\n', fmt(env.cruise_prop_diameter_m, 3));
            fprintf('  Ingombro larghezza:    %s m (con rotori)\n', fmt(env.envelope_width_m, 2));
            fprintf('  Ingombro lunghezza:    %s m (fusoliera)\n\n', fmt(env.envelope_length_m, 2));

            fprintf('VERIFICA\n');
            fprintf('%s\n', repmat('-', 1, 50));
            lift_ok = lift.selected_diameter_in >= lift.diameter_required_in * 0.9;
            cruise_ok = cruise.selected_diameter_in >= cruise.diameter_min_in * 0.9;
            mach_ok = lift.mach_tip < 0.7 && cruise.mach_tip < 0.7;

            fprintf('  Dimensionamento lift:  %s\n', mars_uav.section6.propeller_sizing.pass_fail(lift_ok, 'OK', 'ATT'));
            fprintf('  Dimensionamento croc.: %s\n', mars_uav.section6.propeller_sizing.pass_fail(cruise_ok, 'OK', 'ATT'));
            fprintf('  Limiti Mach punta:     %s\n', mars_uav.section6.propeller_sizing.pass_fail(mach_ok, 'OK', 'NO'));

            fprintf('%s\n', repmat('=', 1, 70));
        end

        function text = pass_fail(flag, pass_text, fail_text)
            if flag
                text = ['[' pass_text ']'];
            else
                text = ['[' fail_text ']'];
            end
        end
    end
end

