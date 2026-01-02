classdef tail_sizing
    %TAIL_SIZING Calcoli di dimensionamento V-tail.

    methods(Static)
        function wing = get_wing_geometry()
            geom = mars_uav.section5.matching_chart.derive_geometry();
            wing = struct( ...
                'wing_area_m2', geom.wing_area_m2, ...
                'wingspan_m', geom.wingspan_m, ...
                'chord_m', geom.chord_m ...
            );
        end

        function fus = get_fuselage_geometry()
            wingspan = mars_uav.section6.tail_sizing.get_wing_geometry().wingspan_m;
            length_ratio = mars_uav.config.get_param('design.fuselage.length_to_span_ratio');
            fineness = mars_uav.config.get_param('design.fuselage.fineness_ratio');

            length_m = length_ratio * wingspan;
            diameter_m = length_m / fineness;

            fus = struct( ...
                'length_m', length_m, ...
                'diameter_m', diameter_m, ...
                'fineness_ratio', fineness, ...
                'length_to_span_ratio', length_ratio ...
            );
        end

        function results = vtail_sizing()
            wing = mars_uav.section6.tail_sizing.get_wing_geometry();
            S_wing = wing.wing_area_m2;
            b_wing = wing.wingspan_m;
            mac = wing.chord_m;

            fus = mars_uav.section6.tail_sizing.get_fuselage_geometry();
            L_fus = fus.length_m;

            V_H = mars_uav.config.get_param('geometry.tail.v_h');
            V_V = mars_uav.config.get_param('geometry.tail.v_v');
            gamma_deg = mars_uav.config.get_param('geometry.tail.vtail_dihedral_deg');
            AR_tail = mars_uav.config.get_param('geometry.tail.vtail_aspect_ratio');
            arm_ratio = mars_uav.config.get_param('geometry.tail.moment_arm_ratio');

            l_tail = arm_ratio * L_fus;

            S_H_required = (V_H * S_wing * mac) / l_tail;
            S_V_required = (V_V * S_wing * b_wing) / l_tail;

            gamma_rad = deg2rad(gamma_deg);
            cos_gamma = cos(gamma_rad);
            sin_gamma = sin(gamma_rad);

            S_vtail_from_H = S_H_required / (cos_gamma ^ 2);
            S_vtail_from_V = S_V_required / (sin_gamma ^ 2);
            S_vtail_total = max(S_vtail_from_H, S_vtail_from_V);

            S_vtail_per_surface = S_vtail_total / 2;
            b_vtail = sqrt(AR_tail * S_vtail_total);
            b_vtail_per_surface = b_vtail / 2;
            c_vtail = S_vtail_total / b_vtail;

            S_H_actual = S_vtail_total * (cos_gamma ^ 2);
            S_V_actual = S_vtail_total * (sin_gamma ^ 2);

            V_H_actual = (S_H_actual * l_tail) / (S_wing * mac);
            V_V_actual = (S_V_actual * l_tail) / (S_wing * b_wing);

            if S_vtail_from_H >= S_vtail_from_V
                active_constraint = 'orizzontale (beccheggio)';
            else
                active_constraint = 'verticale (imbardata)';
            end

            results = struct( ...
                'wing_area_m2', S_wing, ...
                'wingspan_m', b_wing, ...
                'mac_m', mac, ...
                'fuselage_length_m', L_fus, ...
                'moment_arm_m', l_tail, ...
                'moment_arm_ratio', arm_ratio, ...
                'dihedral_deg', gamma_deg, ...
                'aspect_ratio', AR_tail, ...
                'V_H_target', V_H, ...
                'V_V_target', V_V, ...
                'S_H_required_m2', S_H_required, ...
                'S_V_required_m2', S_V_required, ...
                'S_vtail_total_m2', S_vtail_total, ...
                'S_vtail_per_surface_m2', S_vtail_per_surface, ...
                'b_vtail_m', b_vtail, ...
                'b_vtail_per_surface_m', b_vtail_per_surface, ...
                'c_vtail_m', c_vtail, ...
                'S_H_actual_m2', S_H_actual, ...
                'S_V_actual_m2', S_V_actual, ...
                'V_H_actual', V_H_actual, ...
                'V_V_actual', V_V_actual, ...
                'active_constraint', active_constraint ...
            );
        end

        function print_analysis(results)
            if nargin < 1 || isempty(results)
                results = mars_uav.section6.tail_sizing.vtail_sizing();
            end
            fmt = @(value, decimals) mars_uav.core.format_number(value, decimals);

            fprintf('%s\n', repmat('=', 1, 70));
            fprintf('ANALISI DIMENSIONAMENTO CODA (Sezione 6.3)\n');
            fprintf('%s\n', repmat('=', 1, 70));
            fprintf('Calcolato: %s\n', datestr(now, 'yyyy-mm-dd HH:MM:SS'));
            fprintf('Config:    Valori da file YAML in config/\n\n');

            fprintf('GEOMETRIA ALA DI RIFERIMENTO\n');
            fprintf('%s\n', repmat('-', 1, 50));
            fprintf('  Superficie alare:      %s m^2\n', fmt(results.wing_area_m2, 3));
            fprintf('  Apertura alare:        %s m\n', fmt(results.wingspan_m, 2));
            fprintf('  Corda media:           %s m\n\n', fmt(results.mac_m, 3));

            fprintf('FUSOLIERA DI RIFERIMENTO\n');
            fprintf('%s\n', repmat('-', 1, 50));
            fprintf('  Lunghezza fusoliera:   %s m\n', fmt(results.fuselage_length_m, 2));
            fprintf('  Braccio di coda:       %s m\n', fmt(results.moment_arm_m, 2));
            fprintf('  Rapporto braccio/L:    %s\n\n', fmt(results.moment_arm_ratio, 2));

            fprintf('COEFFICIENTI DI VOLUME\n');
            fprintf('%s\n', repmat('-', 1, 50));
            fprintf('  V_H (target):          %s\n', fmt(results.V_H_target, 3));
            fprintf('  V_V (target):          %s\n', fmt(results.V_V_target, 4));
            fprintf('  V_H (effettivo):       %s\n', fmt(results.V_H_actual, 3));
            fprintf('  V_V (effettivo):       %s\n\n', fmt(results.V_V_actual, 4));

            fprintf('GEOMETRIA V-TAIL\n');
            fprintf('%s\n', repmat('-', 1, 50));
            fprintf('  Angolo dihedro:        %s deg\n', fmt(results.dihedral_deg, 0));
            fprintf('  Rapporto d''aspetto:    %s\n', fmt(results.aspect_ratio, 1));
            fprintf('  Area planare totale:   %s m^2\n', fmt(results.S_vtail_total_m2, 3));
            fprintf('  Area per superficie:   %s m^2\n', fmt(results.S_vtail_per_surface_m2, 3));
            fprintf('  Apertura totale:       %s m\n', fmt(results.b_vtail_m, 2));
            fprintf('  Semi-apertura per sup.: %s m\n', fmt(results.b_vtail_per_surface_m, 2));
            fprintf('  Corda media:           %s m\n\n', fmt(results.c_vtail_m, 3));

            fprintf('SINTESI DIMENSIONAMENTO\n');
            fprintf('%s\n', repmat('-', 1, 50));
            fprintf('  Vincolo attivo:        %s\n', results.active_constraint);
            fprintf('  S_H richiesta:         %s m^2\n', fmt(results.S_H_required_m2, 3));
            fprintf('  S_V richiesta:         %s m^2\n', fmt(results.S_V_required_m2, 3));
            fprintf('  S_H fornita:           %s m^2\n', fmt(results.S_H_actual_m2, 3));
            fprintf('  S_V fornita:           %s m^2\n\n', fmt(results.S_V_actual_m2, 3));

            S_ratio = results.S_vtail_total_m2 / results.wing_area_m2;
            fprintf('  S_coda / S_ala:        %s%%\n\n', fmt(S_ratio * 100, 2));

            fprintf('%s\n', repmat('=', 1, 70));
        end
    end
end

