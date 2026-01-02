classdef aerodynamic_calculations
    %AERODYNAMIC_CALCULATIONS Calcoli aerodinamici (Sezione 4.7).

    methods(Static)
        function e = oswald_efficiency_sadraey(aspect_ratio)
            %OSWALD_EFFICIENCY_SADRAEY Correlazione di Sadraey.
            e = 1.78 * (1 - 0.045 * aspect_ratio^0.68) - 0.64;
        end

        function k = induced_drag_factor(aspect_ratio, oswald_e)
            %INDUCED_DRAG_FACTOR Fattore di resistenza indotta.
            if nargin < 1 || isempty(aspect_ratio)
                aspect_ratio = mars_uav.config.get_param('aerodynamic.wing.aspect_ratio');
            end
            if nargin < 2 || isempty(oswald_e)
                oswald_e = mars_uav.config.get_param('aerodynamic.wing.oswald_efficiency');
            end
            k = 1 / (pi * aspect_ratio * oswald_e);
        end

        function cd = drag_coefficient(c_l, cd0, k)
            %DRAG_COEFFICIENT Polare parabolica di resistenza.
            if nargin < 2 || isempty(cd0)
                cd0 = mars_uav.config.get_param('aerodynamic.drag_polar.cd0');
            end
            if nargin < 3 || isempty(k)
                k = mars_uav.section4.aerodynamic_calculations.induced_drag_factor();
            end
            cd = cd0 + k * c_l.^2;
        end

        function ld = lift_to_drag(c_l, cd0, k)
            %LIFT_TO_DRAG Rapporto portanza/resistenza.
            cd = mars_uav.section4.aerodynamic_calculations.drag_coefficient(c_l, cd0, k);
            if cd == 0
                ld = 0;
            else
                ld = c_l / cd;
            end
        end

        function [ld_max, cl_opt] = maximum_ld()
            %MAXIMUM_LD Massimo L/D e CL ottimo.
            ar = mars_uav.config.get_param('aerodynamic.wing.aspect_ratio');
            e = mars_uav.config.get_param('aerodynamic.wing.oswald_efficiency');
            cd0 = mars_uav.config.get_param('aerodynamic.drag_polar.cd0');

            cl_opt = sqrt(cd0 * pi * ar * e);
            ld_max = 0.5 * sqrt(pi * ar * e / cd0);
        end

        function ld_qp = quadplane_ld()
            %QUADPLANE_LD Efficienza L/D con penalita rotori fermi.
            [ld_max, ~] = mars_uav.section4.aerodynamic_calculations.maximum_ld();
            penalty = mars_uav.config.get_param('aerodynamic.quadplane.ld_penalty_factor');
            ld_qp = ld_max * penalty;
        end

        function results = drag_polar_analysis()
            %DRAG_POLAR_ANALYSIS Analisi completa della polare.
            ar = mars_uav.config.get_param('aerodynamic.wing.aspect_ratio');
            e = mars_uav.config.get_param('aerodynamic.wing.oswald_efficiency');
            cd0 = mars_uav.config.get_param('aerodynamic.drag_polar.cd0');

            k = mars_uav.section4.aerodynamic_calculations.induced_drag_factor(ar, e);
            [ld_max, cl_opt] = mars_uav.section4.aerodynamic_calculations.maximum_ld();
            ld_qp = mars_uav.section4.aerodynamic_calculations.quadplane_ld();
            ld_rotor = mars_uav.config.get_param('aerodynamic.rotorcraft.ld_effective');
            e_sadraey = mars_uav.section4.aerodynamic_calculations.oswald_efficiency_sadraey(ar);

            results = struct( ...
                'aspect_ratio', ar, ...
                'oswald_e', e, ...
                'oswald_e_sadraey', e_sadraey, ...
                'cd0', cd0, ...
                'k', k, ...
                'ld_max', ld_max, ...
                'cl_optimal', cl_opt, ...
                'ld_quadplane', ld_qp, ...
                'ld_rotorcraft', ld_rotor ...
            );
        end

        function print_analysis()
            %PRINT_ANALYSIS Stampa analisi aerodinamica.
            results = mars_uav.section4.aerodynamic_calculations.drag_polar_analysis();
            timestamp = datestr(now, 'yyyy-mm-dd HH:MM:SS');
            fmt = @(value, decimals) mars_uav.core.format_number(value, decimals);

            fprintf('%s\n', repmat('=', 1, 80));
            fprintf('CALCOLI AERODINAMICI (Sezione 4.7)\n');
            fprintf('%s\n', repmat('=', 1, 80));
            fprintf('Calcolato: %s\n', timestamp);
            fprintf('Config:    Parametri da config/aerodynamic_parameters.yaml\n\n');

            fprintf('PARAMETRI ALA\n');
            fprintf('%s\n', repmat('-', 1, 50));
            fprintf('  Rapporto d''aspetto: %s\n', fmt(results.aspect_ratio, 2));
            fprintf('  Efficienza Oswald:  %s (config)\n', fmt(results.oswald_e, 4));
            fprintf('  Correlazione Sadraey: %s\n\n', fmt(results.oswald_e_sadraey, 4));

            fprintf('POLARE DI RESISTENZA\n');
            fprintf('%s\n', repmat('-', 1, 50));
            fprintf('  C_D0:              %s\n', fmt(results.cd0, 4));
            fprintf('  K = 1/(pi AR e):   %s\n', fmt(results.k, 4));
            fprintf('  C_D = C_D0 + K * C_L^2\n\n');

            fprintf('EFFICIENZA AERODINAMICA\n');
            fprintf('%s\n', repmat('-', 1, 50));
            fprintf('  (L/D)_max:         %s\n', fmt(results.ld_max, 2));
            fprintf('  C_L ottimo:        %s\n\n', fmt(results.cl_optimal, 3));

            fprintf('CONFIGURAZIONI\n');
            fprintf('%s\n', repmat('-', 1, 50));
            fprintf('  Ala fissa:         %s\n', fmt(results.ld_max, 2));
            fprintf('  QuadPlane:         %s (penalita)\n', fmt(results.ld_quadplane, 2));
            fprintf('  Velivolo a rotore: %s\n', fmt(results.ld_rotorcraft, 1));
            fprintf('%s\n', repmat('=', 1, 80));
        end
    end
end
