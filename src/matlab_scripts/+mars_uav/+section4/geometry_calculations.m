classdef geometry_calculations
    %GEOMETRY_CALCULATIONS Calcoli di geometria (Sezione 4).

    methods(Static)
        function [v_h, v_v] = tail_volume_coefficients()
            %TAIL_VOLUME_COEFFICIENTS Coefficienti di volume di coda.
            v_h = mars_uav.config.get_param('geometry.tail.v_h');
            v_v = mars_uav.config.get_param('geometry.tail.v_v');
        end

        function s_h = horizontal_tail_area(wing_area, mac, moment_arm, v_h)
            %HORIZONTAL_TAIL_AREA Area di coda orizzontale richiesta.
            if nargin < 4 || isempty(v_h)
                v_h = mars_uav.config.get_param('geometry.tail.v_h');
            end
            s_h = v_h * wing_area * mac / moment_arm;
        end

        function s_v = vertical_tail_area(wing_area, wingspan, moment_arm, v_v)
            %VERTICAL_TAIL_AREA Area di coda verticale richiesta.
            if nargin < 4 || isempty(v_v)
                v_v = mars_uav.config.get_param('geometry.tail.v_v');
            end
            s_v = v_v * wing_area * wingspan / moment_arm;
        end

        function vtail = vtail_geometry(sh_required, sv_required, dihedral_deg, aspect_ratio)
            %VTAIL_GEOMETRY Geometria V-tail da aree proiettate.
            if nargin < 3 || isempty(dihedral_deg)
                dihedral_deg = mars_uav.config.get_param('geometry.tail.vtail_dihedral_deg');
            end
            if nargin < 4 || isempty(aspect_ratio)
                aspect_ratio = mars_uav.config.get_param('geometry.tail.vtail_aspect_ratio');
            end

            dihedral_rad = deg2rad(dihedral_deg);
            cos2_gamma = cos(dihedral_rad)^2;
            sin2_gamma = sin(dihedral_rad)^2;

            s_vtail_from_h = sh_required / cos2_gamma;
            s_vtail_from_v = sv_required / sin2_gamma;
            s_vtail_total = max(s_vtail_from_h, s_vtail_from_v);
            s_per_surface = s_vtail_total / 2;

            span_per_surface = sqrt(aspect_ratio * s_per_surface);
            chord = s_per_surface / span_per_surface;

            vtail = struct( ...
                's_vtail_total', s_vtail_total, ...
                's_per_surface', s_per_surface, ...
                'dihedral_deg', dihedral_deg, ...
                'span_per_surface', span_per_surface, ...
                'chord', chord, ...
                'aspect_ratio', aspect_ratio, ...
                'actual_sh', s_vtail_total * cos2_gamma, ...
                'actual_sv', s_vtail_total * sin2_gamma ...
            );
        end

        function length_m = fuselage_length(wingspan, ratio)
            %FUSELAGE_LENGTH Lunghezza fusoliera da rapporto con apertura.
            if nargin < 2 || isempty(ratio)
                ratio = mars_uav.config.get_param('geometry.fuselage.length_to_span_ratio');
            end
            length_m = ratio * wingspan;
        end

        function diameter_m = rotor_diameter(total_thrust, n_rotors, disk_loading)
            %ROTOR_DIAMETER Diametro rotore da carico del disco.
            if nargin < 3 || isempty(disk_loading)
                disk_loading = mars_uav.config.get_param('geometry.rotor.disk_loading_N_m2');
            end
            area_per_rotor = (total_thrust / n_rotors) / disk_loading;
            diameter_m = sqrt(4 * area_per_rotor / pi);
        end

        function area_m2 = total_disk_area(thrust, disk_loading)
            %TOTAL_DISK_AREA Area totale del disco.
            if nargin < 2 || isempty(disk_loading)
                disk_loading = mars_uav.config.get_param('geometry.rotor.disk_loading_N_m2');
            end
            area_m2 = thrust / disk_loading;
        end

        function results = geometry_analysis()
            %GEOMETRY_ANALYSIS Analisi completa della geometria.
            g = mars_uav.config.get_param('physical.mars.g');
            mtow = mars_uav.config.get_param('mission.mass.mtow_kg');
            weight_n = mtow * g;
            ar = mars_uav.config.get_param('aerodynamic.wing.aspect_ratio');

            ws = mars_uav.section4.derived_requirements.maximum_wing_loading();
            s = mars_uav.section4.derived_requirements.wing_area_from_loading(mtow, ws);
            b = mars_uav.section4.derived_requirements.wingspan_from_area(s, ar);
            c = mars_uav.section4.derived_requirements.mean_chord(s, b);

            l_fus = mars_uav.section4.geometry_calculations.fuselage_length(b);

            moment_arm_ratio = mars_uav.config.get_param('geometry.tail.moment_arm_ratio');
            moment_arm = moment_arm_ratio * l_fus;
            sh = mars_uav.section4.geometry_calculations.horizontal_tail_area(s, c, moment_arm);
            sv = mars_uav.section4.geometry_calculations.vertical_tail_area(s, b, moment_arm);
            vtail = mars_uav.section4.geometry_calculations.vtail_geometry(sh, sv);

            n_rotors = mars_uav.config.get_param('geometry.rotor.n_rotors', []);
            if isempty(n_rotors)
                n_rotors = mars_uav.config.get_param('geometry.propulsion_config.lift.n_rotors');
            end
            d_rotor = mars_uav.section4.geometry_calculations.rotor_diameter(weight_n, n_rotors);

            results = struct( ...
                'wing_loading_n_m2', ws, ...
                'wing_area_m2', s, ...
                'wingspan_m', b, ...
                'mean_chord_m', c, ...
                'fuselage_length_m', l_fus, ...
                'moment_arm_ratio', moment_arm_ratio, ...
                'moment_arm_m', moment_arm, ...
                'sh_required_m2', sh, ...
                'sv_required_m2', sv, ...
                'vtail', vtail, ...
                'n_rotors', n_rotors, ...
                'rotor_diameter_m', d_rotor, ...
                'total_disk_area_m2', mars_uav.section4.geometry_calculations.total_disk_area(weight_n) ...
            );
        end

        function print_analysis()
            %PRINT_ANALYSIS Stampa analisi geometria.
            results = mars_uav.section4.geometry_calculations.geometry_analysis();
            timestamp = datestr(now, 'yyyy-mm-dd HH:MM:SS');
            fmt = @(value, decimals) mars_uav.core.format_number(value, decimals);

            fprintf('%s\n', repmat('=', 1, 80));
            fprintf('CALCOLI GEOMETRIA (Sezione 4)\n');
            fprintf('%s\n', repmat('=', 1, 80));
            fprintf('Calcolato: %s\n', timestamp);
            fprintf('Config:    Parametri da file YAML in config/\n\n');

            fprintf('GEOMETRIA ALA (da vincolo stallo)\n');
            fprintf('%s\n', repmat('-', 1, 50));
            fprintf('  Carico alare:      %s N/m^2\n', fmt(results.wing_loading_n_m2, 2));
            fprintf('  Superficie alare:  %s m^2\n', fmt(results.wing_area_m2, 3));
            fprintf('  Apertura alare:    %s m\n', fmt(results.wingspan_m, 2));
            fprintf('  Corda media:       %s m\n\n', fmt(results.mean_chord_m, 3));

            fprintf('GEOMETRIA FUSOLIERA\n');
            fprintf('%s\n', repmat('-', 1, 50));
            fprintf('  Lunghezza fusoliera: %s m\n\n', fmt(results.fuselage_length_m, 2));

            fprintf('GEOMETRIA CODA\n');
            fprintf('%s\n', repmat('-', 1, 50));
            fprintf('  Rapporto braccio:  %s\n', fmt(results.moment_arm_ratio, 2));
            fprintf('  Braccio di coda:   %s m\n', fmt(results.moment_arm_m, 2));
            fprintf('  S_H richiesta:     %s m^2\n', fmt(results.sh_required_m2, 3));
            fprintf('  S_V richiesta:     %s m^2\n', fmt(results.sv_required_m2, 3));
            vtail = results.vtail;
            fprintf('  Area V-tail totale:%s m^2\n', fmt(vtail.s_vtail_total, 3));
            fprintf('  Dihedro V-tail:    %s deg\n', fmt(vtail.dihedral_deg, 0));
            fprintf('  AR V-tail:         %s\n', fmt(vtail.aspect_ratio, 1));
            fprintf('  Semi-apertura:     %s m\n', fmt(vtail.span_per_surface, 2));
            fprintf('  Corda V-tail:      %s m\n\n', fmt(vtail.chord, 3));

            fprintf('GEOMETRIA ROTORI\n');
            fprintf('%s\n', repmat('-', 1, 50));
            fprintf('  Numero rotori:     %s\n', fmt(results.n_rotors, 0));
            fprintf('  Diametro rotore:   %s m (%s in)\n', ...
                fmt(results.rotor_diameter_m, 3), fmt(results.rotor_diameter_m * 39.37, 1));
            fprintf('  Area disco totale: %s m^2\n', fmt(results.total_disk_area_m2, 3));
            fprintf('%s\n', repmat('=', 1, 80));
        end
    end
end
