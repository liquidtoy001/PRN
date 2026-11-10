# Original fictional lecture — summaries of observations

## Arithmetic and weighted means

For real observations x_1 through x_n with n >= 1, the arithmetic mean is
sum(x_i)/n. All observations have equal weight. For nonnegative weights w_i whose sum is
positive, the weighted mean is sum(w_i*x_i)/sum(w_i). Individual weights may be zero.
The result has the observations' units. For x=(1,2,6) the arithmetic mean is 3.
With w=(1,1,2), the weighted mean is 15/4. The denominator is the sum of weights, not
automatically the number of observations.

## Updating a summary

The running arithmetic mean after n observations is m_n = m_(n-1) + (x_n-m_(n-1))/n
for n >= 2, initialised with m_1=x_1. It needs the old mean, current observation and count.
This is exactly the equal-weight arithmetic mean, computed incrementally.

An exponentially weighted moving average (EWMA) uses s_t = alpha*x_t+(1-alpha)*s_(t-1)
for t >= 2, with 0 < alpha <= 1, initialised here with s_1=x_1. Alpha is a chosen smoothing
parameter. Successive contributions from older observations are multiplied by 1-alpha.
The initial value also has a decaying contribution; do not claim all coefficients are
alpha*(1-alpha)^k under this initialisation. With alpha=1, the output is the current observation.
For (1,2,6), the running mean ends at 3; an EWMA with alpha=1/2 ends at 15/4.

Both procedures summarise sequential observations using a previous summary and a new value.
The running mean uses a count-dependent step and gives all observed values equal weight;
EWMA with fixed alpha favours recent values. A fixed-alpha EWMA generally differs from a
running mean. The benefit of smoothing alone is not a definition of either method.
