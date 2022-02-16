# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/losses__pytorch.ipynb (unless otherwise specified).

__all__ = ['MAELoss', 'MSELoss', 'RMSELoss', 'MAPELoss', 'SMAPELoss', 'MASELoss', 'QuantileLoss', 'MQLoss', 'wMQLoss',
           'LevelVariabilityLoss', 'SmylLoss']

# Cell
import torch as t
import torch.nn as nn

# Cell
def _divide_no_nan(a, b) -> float:
    """
    Auxiliary funtion to handle divide by 0
    """
    div = a / b
    div[div != div] = 0.0
    div[div == float('inf')] = 0.0
    return div

# Cell
def MAELoss(y, y_hat, mask=None) -> t.Tensor:
    """

    Calculates Mean Absolute Error (MAE) between
    y and y_hat. MAE measures the relative prediction
    accuracy of a forecasting method by calculating the
    deviation of the prediction and the true
    value at a given time and averages these devations
    over the length of the series.

    $$ \mathrm{MAE}(\\mathbf{y}_{\\tau}, \\mathbf{\hat{y}}_{\\tau}) =
        \\frac{1}{H} \\sum^{t+H}_{\\tau=t+1}
        |y_{\\tau} - \hat{y}_{\\tau}| $$

        Parameters
        ----------
        y: tensor (batch_size, output_size).
            Aactual values in torch tensor.
        y_hat: tensor (batch_size, output_size).
            Predicted values in torch tensor.
        mask: tensor (batch_size, output_size).
            Specifies date stamps per serie
            to consider in loss.

        Returns
        -------
        mae: tensor (single value).
            Mean absolute error.
    """
    if mask is None: mask = t.ones_like(y_hat)

    mae = t.abs(y - y_hat) * mask
    mae = t.mean(mae)
    return mae

# Cell
def MSELoss(y, y_hat, mask=None) -> t.Tensor:
    """

    Calculates Mean Squared Error (MSE) between
    y and y_hat. MSE measures the relative prediction
    accuracy of a forecasting method by calculating the
    squared deviation of the prediction and the true
    value at a given time, and averages these devations
    over the length of the series.

    $$ \mathrm{MSE}(\\mathbf{y}_{\\tau}, \\mathbf{\hat{y}}_{\\tau}) =
        \\frac{1}{H} \\sum^{t+H}_{\\tau=t+1} (y_{\\tau} - \hat{y}_{\\tau})^{2} $$

        Parameters
        ----------
        y: tensor (batch_size, output_size).
            Actual values in torch tensor.
        y_hat: tensor (batch_size, output_size).
            Predicted values in torch tensor.
        mask: tensor (batch_size, output_size).
            Specifies date stamps per serie
            to consider in loss.

        Returns
        -------
        mse: tensor (single value).
            Mean Squared Error.
    """
    if mask is None: mask = t.ones_like(y_hat)

    mse = (y - y_hat)**2
    mse = mask * mse
    mse = t.mean(mse)
    return mse

# Cell
def RMSELoss(y, y_hat, mask=None) -> t.Tensor:
    """

    Calculates Root Mean Squared Error (RMSE) between
    y and y_hat. RMSE measures the relative prediction
    accuracy of a forecasting method by calculating the squared deviation
    of the prediction and the observed value at a given time and
    averages these devations over the length of the series.
    Finally the RMSE will be in the same scale
    as the original time series so its comparison with other
    series is possible only if they share a common scale.
    RMSE has a direct connection to the L2 norm.

    $$ \mathrm{RMSE}(\\mathbf{y}_{\\tau}, \\mathbf{\hat{y}}_{\\tau}) =
        \\sqrt{\\frac{1}{H} \\sum^{t+H}_{\\tau=t+1} (y_{\\tau} - \hat{y}_{\\tau})^{2}} $$

        Parameters
        ----------
        y: tensor (batch_size, output_size).
            Actual values in torch tensor.
        y_hat: tensor (batch_size, output_size).
            Predicted values in torch tensor.
        mask: tensor (batch_size, output_size).
            Specifies date stamps per serie
            to consider in loss.

        Returns
        -------
        rmse: tensor (single value).
            Root Mean Squared Error.
    """
    if mask is None: mask = t.ones_like(y_hat)

    rmse = (y - y_hat)**2
    rmse = mask * rmse
    rmse = t.sqrt(t.mean(rmse))
    return rmse

# Cell
def MAPELoss(y, y_hat, mask=None) -> t.Tensor:
    """

    Calculates Mean Absolute Percentage Error (MAPE) between
    y and y_hat. MAPE measures the relative prediction
    accuracy of a forecasting method by calculating the percentual deviation
    of the prediction and the observed value at a given time and
    averages these devations over the length of the series.
    The closer to zero an observed value is, the higher penalty MAPE loss
    assigns to the corresponding error.

    $$ \mathrm{MAPE}(\\mathbf{y}_{\\tau}, \\mathbf{\hat{y}}_{\\tau}) =
        \\frac{1}{H} \\sum^{t+H}_{\\tau=t+1}
        \\frac{|y_{\\tau}-\hat{y}_{\\tau}|}{|y_{\\tau}|} $$

        Parameters
        ----------
        y: tensor (batch_size, output_size).
            Actual values in torch tensor.
        y_hat: tensor (batch_size, output_size).
            Predicted values in torch tensor.
        mask: tensor (batch_size, output_size).
            Specifies date stamps per serie
            to consider in loss.

        Returns
        -------
        mape: tensor (single value).
            Mean absolute percentage error.
    """
    if mask is None: mask = t.ones_like(y_hat)

    mask = _divide_no_nan(mask, t.abs(y))
    mape = t.abs(y - y_hat) * mask
    mape = t.mean(mape)
    return mape

# Cell
def SMAPELoss(y, y_hat, mask=None) -> t.Tensor:
    """

    Calculates Symmetric Mean Absolute Percentage Error (SMAPE) between
    y and y_hat. SMAPE measures the relative prediction
    accuracy of a forecasting method by calculating the relative deviation
    of the prediction and the observed value scaled by the sum of the
    absolute values for the prediction and observed value at a
    given time, then averages these devations over the length
    of the series. This allows the SMAPE to have bounds between
    0% and 200% which is desireble compared to normal MAPE that
    may be undetermined when the target is zero.

    $$ \mathrm{sMAPE}_{2}(\\mathbf{y}_{\\tau}, \\mathbf{\hat{y}}_{\\tau}) =
       \\frac{1}{H} \\sum^{t+H}_{\\tau=t+1}
       \\frac{|y_{\\tau}-\hat{y}_{\\tau}|}{|y_{\\tau}|+|\hat{y}_{\\tau}|} $$

        Parameters
        ----------
        y: tensor (batch_size, output_size).
            Actual values in torch tensor.
        y_hat: tensor (batch_size, output_size).
            Predicted values in torch tensor.
        mask: tensor (batch_size, output_size).
            Specifies date stamps per serie
            to consider in loss.

        Returns
        -------
        smape: tensor (single value).
            Symmetric mean absolute percentage error.
    """
    if mask is None: mask = t.ones_like(y_hat)

    delta_y = t.abs((y - y_hat))
    scale = t.abs(y) + t.abs(y_hat)
    smape = _divide_no_nan(delta_y, scale)
    smape = smape * mask
    smape = 2 * t.mean(smape)
    return smape

# Cell
def MASELoss(y, y_hat, y_insample, seasonality, mask=None) -> t.Tensor:
    """

    Calculates the Mean Absolute Scaled Error (MASE) between
    y and y_hat. MASE measures the relative prediction
    accuracy of a forecasting method by comparinng the mean absolute errors
    of the prediction and the observed value against the mean
    absolute errors of the seasonal naive model.
    The MASE partially composed the Overall Weighted Average (OWA),
    used in the M4 Competition.

    $$ \mathrm{MASE}(\\mathbf{y}_{\\tau}, \\mathbf{\hat{y}}_{\\tau}, \\mathbf{\hat{y}}^{season}_{\\tau}) =
        \\frac{1}{H} \sum^{t+H}_{\\tau=t+1} \\frac{|y_{\\tau}-\hat{y}_{\\tau}|}{\mathrm{MAE}(\\mathbf{y}_{\\tau}, \\mathbf{\hat{y}}^{season}_{\\tau})} $$

        Parameters
        ----------
        y: tensor (batch_size, output_size).
            Actual values in torch tensor.
        y_hat: tensor (batch_size, output_size).
            Predicted values in torch tensor.
        y_insample: tensor (batch_size, input_size).
            Actual insample Seasonal Naive predictions.
        seasonality: int.
            Main frequency of the time series;
            Hourly 24,  Daily 7, Weekly 52,
            Monthly 12, Quarterly 4, Yearly 1.
        mask: tensor (batch_size, output_size).
            Specifies date stamps per serie
            to consider in loss.

        Returns
        -------
        mase: tensor (single value).
            Mean absolute scaled error.

        References
        ----------
        [1] https://robjhyndman.com/papers/mase.pdf
    """
    if mask is None: mask = t.ones_like(y_hat)

    delta_y = t.abs(y - y_hat)
    scale = t.mean(t.abs(y_insample[:, seasonality:] - \
                            y_insample[:, :-seasonality]), axis=1)
    mase = _divide_no_nan(delta_y, scale[:, None])
    mase = mase * mask
    mase = t.mean(mase)
    return mase

# Cell
def QuantileLoss(y, y_hat, mask=None, q=0.5) -> t.Tensor:
    """

    Computes the quantile loss (QL) between y and y_hat.
    QL measures the deviation of a quantile forecast.
    By weighting the absolute deviation in a non symmetric way, the
    loss pays more attention to under or over estimation.
    A common value for q is 0.5 for the deviation from the median (Pinball loss).

    $$ \mathrm{QL}(\\mathbf{y}_{\\tau}, \\mathbf{\hat{y}}^{(q)}_{\\tau}) =
        \\frac{1}{H} \\sum^{t+H}_{\\tau=t+1}
        \Big( (1-q)\,( \hat{y}^{(q)}_{\\tau} - y_{\\tau} )_{+}
        + q\,( y_{\\tau} - \hat{y}^{(q)}_{\\tau} )_{+} \Big) $$

        Parameters
        ----------
        y: tensor (batch_size, output_size).
            Actual values in torch tensor.
        y_hat: tensor (batch_size, output_size).
            Predicted values in torch tensor.
        mask: tensor (batch_size, output_size).
            Specifies date stamps per serie
            to consider in loss.
        q: float, between 0 and 1.
            The slope of the quantile loss, in the context of
            quantile regression, the q determines the conditional
            quantile level.

        Returns
        -------
        quantile_loss: tensor (single value).
            Average quantile loss.
    """
    if mask is None: mask = t.ones_like(y_hat)

    delta_y = t.sub(y, y_hat)
    loss = t.max(t.mul(q, delta_y), t.mul((q - 1), delta_y))
    loss = loss * mask
    quantile_loss = t.mean(loss)
    return quantile_loss

# Cell
def MQLoss(y, y_hat, quantiles, mask=None) -> t.Tensor:
    """

    Calculates the Multi-Quantile loss (MQL) between y and y_hat.
    MQL calculates the average multi-quantile Loss for
    a given set of quantiles, based on the absolute
    difference between predicted quantiles and observed values.

    $$ \mathrm{MQL}(\\mathbf{y}_{\\tau},
                    [\\mathbf{\hat{y}}^{(q_{1})}_{\\tau}, ... ,\hat{y}^{(q_{n})}_{\\tau}]) =
       \\frac{1}{n} \\sum_{q_{i}} \mathrm{QL}(\\mathbf{y}_{\\tau}, \\mathbf{\hat{y}}^{(q_{i})}_{\\tau}) $$

    The limit behavior of MQL allows to measure the accuracy
    of a full predictive distribution $\mathbf{\hat{F}}_{\\tau}$ with
    the continuous ranked probability score (CRPS). This can be achieved
    through a numerical integration technique, that discretizes the quantiles
    and treats the CRPS integral with a left Riemann approximation, averaging over
    uniformly distanced quantiles.

    $$ \mathrm{CRPS}(y_{\\tau}, \mathbf{\hat{F}}_{\\tau}) =
        \int^{1}_{0} \mathrm{QL}(y_{\\tau}, \hat{y}^{(q)}_{\\tau}) dq $$

        Parameters
        ----------
        y: tensor (batch_size, output_size).
            Actual values in torch tensor.
        y_hat: tensor (batch_size, output_size).
            Predicted values in torch tensor.
        mask: tensor (batch_size, output_size).
            Specifies date stamps per serie to consider in loss.
        quantiles: tensor(n_quantiles).
            Quantiles to estimate from the distribution of y.

        Returns
        -------
        mqloss: tensor(n_quantiles).
            Average multi-quantile loss.

        References
        ----------
        [1] https://www.jstor.org/stable/2629907
    """
    assert len(quantiles) > 1, f'your quantiles are of len: {len(quantiles)}'

    if mask is None: mask = t.ones_like(y_hat)

    n_q = len(quantiles)

    error = y_hat - y.unsqueeze(-1)
    sq = t.maximum(-error, t.zeros_like(error))
    s1_q = t.maximum(error, t.zeros_like(error))
    mqloss = (quantiles * sq + (1 - quantiles) * s1_q)

    return t.mean(t.mean(mqloss, axis=1))

# Cell
def wMQLoss(y, y_hat, quantiles, mask=None) -> t.Tensor:
    """

    Calculates the Weighted Multi-Quantile loss (WMQL) between y and y_hat.
    WMQL calculates the weighted average multi-quantile Loss for
    a given set of quantiles, based on the absolute
    difference between predicted quantiles and observed values.

    $$ \mathrm{WMQL}(\\mathbf{y}_{\\tau},
                    [\\mathbf{\hat{y}}^{(q_{1})}_{\\tau}, ... ,\hat{y}^{(q_{n})}_{\\tau}]) =
       \\frac{1}{n} \\sum_{q_{i}}
           \\frac{\mathrm{QL}(\\mathbf{y}_{\\tau}, \\mathbf{\hat{y}}^{(q_{i})}_{\\tau})}
            {\\sum^{t+H}_{\\tau=t+1} |y_{\\tau}|} $$

        Parameters
        ----------
        y: tensor (batch_size, output_size).
            Actual values in torch tensor.
        y_hat: tensor (batch_size, output_size).
            Predicted values in torch tensor.
        mask: tensor (batch_size, output_size).
            Specifies date stamps per serie to consider in loss.
        quantiles: tensor(n_quantiles).
            Quantiles to estimate from the distribution of y.

        Returns
        -------
        wmqloss: tensor(n_quantiles).
            Weighted average multi-quantile loss.
    """
    assert len(quantiles) > 1, f'your quantiles are of len: {len(quantiles)}'

    if mask is None: mask = t.ones_like(y_hat)

    n_q = len(quantiles)

    error = y_hat - y.unsqueeze(-1)

    sq = t.maximum(-error, t.zeros_like(error))
    s1_q = t.maximum(error, t.zeros_like(error))
    loss = (quantiles * sq + (1 - quantiles) * s1_q)

    wmqloss = _divide_no_nan(t.sum(loss * mask, axis=-2),
                          t.sum(t.abs(y.unsqueeze(-1)) * mask, axis=-2))

    return t.mean(wmqloss)

# Cell
def LevelVariabilityLoss(levels, level_variability_penalty) -> t.Tensor:
    """
    Computes the variability penalty for the level of the ES-RNN.
    The levels of the ES-RNN are based on the Holt-Winters model.

    $$  Penalty = \lambda * (\hat{l}_{τ+1}-\hat{l}_{τ})^{2} $$

        Parameters
        ----------
        levels: tensor with shape (batch, n_time).
            Levels obtained from exponential smoothing component of ESRNN.
        level_variability_penalty: float.
            This parameter controls the strength of the penalization
            to the wigglines of the level vector, induces smoothness
            in the output.

        Returns
        ----------
        level_var_loss: tensor (single value).
            Wiggliness loss for the level vector.
    """
    assert levels.shape[1] > 2
    level_prev = t.log(levels[:, :-1])
    level_next = t.log(levels[:, 1:])
    log_diff_of_levels = t.sub(level_prev, level_next)

    log_diff_prev = log_diff_of_levels[:, :-1]
    log_diff_next = log_diff_of_levels[:, 1:]
    diff = t.sub(log_diff_prev, log_diff_next)
    level_var_loss = diff**2
    level_var_loss = level_var_loss.mean() * level_variability_penalty

    return level_var_loss

# Cell
def SmylLoss(y, y_hat, levels, mask, tau, level_variability_penalty=0.0) -> t.Tensor:
    """

    Computes the Smyl Loss that combines level
    variability regularization with with Quantile loss.

        Parameters
        ----------
        windows_y: tensor (n_windows, batch_size, window_size).
            Actual values .
        windows_y_hat: tensor (n_windows, batch_size, window_size).
            Predicted values.
        levels: tensor (batch, n_time).
            Levels obtained from exponential smoothing component of ESRNN.


        Returns
        ----------
        smyl_loss: tensor (single value).
            Smyl loss.
    """

    if mask is None: mask = t.ones_like(y_hat)

    smyl_loss = QuantileLoss(y, y_hat, mask, tau)

    if level_variability_penalty > 0:
        log_diff_of_levels = LevelVariabilityLoss(levels, level_variability_penalty)
        smyl_loss += log_diff_of_levels

    return smyl_loss