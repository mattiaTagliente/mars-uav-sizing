classdef airfoil_selection
    %AIRFOIL_SELECTION Confronto e selezione profili alari (Sezione 6.2).

    methods(Static)
        function polars = load_airfoil_data()
            %LOAD_AIRFOIL_DATA Carica i dati dei profili dal YAML.
            polars = mars_uav.section6.airfoil_plots.load_airfoil_data();
        end

        function metrics = get_airfoil_metrics(polars)
            %GET_AIRFOIL_METRICS Estrae metriche chiave per ogni profilo.
            metrics = struct('name', {}, 'reynolds', {}, 'cl_max', {}, ...
                'alpha_stall', {}, 'ld_max', {}, 'cl_at_ld_max', {}, ...
                'cd_at_ld_max', {}, 'cd_min', {}, 'score', {});

            for i = 1:numel(polars)
                name = polars(i).name;
                alpha = polars(i).alpha;
                cl = polars(i).cl;
                cd = polars(i).cd;
                ld = polars(i).ld;

                [cl_max, idx_cl_max] = max(cl);
                alpha_stall = alpha(idx_cl_max);

                [ld_max, idx_ld_max] = max(ld);
                cl_at_ld_max = cl(idx_ld_max);
                cd_at_ld_max = cd(idx_ld_max);

                cd_pos = cd(cd > 0);
                if isempty(cd_pos)
                    cd_min = 0;
                else
                    cd_min = min(cd_pos);
                end

                metrics(end+1) = struct( ... %#ok<AGROW>
                    'name', name, ...
                    'reynolds', polars(i).reynolds, ...
                    'cl_max', cl_max, ...
                    'alpha_stall', alpha_stall, ...
                    'ld_max', ld_max, ...
                    'cl_at_ld_max', cl_at_ld_max, ...
                    'cd_at_ld_max', cd_at_ld_max, ...
                    'cd_min', cd_min, ...
                    'score', 0 ...
                );
            end
        end

        function [best_name, metrics] = select_best_airfoil(polars, weights)
            %SELECT_BEST_AIRFOIL Selezione pesata del profilo migliore.
            if nargin < 2 || isempty(weights)
                weights = struct('ld_max', 0.6, 'cl_max', 0.25, 'stall_margin', 0.15);
            end

            metrics = mars_uav.section6.airfoil_selection.get_airfoil_metrics(polars);

            for i = 1:numel(metrics)
                ld_score = metrics(i).ld_max / 50.0;
                cl_score = metrics(i).cl_max / 2.0;
                stall_score = metrics(i).alpha_stall / 15.0;

                total_score = weights.ld_max * ld_score + ...
                    weights.cl_max * cl_score + ...
                    weights.stall_margin * stall_score;

                metrics(i).score = total_score;
            end

            scores = [metrics.score];
            [~, idx_best] = max(scores);
            best_name = metrics(idx_best).name;
        end

        function print_airfoil_comparison()
            %PRINT_AIRFOIL_COMPARISON Tabella confronto profili alari.
            polars = mars_uav.section6.airfoil_selection.load_airfoil_data();
            [best_name, metrics] = mars_uav.section6.airfoil_selection.select_best_airfoil(polars);

            [~, order] = sort([metrics.ld_max], 'descend');
            metrics = metrics(order);

            fmt = @(value, decimals) mars_uav.core.format_number(value, decimals);

            fprintf('%s\n', repmat('=', 1, 80));
            fprintf('CONFRONTO PROFILI ALARI (Sezione 6.2)\n');
            fprintf('%s\n\n', repmat('=', 1, 80));
            fprintf('%-10s %-8s %-8s %-10s %-10s %-10s %-8s\n', ...
                'Profilo', 'Re', 'CL_max', 'alpha_st', '(L/D)_max', 'CL@LD', 'Score');
            fprintf('%s\n', repmat('-', 1, 80));

            for i = 1:numel(metrics)
                marker = '';
                if strcmpi(metrics(i).name, best_name)
                    marker = '  <=';
                end
                fprintf('%-10s %-8s %-8s %-10s %-10s %-10s %-8s%s\n', ...
                    upper(metrics(i).name), ...
                    fmt(metrics(i).reynolds, 0), ...
                    fmt(metrics(i).cl_max, 2), ...
                    fmt(metrics(i).alpha_stall, 1), ...
                    fmt(metrics(i).ld_max, 1), ...
                    fmt(metrics(i).cl_at_ld_max, 2), ...
                    fmt(metrics(i).score, 3), ...
                    marker);
            end

            fprintf('\nSELEZIONATO: %s (punteggio massimo)\n\n', upper(best_name));
            idx_best = find(strcmpi({metrics.name}, best_name), 1);
            fprintf('Razionale selezione:\n');
            fprintf('  - (L/D)_max = %s\n', fmt(metrics(idx_best).ld_max, 1));
            fprintf('  - CL_max = %s (margine stallo)\n', fmt(metrics(idx_best).cl_max, 2));
            fprintf('  - Dati sperimentali UIUC disponibili\n');
            fprintf('%s\n', repmat('=', 1, 80));
        end
    end
end
