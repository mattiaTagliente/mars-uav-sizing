classdef energy
    %ENERGY Utilita per bilancio energetico condiviso.

    methods(Static)
        function batt = get_battery_energy()
            mtow_kg = mars_uav.config.get_mtow();
            batt_params = mars_uav.config.get_battery_params();
            f_batt = mars_uav.config.get_mission_params().f_batt;

            battery_mass_kg = f_batt * mtow_kg;
            total_energy_wh = battery_mass_kg * batt_params.e_spec_Wh_kg;
            usable_energy_wh = total_energy_wh * batt_params.dod * batt_params.eta_discharge;

            batt = struct( ...
                'battery_mass_kg', battery_mass_kg, ...
                'total_energy_wh', total_energy_wh, ...
                'usable_energy_wh', usable_energy_wh, ...
                'e_spec_Wh_kg', batt_params.e_spec_Wh_kg, ...
                'dod', batt_params.dod, ...
                'eta_discharge', batt_params.eta_discharge, ...
                'f_batt', f_batt ...
            );
        end

        function reserve = compute_reserve_energy(mission_energy_wh)
            reserve_fraction = mars_uav.config.get_param('mission.energy.reserve_fraction');
            reserve_energy_wh = mission_energy_wh * reserve_fraction;
            required_energy_wh = mission_energy_wh + reserve_energy_wh;

            reserve = struct( ...
                'mission_energy_wh', mission_energy_wh, ...
                'reserve_fraction', reserve_fraction, ...
                'reserve_energy_wh', reserve_energy_wh, ...
                'required_energy_wh', required_energy_wh ...
            );
        end

        function margin = compute_energy_margin(available_wh, required_wh)
            margin_wh = available_wh - required_wh;
            if required_wh > 0
                margin_percent = (margin_wh / required_wh) * 100;
            else
                margin_percent = 0.0;
            end

            margin = struct( ...
                'available_wh', available_wh, ...
                'required_wh', required_wh, ...
                'margin_wh', margin_wh, ...
                'margin_percent', margin_percent, ...
                'feasible', available_wh >= required_wh ...
            );
        end

        function budget = compute_full_energy_budget(hover_energy_wh, transition_energy_wh, cruise_energy_wh)
            batt = mars_uav.core.energy.get_battery_energy();
            mission_energy_wh = hover_energy_wh + transition_energy_wh + cruise_energy_wh;
            reserve = mars_uav.core.energy.compute_reserve_energy(mission_energy_wh);
            margin = mars_uav.core.energy.compute_energy_margin(batt.usable_energy_wh, reserve.required_energy_wh);

            budget = struct( ...
                'battery_mass_kg', batt.battery_mass_kg, ...
                'total_energy_wh', batt.total_energy_wh, ...
                'usable_energy_wh', batt.usable_energy_wh, ...
                'hover_energy_wh', hover_energy_wh, ...
                'transition_energy_wh', transition_energy_wh, ...
                'cruise_energy_wh', cruise_energy_wh, ...
                'mission_energy_wh', mission_energy_wh, ...
                'reserve_energy_wh', reserve.reserve_energy_wh, ...
                'required_energy_wh', reserve.required_energy_wh, ...
                'margin_wh', margin.margin_wh, ...
                'margin_percent', margin.margin_percent, ...
                'feasible', margin.feasible, ...
                'dod', batt.dod, ...
                'eta_discharge', batt.eta_discharge, ...
                'reserve_fraction', reserve.reserve_fraction ...
            );
        end

        function text = format_energy_budget(budget, label)
            if nargin < 2 || isempty(label)
                label = 'BILANCIO ENERGETICO';
            end

            reserve_pct = round(budget.reserve_fraction * 100);
            fmt = @(value, decimals) mars_uav.core.format_number(value, decimals);

            lines = {
                label,
                repmat('-', 1, 50),
                sprintf('  Massa batteria:     %s kg', fmt(budget.battery_mass_kg, 2)),
                sprintf('  Capacita totale:    %s Wh', fmt(budget.total_energy_wh, 0)),
                sprintf('  Utilizzabile (%d%% DoD, %d%% eta): %s Wh', ...
                    round(budget.dod * 100), round(budget.eta_discharge * 100), fmt(budget.usable_energy_wh, 0)),
                '',
                sprintf('  Energia missione:   %s Wh', fmt(budget.mission_energy_wh, 1))
            };

            if budget.mission_energy_wh > 0
                hover_pct = budget.hover_energy_wh / budget.mission_energy_wh * 100;
                trans_pct = budget.transition_energy_wh / budget.mission_energy_wh * 100;
                cruise_pct = budget.cruise_energy_wh / budget.mission_energy_wh * 100;
                lines = [lines; {
                    sprintf('    - Hovering:       %s Wh (%s%%)', fmt(budget.hover_energy_wh, 1), fmt(hover_pct, 0)),
                    sprintf('    - Transizione:    %s Wh (%s%%)', fmt(budget.transition_energy_wh, 1), fmt(trans_pct, 0)),
                    sprintf('    - Crociera:       %s Wh (%s%%)', fmt(budget.cruise_energy_wh, 1), fmt(cruise_pct, 0))
                }];
            end

            lines = [lines; {
                sprintf('  Riserva (%d%%):      %s Wh', reserve_pct, fmt(budget.reserve_energy_wh, 1)),
                sprintf('  Totale richiesto:   %s Wh', fmt(budget.required_energy_wh, 1)),
                sprintf('  Margine:            %s Wh (%s%%)', fmt(budget.margin_wh, 1), fmt(budget.margin_percent, 1))
            }];

            text = strjoin(lines, newline);
        end

        function label = get_reserve_label()
            reserve_fraction = mars_uav.config.get_param('mission.energy.reserve_fraction');
            label = sprintf('%d%%', round(reserve_fraction * 100));
        end
    end
end

