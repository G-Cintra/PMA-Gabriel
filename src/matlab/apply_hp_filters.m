% apply_hp_filters.m
% Loads IPCA and GDP data, applies log-transform to GDP,
% applies two-sided and one-sided HP filters, and saves trends

% ---- Step 1: Load CSV files ----
ipca_table = readtable('IBGE_20250331_183405_T118-V306_205037.csv');
gdp_table  = readtable('IBGE_20250331_183405_T6613-V9319_205007.csv');

ipca_values = ipca_table.valor;
gdp_values  = gdp_table.valor;

% ---- Step 2: Log-transform GDP ----
log_gdp_values = log(gdp_values);

% ---- Step 3: Apply HP Filters ----

% IPCA (monthly): lambda = 129600
[ipca_trend_two, ~] = hpfilter(ipca_values, Smoothing=129600, FilterType="two-sided");
[ipca_trend_one, ~] = hpfilter(ipca_values, Smoothing=129600, FilterType="one-sided");

% GDP (quarterly, log): lambda = 1600
[gdp_trend_two, ~] = hpfilter(log_gdp_values, Smoothing=1600, FilterType="two-sided");
[gdp_trend_one, ~] = hpfilter(log_gdp_values, Smoothing=1600, FilterType="one-sided");
[gdp_trend_onea, ~] = hpfilter(log_gdp_values, Smoothing=650, FilterType="one-sided");

% ---- Step 4: Save Results ----
writematrix(ipca_trend_two, 'ipca_trend_two_sided.csv');
writematrix(ipca_trend_one, 'ipca_trend_one_sided.csv');
writematrix(gdp_trend_two,  'gdp_trend_two_sided.csv');
writematrix(gdp_trend_one,  'gdp_trend_one_sided.csv');
writematrix(gdp_trend_onea,  'gdp_trend_one_sideda.csv');

disp('HP filter trends saved successfully (log-GDP applied).');
