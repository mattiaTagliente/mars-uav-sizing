classdef component_selection
    %COMPONENT_SELECTION Analisi selezione componenti.

    methods(Static)
        function candidates = get_lift_motor_candidates()
            candidates = [
                struct('model', 'V4006-380', 'manufacturer', 'SunnySky', 'mass_g', 66, 'power_w', 375, 'kv', 380, 'lipo', '4-6S', 'prop_size', '12-15', 'thrust_g', 2560, 'source_key', 'sunnyskySunnySkyV4006Multicopter2024'),
                struct('model', '4008 EEE-380', 'manufacturer', 'MAD', 'mass_g', 88, 'power_w', 400, 'kv', 380, 'lipo', '4-6S', 'prop_size', '14-18', 'thrust_g', 2700, 'source_key', 'madcomponentsMAD4008EEE2024'),
                struct('model', 'MN5008-400', 'manufacturer', 'T-Motor', 'mass_g', 135, 'power_w', 800, 'kv', 400, 'lipo', '6S', 'prop_size', '15-17', 'thrust_g', 4200, 'source_key', 't-motorTMotorMN5008Antigravity2024'),
                struct('model', 'MN505-S-260', 'manufacturer', 'T-Motor', 'mass_g', 225, 'power_w', 2500, 'kv', 260, 'lipo', '12S', 'prop_size', '16-17', 'thrust_g', [], 'source_key', 't-motorMN505SKV260Brushless2024')
            ];
        end

        function candidates = get_cruise_motor_candidates()
            candidates = [
                struct('model', 'AT2312-1150', 'manufacturer', 'T-Motor', 'mass_g', 60, 'power_w', 350, 'kv', 1150, 'lipo', '2-4S', 'prop_size', '10-12', 'thrust_g', [], 'source_key', 't-motorTMotorAT2312FixedWing2024'),
                struct('model', 'AT2814-1000', 'manufacturer', 'T-Motor', 'mass_g', 109, 'power_w', 370, 'kv', 1000, 'lipo', '2-4S', 'prop_size', '11-13', 'thrust_g', [], 'source_key', ''),
                struct('model', 'AT4130-230', 'manufacturer', 'T-Motor', 'mass_g', 408, 'power_w', 2500, 'kv', 230, 'lipo', '12S', 'prop_size', '15-18', 'thrust_g', [], 'source_key', '')
            ];
        end

        function candidates = get_esc_candidates()
            candidates = [
                struct('model', 'XRotor Micro 30A', 'manufacturer', 'Hobbywing', 'mass_g', 6, 'continuous_a', 30, 'burst_a', 40, 'lipo', '2-4S', 'has_bec', false, 'source_key', 'hobbywingHobbywingXRotorMicro2024'),
                struct('model', 'F35A', 'manufacturer', 'T-Motor', 'mass_g', 7, 'continuous_a', 35, 'burst_a', 45, 'lipo', '3-6S', 'has_bec', false, 'source_key', ''),
                struct('model', 'FLAME 60A 12S', 'manufacturer', 'T-Motor', 'mass_g', 74, 'continuous_a', 60, 'burst_a', 80, 'lipo', '12S', 'has_bec', false, 'source_key', 't-motorFLAME60A12S2024')
            ];
        end

        function power_req = get_power_requirements()
            hover_power = mars_uav.section5.hybrid_vtol.quadplane_hover_power();
            cruise_power = mars_uav.section5.hybrid_vtol.quadplane_cruise_power();

            n_lift = mars_uav.config.get_param('propulsion.components.lift.motor.quantity');
            n_cruise = mars_uav.config.get_param('propulsion.components.cruise.motor.quantity');

            power_req = struct( ...
                'hover_total_w', hover_power, ...
                'per_lift_motor_w', hover_power / n_lift, ...
                'cruise_total_w', cruise_power, ...
                'per_cruise_motor_w', cruise_power / n_cruise, ...
                'n_lift_motors', n_lift, ...
                'n_cruise_motors', n_cruise ...
            );
        end

        function mass_budget = get_mass_budget()
            mtow = mars_uav.config.get_param('mission.mass.mtow_kg');
            f_prop = mars_uav.config.get_param('mission.mass_fractions.f_propulsion');

            m_propulsion = f_prop * mtow;
            lift_fraction = 0.70;
            cruise_fraction = 0.30;

            m_lift = lift_fraction * m_propulsion;
            m_cruise = cruise_fraction * m_propulsion;

            n_lift_motors = mars_uav.config.get_param('propulsion.components.lift.motor.quantity');
            n_cruise_motors = mars_uav.config.get_param('propulsion.components.cruise.motor.quantity');

            mass_budget = struct( ...
                'mtow_kg', mtow, ...
                'f_propulsion', f_prop, ...
                'm_propulsion_kg', m_propulsion, ...
                'm_lift_kg', m_lift, ...
                'm_cruise_kg', m_cruise, ...
                'target_lift_motor_g', (m_lift * 1000) / n_lift_motors * 0.5, ...
                'target_cruise_motor_g', (m_cruise * 1000) / n_cruise_motors * 0.5, ...
                'n_lift_motors', n_lift_motors, ...
                'n_cruise_motors', n_cruise_motors ...
            );
        end

        function results = evaluate_motor_candidates(candidates, min_power_w, max_mass_g)
            results = struct('model', {}, 'mass_g', {}, 'power_w', {}, 'kv', {}, 'lipo', {}, ...
                'prop_size', {}, 'thrust_g', {}, 'power_ok', {}, 'mass_ok', {}, 'status', {}, 'source_key', {});

            for i = 1:numel(candidates)
                motor = candidates(i);
                power_ok = motor.power_w >= min_power_w;
                mass_ok = motor.mass_g <= max_mass_g;

                if power_ok && mass_ok
                    status = 'Idoneo';
                elseif power_ok && ~mass_ok
                    status = 'Troppo pesante';
                elseif ~power_ok && mass_ok
                    status = 'Potenza insufficiente';
                else
                    status = 'Non idoneo';
                end

                results(end + 1) = struct( ...
                    'model', sprintf('%s %s', motor.manufacturer, motor.model), ...
                    'mass_g', motor.mass_g, ...
                    'power_w', motor.power_w, ...
                    'kv', motor.kv, ...
                    'lipo', motor.lipo, ...
                    'prop_size', motor.prop_size, ...
                    'thrust_g', motor.thrust_g, ...
                    'power_ok', power_ok, ...
                    'mass_ok', mass_ok, ...
                    'status', status, ...
                    'source_key', motor.source_key ...
                );
            end
        end

        function selected = get_selected_components()
            selected = struct( ...
                'lift_motor', struct( ...
                    'model', mars_uav.config.get_param('propulsion.components.lift.motor.model'), ...
                    'mass_kg', mars_uav.config.get_param('propulsion.components.lift.motor.mass_kg'), ...
                    'quantity', mars_uav.config.get_param('propulsion.components.lift.motor.quantity'), ...
                    'max_power_w', mars_uav.config.get_param('propulsion.components.lift.motor.max_power_w') ...
                ), ...
                'lift_esc', struct( ...
                    'model', mars_uav.config.get_param('propulsion.components.lift.esc.model'), ...
                    'mass_kg', mars_uav.config.get_param('propulsion.components.lift.esc.mass_kg'), ...
                    'quantity', mars_uav.config.get_param('propulsion.components.lift.esc.quantity') ...
                ), ...
                'lift_propeller', struct( ...
                    'model', mars_uav.config.get_param('propulsion.components.lift.propeller.model'), ...
                    'mass_kg', mars_uav.config.get_param('propulsion.components.lift.propeller.mass_kg'), ...
                    'quantity', mars_uav.config.get_param('propulsion.components.lift.propeller.quantity') ...
                ), ...
                'cruise_motor', struct( ...
                    'model', mars_uav.config.get_param('propulsion.components.cruise.motor.model'), ...
                    'mass_kg', mars_uav.config.get_param('propulsion.components.cruise.motor.mass_kg'), ...
                    'quantity', mars_uav.config.get_param('propulsion.components.cruise.motor.quantity'), ...
                    'max_power_w', mars_uav.config.get_param('propulsion.components.cruise.motor.max_power_w') ...
                ), ...
                'cruise_esc', struct( ...
                    'model', mars_uav.config.get_param('propulsion.components.cruise.esc.model'), ...
                    'mass_kg', mars_uav.config.get_param('propulsion.components.cruise.esc.mass_kg'), ...
                    'quantity', mars_uav.config.get_param('propulsion.components.cruise.esc.quantity') ...
                ), ...
                'cruise_propeller', struct( ...
                    'model', mars_uav.config.get_param('propulsion.components.cruise.propeller.model'), ...
                    'mass_kg', mars_uav.config.get_param('propulsion.components.cruise.propeller.mass_kg'), ...
                    'quantity', mars_uav.config.get_param('propulsion.components.cruise.propeller.quantity') ...
                ) ...
            );
        end

        function print_component_selection()
            fprintf('%s\n', repmat('=', 1, 70));
            fprintf('ANALISI SELEZIONE COMPONENTI (Sezione 7)\n');
            fprintf('%s\n', repmat('=', 1, 70));
            fprintf('Calcolato: %s\n', datestr(now, 'yyyy-mm-dd HH:MM:SS'));
            fprintf('Config:    Valori da file YAML in config/\n');
            fmt = @(value, decimals) mars_uav.core.format_number(value, decimals);

            power_req = mars_uav.section7.component_selection.get_power_requirements();
            fprintf('\nREQUISITI DI POTENZA (da Sezione 5)\n');
            fprintf('%s\n', repmat('-', 1, 50));
            fprintf('  Potenza hovering totale: %s W\n', fmt(power_req.hover_total_w, 0));
            fprintf('  Per motore lift (%s):  %s W\n', ...
                fmt(power_req.n_lift_motors, 0), fmt(power_req.per_lift_motor_w, 0));
            fprintf('  Potenza crociera totale: %s W\n', fmt(power_req.cruise_total_w, 0));
            fprintf('  Per motore crociera (%s): %s W\n', ...
                fmt(power_req.n_cruise_motors, 0), fmt(power_req.per_cruise_motor_w, 0));

            mass_budget = mars_uav.section7.component_selection.get_mass_budget();
            fprintf('\nBILANCIO MASSA\n');
            fprintf('%s\n', repmat('-', 1, 50));
            fprintf('  MTOW:                   %s kg\n', fmt(mass_budget.mtow_kg, 2));
            fprintf('  f_propulsione:          %s\n', fmt(mass_budget.f_propulsion, 2));
            fprintf('  Budget propulsione:     %s kg\n', fmt(mass_budget.m_propulsion_kg, 3));
            fprintf('  Sistema lift (70%%):     %s kg\n', fmt(mass_budget.m_lift_kg, 3));
            fprintf('  Sistema crociera (30%%): %s kg\n', fmt(mass_budget.m_cruise_kg, 3));

            fprintf('\nCANDIDATI MOTORI LIFT\n');
            fprintf('%s\n', repmat('-', 1, 70));
            fprintf('%-25s %-8s %-8s %-6s %-15s\n', 'Modello', 'Massa', 'Potenza', 'KV', 'Esito');
            fprintf('%s\n', repmat('-', 1, 70));

            lift_results = mars_uav.section7.component_selection.evaluate_motor_candidates( ...
                mars_uav.section7.component_selection.get_lift_motor_candidates(), ...
                power_req.per_lift_motor_w, 100);

            for i = 1:numel(lift_results)
                r = lift_results(i);
                if strcmp(r.status, 'Idoneo')
                    status_mark = '[OK]';
                else
                    status_mark = '[X]';
                end
                fprintf('%-25s %-8s %-8s %-6s %s %s\n', ...
                    r.model, fmt(r.mass_g, 0), fmt(r.power_w, 0), fmt(r.kv, 0), status_mark, r.status);
            end

            fprintf('\nCANDIDATI MOTORI CROCIERA\n');
            fprintf('%s\n', repmat('-', 1, 70));
            fprintf('%-25s %-8s %-8s %-6s %-15s\n', 'Modello', 'Massa', 'Potenza', 'KV', 'Esito');
            fprintf('%s\n', repmat('-', 1, 70));

            cruise_results = mars_uav.section7.component_selection.evaluate_motor_candidates( ...
                mars_uav.section7.component_selection.get_cruise_motor_candidates(), ...
                power_req.per_cruise_motor_w, 100);

            for i = 1:numel(cruise_results)
                r = cruise_results(i);
                if strcmp(r.status, 'Idoneo')
                    status_mark = '[OK]';
                else
                    status_mark = '[X]';
                end
                fprintf('%-25s %-8s %-8s %-6s %s %s\n', ...
                    r.model, fmt(r.mass_g, 0), fmt(r.power_w, 0), fmt(r.kv, 0), status_mark, r.status);
            end

            selected = mars_uav.section7.component_selection.get_selected_components();
            fprintf('\nCOMPONENTI SELEZIONATI\n');
            fprintf('%s\n', repmat('-', 1, 50));
            fprintf('  Motore lift:    %s\n', selected.lift_motor.model);
            fprintf('  ESC lift:       %s\n', selected.lift_esc.model);
            fprintf('  Motore crociera:%s\n', selected.cruise_motor.model);
            fprintf('  ESC crociera:   %s\n', selected.cruise_esc.model);

            breakdown = mars_uav.section7.mass_breakdown.get_propulsion_mass_breakdown();
            fprintf('\nSINTESI MASSE PROPULSIONE\n');
            fprintf('%s\n', repmat('-', 1, 50));
            fprintf('  Sistema lift:    %s kg\n', fmt(breakdown.lift.subtotal_kg, 3));
            fprintf('  Sistema crociera:%s kg\n', fmt(breakdown.cruise.subtotal_kg, 3));
            fprintf('  Totale:          %s kg\n', fmt(breakdown.total_kg, 3));
            fprintf('  Budget:          %s kg\n', fmt(mass_budget.m_propulsion_kg, 3));
            margin = mass_budget.m_propulsion_kg - breakdown.total_kg;
            margin_pct = 100 * margin / mass_budget.m_propulsion_kg;
            margin_text = fmt(abs(margin), 3);
            if margin >= 0
                margin_text = ['+' margin_text];
            else
                margin_text = ['-' margin_text];
            end
            margin_pct_text = fmt(abs(margin_pct), 1);
            if margin_pct >= 0
                margin_pct_text = ['+' margin_pct_text];
            else
                margin_pct_text = ['-' margin_pct_text];
            end
            fprintf('  Margine:         %s kg (%s%%)\n', margin_text, margin_pct_text);

            if margin > 0
                fprintf('\n  [OK] Bilancio massa soddisfatto\n');
            else
                fprintf('\n  [NO] Bilancio massa superato\n');
            end

            fprintf('%s\n', repmat('=', 1, 70));
        end
    end
end

