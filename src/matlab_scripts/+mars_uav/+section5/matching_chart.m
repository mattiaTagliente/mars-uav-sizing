classdef matching_chart
    %MATCHING_CHART Analisi di dimensionamento basata su vincoli.

    methods(Static)
        function pw = hover_constraint()
            pw = mars_uav.section5.rotorcraft.hover_power_loading();
        end

        function ws_max = stall_constraint()
            rho = mars_uav.config.get_density();
            v_stall = mars_uav.config.get_mission_params().v_stall;
            v_min_factor = mars_uav.config.get_param('mission.velocity.v_min_factor');
            v_min = v_stall * v_min_factor;
            cl_max = mars_uav.config.get_aerodynamic_params().cl_max;
            ws_max = mars_uav.section5.fixed_wing.stall_wing_loading_limit(rho, v_min, cl_max);
        end

        function pw = cruise_constraint(wing_loading)
            rho = mars_uav.config.get_density();
            v_cruise = mars_uav.config.get_mission_params().v_cruise;

            cl = mars_uav.section5.fixed_wing.cruise_lift_coefficient(wing_loading, rho, v_cruise);
            ld_penalty = mars_uav.config.get_param('aerodynamic.quadplane.ld_penalty_factor');
            ld_pure = mars_uav.section5.fixed_wing.lift_to_drag(cl);
            ld = ld_pure * ld_penalty;

            pw = mars_uav.section5.fixed_wing.cruise_power_loading(v_cruise, ld);
        end

        function pw_curve = cruise_constraint_curve(ws_range)
            pw_curve = arrayfun(@(ws) mars_uav.section5.matching_chart.cruise_constraint(ws), ws_range);
        end

        function dp = find_design_point()
            pw_hover = mars_uav.section5.matching_chart.hover_constraint();
            ws_stall = mars_uav.section5.matching_chart.stall_constraint();
            pw_cruise_at_stall = mars_uav.section5.matching_chart.cruise_constraint(ws_stall);

            ws_design = ws_stall;
            pw_design = max(pw_hover, pw_cruise_at_stall);

            if pw_hover > pw_cruise_at_stall
                active_constraint = 'hover';
            else
                active_constraint = 'cruise';
            end

            dp = struct( ...
                'wing_loading', ws_design, ...
                'power_loading', pw_design, ...
                'hover_pw', pw_hover, ...
                'cruise_pw_at_stall', pw_cruise_at_stall, ...
                'stall_ws', ws_stall, ...
                'active_constraint', active_constraint ...
            );
        end

        function geom = derive_geometry(design_point)
            if nargin < 1 || isempty(design_point)
                design_point = mars_uav.section5.matching_chart.find_design_point();
            end

            g_mars = mars_uav.config.get_mars_gravity();
            mtow_kg = mars_uav.config.get_mtow();
            ar = mars_uav.config.get_aerodynamic_params().aspect_ratio;

            weight_n = mtow_kg * g_mars;
            ws = design_point.wing_loading;
            pw = design_point.power_loading;

            wing_area = weight_n / ws;
            wingspan = sqrt(ar * wing_area);
            chord = wing_area / wingspan;

            installed_power = pw * weight_n;

            disk_loading = mars_uav.config.get_param('geometry.rotor.disk_loading_N_m2');
            disk_area = weight_n / disk_loading;

            geom = struct( ...
                'wing_area_m2', wing_area, ...
                'wingspan_m', wingspan, ...
                'chord_m', chord, ...
                'installed_power_w', installed_power, ...
                'disk_area_m2', disk_area ...
            );
        end

        function results = matching_chart_analysis()
            g_mars = mars_uav.config.get_mars_gravity();
            rho = mars_uav.config.get_density();
            mtow_kg = mars_uav.config.get_mtow();
            prop = mars_uav.config.get_propulsion_efficiencies();
            aero = mars_uav.config.get_aerodynamic_params();
            mission = mars_uav.config.get_mission_params();
            disk_loading = mars_uav.config.get_param('geometry.rotor.disk_loading_N_m2');

            weight_n = mtow_kg * g_mars;

            pw_hover = mars_uav.section5.matching_chart.hover_constraint();
            ws_stall = mars_uav.section5.matching_chart.stall_constraint();

            design_point = mars_uav.section5.matching_chart.find_design_point();
            geometry = mars_uav.section5.matching_chart.derive_geometry(design_point);

            [ld_max, ~] = mars_uav.section5.fixed_wing.maximum_ld();
            ld_penalty = mars_uav.config.get_param('aerodynamic.quadplane.ld_penalty_factor');
            ld_quadplane = ld_max * ld_penalty;

            v_i = mars_uav.section5.rotorcraft.induced_velocity_from_disk_loading(disk_loading, rho);

            eta_hover = prop.figure_of_merit * prop.eta_motor * prop.eta_esc;
            eta_cruise = prop.eta_prop * prop.eta_motor * prop.eta_esc;

            ws_range = linspace(2.0, 15.0, 50);
            pw_cruise_curve = mars_uav.section5.matching_chart.cruise_constraint_curve(ws_range);
            pw_hover_line = pw_hover * ones(size(ws_range));

            results = struct( ...
                'mtow_kg', mtow_kg, ...
                'weight_n', weight_n, ...
                'rho_kg_m3', rho, ...
                'v_cruise_m_s', mission.v_cruise, ...
                'disk_loading_n_m2', disk_loading, ...
                'figure_of_merit', prop.figure_of_merit, ...
                'eta_hover', eta_hover, ...
                'eta_cruise', eta_cruise, ...
                'ld_max', ld_max, ...
                'ld_quadplane', ld_quadplane, ...
                'cl_max', aero.cl_max, ...
                'hover_pw', pw_hover, ...
                'stall_ws', ws_stall, ...
                'induced_velocity_m_s', v_i, ...
                'design_point', design_point, ...
                'geometry', geometry, ...
                'ws_range', ws_range, ...
                'pw_cruise_curve', pw_cruise_curve, ...
                'pw_hover_line', pw_hover_line ...
            );
        end

        function print_analysis(results)
            if nargin < 1 || isempty(results)
                results = mars_uav.section5.matching_chart.matching_chart_analysis();
            end

            dp = results.design_point;
            geom = results.geometry;
            fmt = @(value, decimals) mars_uav.core.format_number(value, decimals);

            fprintf('%s\n', repmat('=', 1, 80));
            fprintf('ANALISI DIAGRAMMA DI MATCHING (Sezione 5.4)\n');
            fprintf('%s\n', repmat('=', 1, 80));
            fprintf('Calcolato: %s\n', datestr(now, 'yyyy-mm-dd HH:MM:SS'));
            fprintf('Config:    Valori da file YAML in config/\n\n');

            fprintf('PARAMETRI DI INGRESSO\n');
            fprintf('%s\n', repmat('-', 1, 50));
            fprintf('  MTOW:               %s kg\n', fmt(results.mtow_kg, 2));
            fprintf('  Peso:               %s N\n', fmt(results.weight_n, 2));
            fprintf('  Densita aria:       %s kg/m^3\n', fmt(results.rho_kg_m3, 4));
            fprintf('  Velocita crociera:  %s m/s\n', fmt(results.v_cruise_m_s, 1));
            fprintf('  Carico disco:       %s N/m^2\n\n', fmt(results.disk_loading_n_m2, 1));

            fprintf('VALORI DEI VINCOLI\n');
            fprintf('%s\n', repmat('-', 1, 50));
            fprintf('  P/W hovering:       %s W/N (linea orizzontale)\n', fmt(results.hover_pw, 2));
            fprintf('  Limite W/S stallo:  %s N/m^2 (linea verticale)\n\n', fmt(results.stall_ws, 2));

            fprintf('PUNTO DI PROGETTO (intersezione vincoli)\n');
            fprintf('%s\n', repmat('-', 1, 50));
            fprintf('  Carico alare:       %s N/m^2\n', fmt(dp.wing_loading, 2));
            fprintf('  Carico di potenza:  %s W/N\n', fmt(dp.power_loading, 2));
            active_label = dp.active_constraint;
            if strcmp(active_label, 'hover')
                active_label = 'hovering';
            elseif strcmp(active_label, 'cruise')
                active_label = 'crociera';
            end
            fprintf('  Vincolo attivo:     %s\n\n', upper(active_label));

            fprintf('GEOMETRIA DERIVATA\n');
            fprintf('%s\n', repmat('-', 1, 50));
            fprintf('  Superficie alare:   %s m^2\n', fmt(geom.wing_area_m2, 3));
            fprintf('  Apertura alare:     %s m\n', fmt(geom.wingspan_m, 2));
            fprintf('  Corda media:        %s m\n', fmt(geom.chord_m, 3));
            fprintf('  Potenza installata: %s W (hovering)\n', fmt(geom.installed_power_w, 0));
            fprintf('  Area disco:         %s m^2\n\n', fmt(geom.disk_area_m2, 3));

            fprintf('SINTESI\n');
            fprintf('%s\n', repmat('-', 1, 50));
            fprintf('  Il diagramma di matching indica che:\n');
            fprintf('  1. Il vincolo di hovering domina a P/W = %s W/N\n', fmt(results.hover_pw, 1));
            fprintf('  2. Il vincolo di stallo limita W/S a %s N/m^2\n', fmt(results.stall_ws, 1));
            fprintf('  3. La potenza in crociera (%s W/N) e ~%s volte inferiore all''hovering\n', ...
                fmt(dp.cruise_pw_at_stall, 1), ...
                fmt(results.hover_pw / dp.cruise_pw_at_stall, 0));
            fprintf('  -> Il progetto e dominato dall''hovering; potenza in crociera abbondante\n\n');

            fprintf('%s\n', repmat('=', 1, 80));
        end
    end
end

