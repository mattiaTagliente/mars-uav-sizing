classdef atmospheric_model
    %ATMOSPHERIC_MODEL Modello atmosferico polytropico (Sezione 3.1).

    methods(Static)
        function P = barometric_pressure(altitude_km)
            %BAROMETRIC_PRESSURE Pressione barometrica con gradiente termico.
            P0 = mars_uav.config.get_param('environment.reference_atmosphere.P_surface');
            g = mars_uav.config.get_param('physical.mars.g');
            R = mars_uav.config.get_param('physical.mars_atmosphere_composition.R_specific');
            T0 = mars_uav.config.get_param('environment.reference_atmosphere.T_surface');
            lapse = mars_uav.config.get_param('environment.reference_atmosphere.lapse_rate');

            T = T0 - lapse * altitude_km * 1000;
            exponent = g / (R * lapse);
            P = P0 * (T / T0) ^ exponent;
        end

        function rho = ideal_gas_density(pressure_pa, temperature_k)
            %IDEAL_GAS_DENSITY Densita da equazione dei gas ideali.
            R = mars_uav.config.get_param('physical.mars_atmosphere_composition.R_specific');
            rho = pressure_pa / (R * temperature_k);
        end

        function mu = sutherland_viscosity(temperature_k)
            %SUTHERLAND_VISCOSITY Viscosita dinamica con legge di Sutherland.
            mu_ref = mars_uav.config.get_param('physical.sutherland.mu_ref');
            T_ref = mars_uav.config.get_param('physical.sutherland.T_ref');
            C = mars_uav.config.get_param('physical.sutherland.C');

            ratio = (temperature_k / T_ref) ^ 1.5;
            factor = (T_ref + C) / (temperature_k + C);
            mu = mu_ref * ratio * factor;
        end

        function a = speed_of_sound(temperature_k)
            %SPEED_OF_SOUND Velocita del suono in atmosfera marziana.
            gamma = mars_uav.config.get_param('physical.mars_atmosphere_composition.gamma');
            R = mars_uav.config.get_param('physical.mars_atmosphere_composition.R_specific');
            a = sqrt(gamma * R * temperature_k);
        end

        function re = reynolds_number(velocity, length, rho, mu)
            %REYNOLDS_NUMBER Numero di Reynolds.
            re = rho * velocity * length / mu;
        end

        function mach = mach_number(velocity, temperature_k)
            %MACH_NUMBER Numero di Mach.
            a = mars_uav.section3.atmospheric_model.speed_of_sound(temperature_k);
            mach = velocity / a;
        end

        function results = arcadia_planitia_conditions()
            %ARCADIA_PLANITIA_CONDITIONS Stato atmosferico operativo.
            elevation_km = mars_uav.config.get_param('environment.arcadia_planitia.elevation_km');
            agl_m = mars_uav.config.get_param('environment.arcadia_planitia.operating_altitude_agl_m');
            altitude_km = elevation_km + agl_m / 1000;

            T0 = mars_uav.config.get_param('environment.reference_atmosphere.T_surface');
            lapse = mars_uav.config.get_param('environment.reference_atmosphere.lapse_rate');
            T = T0 - lapse * altitude_km * 1000;

            P = mars_uav.section3.atmospheric_model.barometric_pressure(altitude_km);
            rho = mars_uav.section3.atmospheric_model.ideal_gas_density(P, T);
            mu = mars_uav.section3.atmospheric_model.sutherland_viscosity(T);
            a = mars_uav.section3.atmospheric_model.speed_of_sound(T);

            v_cruise = mars_uav.config.get_param('mission.velocity.v_cruise_m_s');
            chord = mars_uav.config.get_param('aerodynamic.wing.mean_chord_m');
            re = mars_uav.section3.atmospheric_model.reynolds_number(v_cruise, chord, rho, mu);
            mach = mars_uav.section3.atmospheric_model.mach_number(v_cruise, T);

            results = struct( ...
                'surface_elevation_km', elevation_km, ...
                'agl_m', agl_m, ...
                'operating_altitude_km', altitude_km, ...
                'temperature_k', T, ...
                'pressure_pa', P, ...
                'density_kg_m3', rho, ...
                'viscosity_pa_s', mu, ...
                'speed_of_sound_m_s', a, ...
                'kinematic_viscosity_m2_s', mu / rho, ...
                'reynolds_at_cruise', re, ...
                'mach_at_cruise', mach ...
            );
        end

        function print_analysis()
            %PRINT_ANALYSIS Stampa analisi atmosferica formattata.
            results = mars_uav.section3.atmospheric_model.arcadia_planitia_conditions();
            timestamp = datestr(now, 'yyyy-mm-dd HH:MM:SS');
            fmt = @(value, decimals) mars_uav.core.format_number(value, decimals);

            fprintf('%s\n', repmat('=', 1, 80));
            fprintf('MODELLO ATMOSFERICO (Sezione 3.1)\n');
            fprintf('%s\n', repmat('=', 1, 80));
            fprintf('Calcolato: %s\n', timestamp);
            fprintf('Config:    Parametri da config/mars_environment.yaml\n\n');

            T0 = mars_uav.config.get_param('environment.reference_atmosphere.T_surface');
            P0 = mars_uav.config.get_param('environment.reference_atmosphere.P_surface');
            fprintf('CONDIZIONI DI RIFERIMENTO (h = 0 km)\n');
            fprintf('%s\n', repmat('-', 1, 50));
            fprintf('  Temperatura: %s K\n', fmt(T0, 1));
            fprintf('  Pressione:   %s Pa\n\n', fmt(P0, 1));

            fprintf('ARCADIA PLANITIA (superficie = %s km, AGL = %s m)\n', ...
                fmt(results.surface_elevation_km, 1), fmt(results.agl_m, 0));
            fprintf('%s\n', repmat('-', 1, 50));
            fprintf('  Quota operativa:   %s km\n', fmt(results.operating_altitude_km, 2));
            fprintf('  Temperatura:       %s K\n', fmt(results.temperature_k, 1));
            fprintf('  Pressione:         %s Pa\n', fmt(results.pressure_pa, 1));
            fprintf('  Densita:           %s kg/m^3\n', fmt(results.density_kg_m3, 5));
            fprintf('  Viscosita:         %.3e Pa s\n', results.viscosity_pa_s);
            fprintf('  Viscosita kin.:    %.3e m^2/s\n', results.kinematic_viscosity_m2_s);
            fprintf('  Velocita suono:    %s m/s\n\n', fmt(results.speed_of_sound_m_s, 1));

            v_cruise = mars_uav.config.get_param('mission.velocity.v_cruise_m_s');
            chord = mars_uav.config.get_param('aerodynamic.wing.mean_chord_m');
            fprintf('CONDIZIONI DI CROCIERA (V = %s m/s, c = %s m)\n', ...
                fmt(v_cruise, 0), fmt(chord, 3));
            fprintf('%s\n', repmat('-', 1, 50));
            fprintf('  Reynolds:     %s\n', fmt(results.reynolds_at_cruise, 0));
            fprintf('  Mach:         %s\n\n', fmt(results.mach_at_cruise, 3));

            config_rho = mars_uav.config.get_param('environment.arcadia_planitia.density_kg_m3');
            diff_pct = abs(results.density_kg_m3 - config_rho) / config_rho * 100;
            fprintf('VERIFICA\n');
            fprintf('%s\n', repmat('-', 1, 50));
            fprintf('  Densita calcolata: %s kg/m^3\n', fmt(results.density_kg_m3, 5));
            fprintf('  Densita config:    %s kg/m^3\n', fmt(config_rho, 5));
            fprintf('  Differenza:        %s %%\n', fmt(diff_pct, 2));
            fprintf('%s\n', repmat('=', 1, 80));
        end
    end
end
