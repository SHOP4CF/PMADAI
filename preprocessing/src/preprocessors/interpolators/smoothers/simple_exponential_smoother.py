from statsmodels.tsa.holtwinters import SimpleExpSmoothing
from numpy import ndarray

from src.preprocessors.interpolators.smoothers.basic_smoother import BasicSmoother
from src.preprocessors.interpolators.smoothers.simple_exponential_smoother_config import SimpleExponentialSmootherConfig


class SimpleExponentialSmoother(BasicSmoother):
    """
    This class is responsible for smoothing interpolation. The method used is Simple Exponential Smoothin
    """
    def __init__(self, smoother_config: SimpleExponentialSmootherConfig):
        super().__init__(smoother_config=smoother_config)

    def smooth_out(self, data: ndarray) -> ndarray:
        """
        this method smooth the received data. Smoother takes into account the parameters saved in the configuration.
        data:
            data to smooth out.
        """
        smoother = SimpleExpSmoothing(
            data,
            initialization_method=self.smoother_config.initialization_method,
            initial_level=self.smoother_config.initial_level_construction
        ).fit(
            smoothing_level=self.smoother_config.smoothing_level,
            optimized=self.smoother_config.optimized,
            start_params=self.smoother_config.start_params,
            initial_level=self.smoother_config.initial_level_fit,
            use_brute=self.smoother_config.use_brute,
            use_boxcox=self.smoother_config.use_boxcox,
            remove_bias=self.smoother_config.remove_bias,
            method=self.smoother_config.method,
            minimize_kwargs=self.smoother_config.minimize_kwargs
        )
        return smoother.fittedvalues
