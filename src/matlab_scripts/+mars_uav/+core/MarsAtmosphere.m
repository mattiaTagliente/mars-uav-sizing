classdef MarsAtmosphere
    %MARSATMOSPHERE Modello atmosferico di Marte.

    properties
        R
        gamma
        g
        T0
        P0
        H
        lapse_rate
        mu_ref
        T_mu_ref
        C_suth
    end

    methods
        function obj = MarsAtmosphere()
            obj.R = mars_uav.config.get_param('physical.mars_atmosphere_composition.R_specific');
            obj.gamma = mars_uav.config.get_param('physical.mars_atmosphere_composition.gamma');
            obj.g = mars_uav.config.get_param('physical.mars.g');

            ref = mars_uav.config.get_param('environment.reference_atmosphere');
            obj.T0 = ref.T_surface;
            obj.P0 = ref.P_surface;
            obj.H = ref.scale_height_km;
            obj.lapse_rate = ref.lapse_rate;

            suth = mars_uav.config.get_param('physical.sutherland');
            obj.mu_ref = suth.mu_ref;
            obj.T_mu_ref = suth.T_ref;
            obj.C_suth = suth.C;
        end

        function T = temperature(obj, altitude_km)
            lapse_k_km = obj.lapse_rate * 1000;
            T = obj.T0 - lapse_k_km * altitude_km;
        end

        function P = pressure(obj, altitude_km)
            h_m = altitude_km * 1000;
            T = obj.temperature(altitude_km);
            exponent = -obj.g * h_m / (obj.R * T);
            P = obj.P0 * exp(exponent);
        end

        function rho = density(obj, altitude_km)
            P = obj.pressure(altitude_km);
            T = obj.temperature(altitude_km);
            rho = P / (obj.R * T);
        end

        function mu = viscosity(obj, altitude_km)
            T = obj.temperature(altitude_km);
            ratio = (T / obj.T_mu_ref) ^ 1.5;
            factor = (obj.T_mu_ref + obj.C_suth) / (T + obj.C_suth);
            mu = obj.mu_ref * ratio * factor;
        end

        function a = speed_of_sound(obj, altitude_km)
            T = obj.temperature(altitude_km);
            a = sqrt(obj.gamma * obj.R * T);
        end

        function state = get_state(obj, altitude_km)
            state = struct( ...
                'altitude_km', altitude_km, ...
                'temperature_K', obj.temperature(altitude_km), ...
                'pressure_Pa', obj.pressure(altitude_km), ...
                'density_kg_m3', obj.density(altitude_km), ...
                'viscosity_Pa_s', obj.viscosity(altitude_km), ...
                'speed_of_sound_m_s', obj.speed_of_sound(altitude_km) ...
            );
            state.kinematic_viscosity = state.viscosity_Pa_s / state.density_kg_m3;
        end

        function re = reynolds_number(obj, velocity, length, altitude_km)
            if nargin < 4
                altitude_km = -3.0;
            end
            rho = obj.density(altitude_km);
            mu = obj.viscosity(altitude_km);
            re = rho * velocity * length / mu;
        end

        function mach = mach_number(obj, velocity, altitude_km)
            if nargin < 3
                altitude_km = -3.0;
            end
            a = obj.speed_of_sound(altitude_km);
            mach = velocity / a;
        end
    end

    methods(Static)
        function atm = arcadia_planitia()
            atm = mars_uav.core.MarsAtmosphere();
        end
    end
end

