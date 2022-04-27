from src.preprocessors.interpolators.smoothers.basic_smoother_config import BasicSmootherConfig


class SimpleExponentialSmootherConfig(BasicSmootherConfig):
    def __init__(self):
        # https://www.statsmodels.org/stable/generated/statsmodels.tsa.holtwinters.SimpleExpSmoothing.html
        super(SimpleExponentialSmootherConfig, self).__init__()
        self.initialization_method = 'heuristic'
        self.initial_level_construction = None

        # https://www.statsmodels.org/stable/generated/statsmodels.tsa.holtwinters.SimpleExpSmoothing.fit.html#statsmodels.tsa.holtwinters.SimpleExpSmoothing.fit
        self.smoothing_level = 0.4
        self.optimized = True
        self.start_params = None
        self.initial_level_fit = None
        self.use_brute = True
        self.use_boxcox = None
        self.remove_bias = False
        self.method = None
        self.minimize_kwargs = None

    @property
    def dict_of_initial_params(self):
        return {'initialization_method': self.initialization_method, 'initial_level': self.initial_level_construction}

    @property
    def dict_of_fit_params(self):
        return {
            'smoothing_level': self.smoothing_level,
            'optimized': self.optimized,
            'start_params': self.start_params,
            'initial_level': self.initial_level_fit,
            'use_brute': self.use_brute,
            'use_boxcox': self.use_boxcox,
            'remove_bias': self.remove_bias,
            'method': self.method,
            'minimize_kwargs': self.minimize_kwargs
        }

    def __str__(self):
        return str({
            'initial_params': self.dict_of_initial_params,
            'fit_params': self.dict_of_fit_params
        })
