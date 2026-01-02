classdef hybrid_vtol
    %HYBRID_VTOL Analisi configurazione VTOL ibrido (QuadPlane).

    methods(Static)
        function ld_qp = get_quadplane_ld()
            [ld_max, ~] = mars_uav.section5.fixed_wing.maximum_ld();
            penalty = mars_uav.config.get_param('aerodynamic.quadplane.ld_penalty_factor');
            ld_qp = ld_max * penalty;
        end

        function p_hover = quadplane_hover_power()
            p_hover = mars_uav.section5.rotorcraft.electric_hover_power();
        end

        function e_hover = quadplane_hover_energy()
            p_hover = mars_uav.section5.hybrid_vtol.quadplane_hover_power();
            t_hover_s = mars_uav.config.get_param('mission.time.t_hover_s');
            e_hover = p_hover * (t_hover_s / 3600);
        end

        function p_cruise = quadplane_cruise_power()
            g_mars = mars_uav.config.get_mars_gravity();
            mtow_kg = mars_uav.config.get_mtow();
            weight_n = mtow_kg * g_mars;
            v_cruise = mars_uav.config.get_mission_params().v_cruise;
            ld_qp = mars_uav.section5.hybrid_vtol.get_quadplane_ld();
            p_cruise = mars_uav.section5.fixed_wing.cruise_power(weight_n, v_cruise, ld_qp);
        end

        function e_cruise = quadplane_cruise_energy()
            p_cruise = mars_uav.section5.hybrid_vtol.quadplane_cruise_power();
            t_cruise_min = mars_uav.config.get_param('mission.time.t_cruise_min');
            e_cruise = p_cruise * (t_cruise_min / 60);
        end

        function trans = transition_energy_estimate()
            n_transitions = mars_uav.config.get_param('mission.time.n_transitions');
            reference_energy_j = mars_uav.config.get_param('mission.transition.reference_energy_j');
            mars_scaling = mars_uav.config.get_param('mission.transition.mars_scaling_factor');

            ref_mtow_kg = mars_uav.config.get_param('mission.transition.reference_mtow_kg');
            actual_mtow_kg = mars_uav.config.get_mtow();

            mass_ratio = actual_mtow_kg / ref_mtow_kg;
            scaled_energy_j = reference_energy_j * mass_ratio * mars_scaling;

            total_transition_j = scaled_energy_j * n_transitions;
            total_transition_wh = total_transition_j / 3600.0;

            trans = struct( ...
                'n_transitions', n_transitions, ...
                'reference_energy_j', reference_energy_j, ...
                'mars_scaling_factor', mars_scaling, ...
                'per_transition_j', scaled_energy_j, ...
                'per_transition_wh', scaled_energy_j / 3600.0, ...
                'total_transition_j', total_transition_j, ...
                'total_transition_wh', total_transition_wh ...
            );
        end

        function impact = transition_energy_impact(hover_energy_wh, mission_energy_wh)
            trans = mars_uav.section5.hybrid_vtol.transition_energy_estimate();
            e_transition = trans.total_transition_wh;

            if hover_energy_wh > 0
                fraction_of_hover = (e_transition / hover_energy_wh) * 100;
            else
                fraction_of_hover = 0.0;
            end

            if mission_energy_wh > 0
                fraction_of_mission = (e_transition / mission_energy_wh) * 100;
            else
                fraction_of_mission = 0.0;
            end

            impact = struct( ...
                'transition_energy_wh', e_transition, ...
                'fraction_of_hover_percent', fraction_of_hover, ...
                'fraction_of_mission_percent', fraction_of_mission ...
            );
        end

        function budget = energy_budget()
            e_hover = mars_uav.section5.hybrid_vtol.quadplane_hover_energy();
            e_cruise = mars_uav.section5.hybrid_vtol.quadplane_cruise_energy();
            trans = mars_uav.section5.hybrid_vtol.transition_energy_estimate();
            e_transition = trans.total_transition_wh;
            reserve = mars_uav.config.get_param('mission.energy.reserve_fraction');

            e_mission = e_hover + e_transition + e_cruise;
            e_reserve = e_mission * reserve;
            e_required = e_mission + e_reserve;

            budget = struct( ...
                'hover_wh', e_hover, ...
                'transition_wh', e_transition, ...
                'cruise_wh', e_cruise, ...
                'mission_wh', e_mission, ...
                'reserve_wh', e_reserve, ...
                'required_wh', e_required ...
            );
        end

        function e_avail = available_energy()
            mtow_kg = mars_uav.config.get_mtow();
            batt = mars_uav.config.get_battery_params();
            f_batt = mars_uav.config.get_mission_params().f_batt;

            e_avail = f_batt * mtow_kg * batt.e_spec_Wh_kg * batt.dod * batt.eta_discharge;
        end

        function margin = energy_margin()
            budget = mars_uav.section5.hybrid_vtol.energy_budget();
            e_available = mars_uav.section5.hybrid_vtol.available_energy();
            e_required = budget.required_wh;

            margin_wh = e_available - e_required;
            margin_percent = (margin_wh / e_required) * 100;
            feasible = e_available >= e_required;

            margin = struct( ...
                'available_wh', e_available, ...
                'required_wh', e_required, ...
                'margin_wh', margin_wh, ...
                'margin_percent', margin_percent, ...
                'feasible', feasible ...
            );
        end

        function results = hybrid_vtol_feasibility_analysis()
            g_mars = mars_uav.config.get_mars_gravity();
            rho = mars_uav.config.get_density();
            mtow_kg = mars_uav.config.get_mtow();
            prop = mars_uav.config.get_propulsion_efficiencies();
            batt = mars_uav.config.get_battery_params();
            mission = mars_uav.config.get_mission_params();
            aero = mars_uav.config.get_aerodynamic_params();
            endurance_req = mars_uav.config.get_param('mission.requirements.endurance_min');
            disk_loading = mars_uav.config.get_param('geometry.rotor.disk_loading_N_m2');
            ld_penalty = mars_uav.config.get_param('aerodynamic.quadplane.ld_penalty_factor');

            weight_n = mtow_kg * g_mars;
            disk_area_m2 = weight_n / disk_loading;
            v_cruise = mission.v_cruise;
            t_hover_s = mission.t_hover_s;
            t_cruise_min = mission.t_cruise_min;

            [ld_max, cl_opt] = mars_uav.section5.fixed_wing.maximum_ld();
            ld_quadplane = ld_max * ld_penalty;

            p_hover = mars_uav.section5.rotorcraft.electric_hover_power();
            eta_cruise = prop.eta_prop * prop.eta_motor * prop.eta_esc;
            p_cruise = mars_uav.section5.fixed_wing.cruise_power(weight_n, v_cruise, ld_quadplane);

            v_i = mars_uav.section5.rotorcraft.induced_velocity_from_disk_loading(disk_loading, rho);
            eta_hover = prop.figure_of_merit * prop.eta_motor * prop.eta_esc;

            e_hover = p_hover * (t_hover_s / 3600);
            e_cruise = p_cruise * (t_cruise_min / 60);

            trans = mars_uav.section5.hybrid_vtol.transition_energy_estimate();
            e_transition = trans.total_transition_wh;

            e_mission_without_trans = e_hover + e_cruise;
            e_mission = e_hover + e_transition + e_cruise;
            e_reserve = e_mission * mission.energy_reserve;
            e_required = e_mission + e_reserve;

            trans_impact = mars_uav.section5.hybrid_vtol.transition_energy_impact(e_hover, e_mission_without_trans);

            battery_mass_kg = mission.f_batt * mtow_kg;
            total_energy_wh = battery_mass_kg * batt.e_spec_Wh_kg;
            usable_energy_wh = total_energy_wh * batt.dod * batt.eta_discharge;

            margin_wh = usable_energy_wh - e_required;
            if e_required > 0
                margin_percent = (margin_wh / e_required) * 100;
            else
                margin_percent = 0;
            end

            t_transition_s = mars_uav.config.get_param('mission.time.t_transition_s');
            e_for_cruise = usable_energy_wh * (1 - mission.energy_reserve) - e_hover - e_transition;
            if e_for_cruise > 0 && p_cruise > 0
                cruise_time_min = (e_for_cruise / p_cruise) * 60;
            else
                cruise_time_min = 0;
            end

            total_endurance_min = (t_hover_s / 60) + (t_transition_s / 60) + cruise_time_min;

            range_km = (v_cruise * cruise_time_min * 60) / 1000;
            operational_radius_km = range_km / 2;

            feasible = usable_energy_wh >= e_required;
            endurance_passes = total_endurance_min >= endurance_req;

            results = struct( ...
                'mtow_kg', mtow_kg, ...
                'weight_n', weight_n, ...
                'rho_kg_m3', rho, ...
                'v_cruise_m_s', v_cruise, ...
                'disk_loading_n_m2', disk_loading, ...
                'disk_area_m2', disk_area_m2, ...
                'ld_max_pure', ld_max, ...
                'ld_penalty_factor', ld_penalty, ...
                'ld_quadplane', ld_quadplane, ...
                'figure_of_merit', prop.figure_of_merit, ...
                'eta_motor', prop.eta_motor, ...
                'eta_esc', prop.eta_esc, ...
                'eta_prop', prop.eta_prop, ...
                'eta_hover', eta_hover, ...
                'eta_cruise', eta_cruise, ...
                'induced_velocity_m_s', v_i, ...
                'hover_power_w', p_hover, ...
                'cruise_power_w', p_cruise, ...
                'hover_time_min', t_hover_s / 60, ...
                'cruise_time_min', cruise_time_min, ...
                'hover_energy_wh', e_hover, ...
                'transition_energy_wh', e_transition, ...
                'cruise_energy_wh', e_cruise, ...
                'mission_energy_wh', e_mission, ...
                'mission_energy_without_trans_wh', e_mission_without_trans, ...
                'reserve_energy_wh', e_reserve, ...
                'required_energy_wh', e_required, ...
                'transition_per_phase_j', trans.per_transition_j, ...
                'transition_per_phase_wh', trans.per_transition_wh, ...
                'n_transitions', trans.n_transitions, ...
                'transition_fraction_of_hover', trans_impact.fraction_of_hover_percent, ...
                'transition_fraction_of_mission', trans_impact.fraction_of_mission_percent, ...
                'battery_mass_kg', battery_mass_kg, ...
                'total_energy_wh', total_energy_wh, ...
                'usable_energy_wh', usable_energy_wh, ...
                'margin_wh', margin_wh, ...
                'margin_percent', margin_percent, ...
                'endurance_min', total_endurance_min, ...
                'range_km', range_km, ...
                'operational_radius_km', operational_radius_km, ...
                'requirement_min', endurance_req, ...
                'feasible', feasible && endurance_passes, ...
                'endurance_passes', endurance_passes, ...
                'energy_feasible', feasible ...
            );
        end

        function print_analysis(results)
            if nargin < 1 || isempty(results)
                results = mars_uav.section5.hybrid_vtol.hybrid_vtol_feasibility_analysis();
            end
            fmt = @(value, decimals) mars_uav.core.format_number(value, decimals);

            fprintf('%s\n', repmat('=', 1, 80));
            fprintf('ANALISI DI FATTIBILITA VTOL IBRIDO (QUADPLANE) (Sezione 5.3)\n');
            fprintf('%s\n', repmat('=', 1, 80));
            fprintf('Calcolato: %s\n', datestr(now, 'yyyy-mm-dd HH:MM:SS'));
            fprintf('Config:    Valori da file YAML in config/\n\n');

            fprintf('PARAMETRI DI INGRESSO (da configurazione)\n');
            fprintf('%s\n', repmat('-', 1, 50));
            fprintf('  MTOW:               %s kg\n', fmt(results.mtow_kg, 2));
            fprintf('  Peso:               %s N\n', fmt(results.weight_n, 2));
            fprintf('  Densita aria:       %s kg/m^3\n', fmt(results.rho_kg_m3, 4));
            fprintf('  Velocita crociera:  %s m/s\n', fmt(results.v_cruise_m_s, 1));
            fprintf('  Carico disco:       %s N/m^2\n\n', fmt(results.disk_loading_n_m2, 1));

            fprintf('EFFICIENZA AERODINAMICA\n');
            fprintf('%s\n', repmat('-', 1, 50));
            fprintf('  Ala pura (L/D)max:  %s\n', fmt(results.ld_max_pure, 2));
            fprintf('  Fattore penalita:   %s (rotori fermi)\n', fmt(results.ld_penalty_factor, 2));
            fprintf('  L/D QuadPlane:      %s\n\n', fmt(results.ld_quadplane, 2));

            fprintf('ANALISI HOVERING (rotori di sollevamento)\n');
            fprintf('%s\n', repmat('-', 1, 50));
            fprintf('  Velocita indotta:   %s m/s\n', fmt(results.induced_velocity_m_s, 2));
            fprintf('  Potenza hovering:   %s W\n', fmt(results.hover_power_w, 0));
            fprintf('  Tempo hovering:     %s min\n', fmt(results.hover_time_min, 0));
            fprintf('  Energia hovering:   %s Wh\n\n', fmt(results.hover_energy_wh, 1));

            fprintf('ANALISI CROCIERA (ala + motore crociera)\n');
            fprintf('%s\n', repmat('-', 1, 50));
            fprintf('  Potenza crociera:   %s W\n', fmt(results.cruise_power_w, 1));
            fprintf('  Tempo crociera:     %s min\n', fmt(results.cruise_time_min, 1));
            fprintf('  Energia crociera:   %s Wh\n\n', fmt(results.cruise_energy_wh, 1));

            fprintf('ANALISI TRANSIZIONE (stima conservativa)\n');
            fprintf('%s\n', repmat('-', 1, 50));
            fprintf('  Numero transizioni:     %s\n', fmt(results.n_transitions, 0));
            fprintf('  Energia per transizione: %s Wh (%s J)\n', ...
                fmt(results.transition_per_phase_wh, 1), fmt(results.transition_per_phase_j, 0));
            fprintf('  Energia transizione tot: %s Wh\n', fmt(results.transition_energy_wh, 1));
            fprintf('  Frazione di hovering:   %s%%\n', fmt(results.transition_fraction_of_hover, 1));
            fprintf('  Frazione missione:      %s%%\n\n', fmt(results.transition_fraction_of_mission, 1));

            hover_frac = results.hover_energy_wh / results.mission_energy_wh * 100;
            trans_frac = results.transition_energy_wh / results.mission_energy_wh * 100;
            cruise_frac = results.cruise_energy_wh / results.mission_energy_wh * 100;

            fprintf('BILANCIO ENERGETICO (con transizione)\n');
            fprintf('%s\n', repmat('-', 1, 50));
            fprintf('  Energia missione:   %s Wh\n', fmt(results.mission_energy_wh, 1));
            fprintf('    - Hovering:       %s Wh (%s%%)\n', ...
                fmt(results.hover_energy_wh, 1), fmt(hover_frac, 0));
            fprintf('    - Transizione:    %s Wh (%s%%)\n', ...
                fmt(results.transition_energy_wh, 1), fmt(trans_frac, 0));
            fprintf('    - Crociera:       %s Wh (%s%%)\n', ...
                fmt(results.cruise_energy_wh, 1), fmt(cruise_frac, 0));
            fprintf('  Riserva (20%%):      %s Wh\n', fmt(results.reserve_energy_wh, 1));
            fprintf('  Totale richiesto:   %s Wh\n', fmt(results.required_energy_wh, 1));
            fprintf('  Disponibile:        %s Wh\n', fmt(results.usable_energy_wh, 1));
            fprintf('  Margine:            %s Wh (%s%%)\n\n', ...
                fmt(results.margin_wh, 1), fmt(results.margin_percent, 1));

            fprintf('PRESTAZIONI\n');
            fprintf('%s\n', repmat('-', 1, 50));
            fprintf('  Autonomia totale:   %s min\n', fmt(results.endurance_min, 1));
            fprintf('  Raggio:             %s km\n', fmt(results.range_km, 0));
            fprintf('  Raggio operativo:   %s km\n\n', fmt(results.operational_radius_km, 0));

            fprintf('VALUTAZIONE FATTIBILITA\n');
            fprintf('%s\n', repmat('-', 1, 50));
            if results.endurance_passes
                end_status = '[OK]';
            else
                end_status = '[NO]';
            end
            if results.energy_feasible
                energy_status = '[OK]';
            else
                energy_status = '[NO]';
            end
            if results.feasible
                overall = '[OK]';
            else
                overall = '[NO]';
            end

            margin = (results.endurance_min / results.requirement_min - 1) * 100;

            fprintf('  Capacita VTOL:      [OK] (rotori di sollevamento)\n');
            fprintf('  Vincolo energia:    %s (margine %s%%)\n', energy_status, fmt(results.margin_percent, 1));
            fprintf('  Requisito autonomia: %s min -> %s min (%s%%) -> %s\n', ...
                fmt(results.requirement_min, 0), fmt(results.endurance_min, 0), fmt(margin, 1), end_status);
            fprintf('  Complessivo:        %s\n\n', overall);

            if results.feasible
                fprintf('CONCLUSIONE: Il VTOL ibrido (QuadPlane) soddisfa tutti i requisiti.\n');
            else
                fprintf('CONCLUSIONE: Il VTOL ibrido non soddisfa uno o piu requisiti.\n');
            end

            fprintf('%s\n', repmat('=', 1, 80));
        end
    end
end

