classdef derived_requirements
    %DERIVED_REQUIREMENTS Requisiti derivati (Sezione 4.12).

    methods(Static)
        function v_stall = stall_speed(wing_loading)
            %STALL_SPEED Velocita di stallo da carico alare.
            if nargin < 1 || isempty(wing_loading)
                wing_loading = mars_uav.section4.derived_requirements.wing_loading_from_reynolds();
            end
            rho = mars_uav.config.get_param('environment.arcadia_planitia.density_kg_m3');
            cl_max = mars_uav.config.get_param('aerodynamic.airfoil.cl_max');
            v_stall = sqrt(2 * wing_loading / (rho * cl_max));
        end

        function v_min = minimum_flight_speed(wing_loading)
            %MINIMUM_FLIGHT_SPEED Velocita minima con fattore di margine.
            v_stall = mars_uav.section4.derived_requirements.stall_speed(wing_loading);
            factor = mars_uav.config.get_param('mission.velocity.v_min_factor');
            v_min = factor * v_stall;
        end

        function ws_max = maximum_wing_loading(v_min)
            %MAXIMUM_WING_LOADING Limite massimo W/S da stallo.
            if nargin < 1 || isempty(v_min)
                v_stall = mars_uav.config.get_param('mission.velocity.v_stall_m_s');
                factor = mars_uav.config.get_param('mission.velocity.v_min_factor');
                v_min = v_stall * factor;
            end
            rho = mars_uav.config.get_param('environment.arcadia_planitia.density_kg_m3');
            cl_max = mars_uav.config.get_param('aerodynamic.airfoil.cl_max');
            ws_max = 0.5 * rho * v_min^2 * cl_max;
        end

        function chord = chord_from_reynolds(target_re)
            %CHORD_FROM_REYNOLDS Corda media richiesta per Re target.
            if nargin < 1 || isempty(target_re)
                target_re = 60000;
            end
            rho = mars_uav.config.get_param('environment.arcadia_planitia.density_kg_m3');
            v_cruise = mars_uav.config.get_param('mission.velocity.v_cruise_m_s');
            mu = mars_uav.config.get_param('environment.arcadia_planitia.viscosity_Pa_s');
            chord = target_re * mu / (rho * v_cruise);
        end

        function wing_area = wing_area_from_reynolds(target_re, aspect_ratio)
            %WING_AREA_FROM_REYNOLDS Area alare da Re target e AR.
            if nargin < 1 || isempty(target_re)
                target_re = 60000;
            end
            if nargin < 2 || isempty(aspect_ratio)
                aspect_ratio = mars_uav.config.get_param('aerodynamic.wing.aspect_ratio');
            end
            chord = mars_uav.section4.derived_requirements.chord_from_reynolds(target_re);
            wing_area = chord^2 * aspect_ratio;
        end

        function ws = wing_loading_from_reynolds(mtow_kg, target_re)
            %WING_LOADING_FROM_REYNOLDS W/S coerente con Re target.
            if nargin < 1 || isempty(mtow_kg)
                mtow_kg = mars_uav.config.get_param('mission.mass.mtow_kg');
            end
            if nargin < 2 || isempty(target_re)
                target_re = 60000;
            end
            g = mars_uav.config.get_param('physical.mars.g');
            weight_n = mtow_kg * g;
            wing_area = mars_uav.section4.derived_requirements.wing_area_from_reynolds(target_re);
            ws = weight_n / wing_area;
        end

        function re = cruise_reynolds(chord)
            %CRUISE_REYNOLDS Numero di Reynolds in crociera.
            if nargin < 1 || isempty(chord)
                chord = mars_uav.config.get_param('aerodynamic.wing.mean_chord_m');
            end
            rho = mars_uav.config.get_param('environment.arcadia_planitia.density_kg_m3');
            v_cruise = mars_uav.config.get_param('mission.velocity.v_cruise_m_s');
            mu = mars_uav.config.get_param('environment.arcadia_planitia.viscosity_Pa_s');
            re = rho * v_cruise * chord / mu;
        end

        function mach = cruise_mach()
            %CRUISE_MACH Numero di Mach in crociera.
            v_cruise = mars_uav.config.get_param('mission.velocity.v_cruise_m_s');
            a = mars_uav.config.get_param('environment.arcadia_planitia.speed_of_sound_m_s');
            mach = v_cruise / a;
        end

        function wing_area = wing_area_from_loading(mtow_kg, wing_loading)
            %WING_AREA_FROM_LOADING Area alare da MTOW e W/S.
            if nargin < 1 || isempty(mtow_kg)
                mtow_kg = mars_uav.config.get_param('mission.mass.mtow_kg');
            end
            if nargin < 2 || isempty(wing_loading)
                wing_loading = mars_uav.section4.derived_requirements.maximum_wing_loading();
            end
            g = mars_uav.config.get_param('physical.mars.g');
            weight_n = mtow_kg * g;
            wing_area = weight_n / wing_loading;
        end

        function wingspan = wingspan_from_area(wing_area, aspect_ratio)
            %WINGSPAN_FROM_AREA Apertura alare da area e AR.
            if nargin < 2 || isempty(aspect_ratio)
                aspect_ratio = mars_uav.config.get_param('aerodynamic.wing.aspect_ratio');
            end
            wingspan = sqrt(aspect_ratio * wing_area);
        end

        function chord = mean_chord(wing_area, wingspan)
            %MEAN_CHORD Corda media aerodinamica.
            chord = wing_area / wingspan;
        end

        function results = derived_requirements_analysis()
            %DERIVED_REQUIREMENTS_ANALYSIS Analisi requisiti derivati.
            g = mars_uav.config.get_param('physical.mars.g');
            mtow_kg = mars_uav.config.get_param('mission.mass.mtow_kg');
            weight_n = mtow_kg * g;
            ar = mars_uav.config.get_param('aerodynamic.wing.aspect_ratio');

            v_cruise = mars_uav.config.get_param('mission.velocity.v_cruise_m_s');
            v_min_factor = mars_uav.config.get_param('mission.velocity.v_min_factor');

            target_re = 60000;
            chord_re = mars_uav.section4.derived_requirements.chord_from_reynolds(target_re);
            wing_area_re = mars_uav.section4.derived_requirements.wing_area_from_reynolds(target_re, ar);
            wingspan_re = mars_uav.section4.derived_requirements.wingspan_from_area(wing_area_re, ar);
            ws_re = mars_uav.section4.derived_requirements.wing_loading_from_reynolds(mtow_kg, target_re);
            v_stall_re = mars_uav.section4.derived_requirements.stall_speed(ws_re);
            v_min_re = v_stall_re * v_min_factor;

            v_stall_config = mars_uav.config.get_param('mission.velocity.v_stall_m_s');
            v_min_stall = v_stall_config * v_min_factor;
            ws_stall = mars_uav.section4.derived_requirements.maximum_wing_loading(v_min_stall);
            wing_area_stall = mars_uav.section4.derived_requirements.wing_area_from_loading(mtow_kg, ws_stall);
            wingspan_stall = mars_uav.section4.derived_requirements.wingspan_from_area(wing_area_stall, ar);
            chord_stall = mars_uav.section4.derived_requirements.mean_chord(wing_area_stall, wingspan_stall);
            re_stall = mars_uav.section4.derived_requirements.cruise_reynolds(chord_stall);

            mach = mars_uav.section4.derived_requirements.cruise_mach();

            results = struct( ...
                'mtow_kg', mtow_kg, ...
                'weight_n', weight_n, ...
                'v_cruise_m_s', v_cruise, ...
                'v_min_factor', v_min_factor, ...
                'target_reynolds', target_re, ...
                're_chord_m', chord_re, ...
                're_wing_area_m2', wing_area_re, ...
                're_wingspan_m', wingspan_re, ...
                're_wing_loading', ws_re, ...
                're_v_stall_m_s', v_stall_re, ...
                're_v_min_m_s', v_min_re, ...
                'stall_v_stall_m_s', v_stall_config, ...
                'stall_v_min_m_s', v_min_stall, ...
                'stall_wing_loading', ws_stall, ...
                'stall_wing_area_m2', wing_area_stall, ...
                'stall_wingspan_m', wingspan_stall, ...
                'stall_chord_m', chord_stall, ...
                'stall_reynolds', re_stall, ...
                'mach_cruise', mach, ...
                'aspect_ratio', ar ...
            );
        end

        function print_analysis()
            %PRINT_ANALYSIS Stampa analisi requisiti derivati.
            results = mars_uav.section4.derived_requirements.derived_requirements_analysis();
            timestamp = datestr(now, 'yyyy-mm-dd HH:MM:SS');
            fmt = @(value, decimals) mars_uav.core.format_number(value, decimals);

            fprintf('%s\n', repmat('=', 1, 80));
            fprintf('REQUISITI DERIVATI (Sezione 4.12)\n');
            fprintf('%s\n', repmat('=', 1, 80));
            fprintf('Calcolato: %s\n', timestamp);
            fprintf('Config:    Parametri da file YAML in config/\n\n');

            fprintf('MASSA E PESO\n');
            fprintf('%s\n', repmat('-', 1, 50));
            fprintf('  MTOW:              %s kg\n', fmt(results.mtow_kg, 2));
            fprintf('  Peso (Marte):      %s N\n', fmt(results.weight_n, 2));
            fprintf('  Rapporto d''aspetto: %s\n\n', fmt(results.aspect_ratio, 2));

            fprintf('REQUISITI VELOCITA\n');
            fprintf('%s\n', repmat('-', 1, 50));
            fprintf('  V_crociera:        %s m/s\n', fmt(results.v_cruise_m_s, 2));
            fprintf('  Fattore V_min:     %s\n', fmt(results.v_min_factor, 2));
            fprintf('  Mach crociera:     %s\n\n', fmt(results.mach_cruise, 4));

            fprintf('%s\n', repmat('=', 1, 80));
            fprintf('DERIVAZIONE 1: Re target (Sezione 4.12)\n');
            fprintf('%s\n', repmat('=', 1, 80));
            fprintf('  Re target:         %s\n', fmt(results.target_reynolds, 0));
            fprintf('  Corda richiesta:   %s m\n', fmt(results.re_chord_m, 4));
            fprintf('  Superficie alare:  %s m^2\n', fmt(results.re_wing_area_m2, 4));
            fprintf('  Apertura alare:    %s m\n', fmt(results.re_wingspan_m, 4));
            fprintf('  Carico alare:      %s N/m^2\n', fmt(results.re_wing_loading, 4));
            fprintf('  V_stallo:          %s m/s\n', fmt(results.re_v_stall_m_s, 4));
            fprintf('  V_min (1.2x):      %s m/s\n\n', fmt(results.re_v_min_m_s, 4));

            fprintf('%s\n', repmat('=', 1, 80));
            fprintf('DERIVAZIONE 2: Stallo (matching chart)\n');
            fprintf('%s\n', repmat('=', 1, 80));
            fprintf('  V_stallo (config): %s m/s\n', fmt(results.stall_v_stall_m_s, 4));
            fprintf('  V_min (1.2x):      %s m/s\n', fmt(results.stall_v_min_m_s, 4));
            fprintf('  Carico alare max:  %s N/m^2\n', fmt(results.stall_wing_loading, 4));
            fprintf('  Superficie alare:  %s m^2\n', fmt(results.stall_wing_area_m2, 4));
            fprintf('  Apertura alare:    %s m\n', fmt(results.stall_wingspan_m, 4));
            fprintf('  Corda media:       %s m\n', fmt(results.stall_chord_m, 4));
            fprintf('  Re raggiunto:      %s\n\n', fmt(results.stall_reynolds, 0));

            fprintf('%s\n', repmat('=', 1, 80));
            fprintf('CONFRONTO\n');
            fprintf('%s\n', repmat('=', 1, 80));
            fprintf('  W/S (Re):          %s N/m^2\n', fmt(results.re_wing_loading, 4));
            fprintf('  W/S (stallo):      %s N/m^2\n', fmt(results.stall_wing_loading, 4));
            fprintf('  Rapporto:          %s\n', fmt(results.stall_wing_loading / results.re_wing_loading, 4));
            fprintf('%s\n', repmat('=', 1, 80));
        end
    end
end
