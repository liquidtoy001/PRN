# Three short source cards for a revision session

These independent teaching and assessment examples are original practice material.

## Card A · Choosing a reading for one target

A translator is about to produce a target word. Its current decoder state supplies query
q = (1,2). Two source positions supply keys (2,0) and (0,2), and scalar values 5 and 9,
respectively. For each key the score is the dot product with q divided by the square root
of the key dimension. Apply softmax across the candidate source positions and sum the
values with those weights. Subtracting a common constant from the scores before softmax
preserves the weights. Subtracting the largest score helps avoid overflow.

Practice A. Write the two scaled scores and explain what the larger score means here.

## Card B · Choosing a continuation estimate

A cart moves between bays. After an observed move it receives 1 unit of reward and reaches
a nonterminal fork. The current entry for that move is 2. At the fork the old action
values are 4 for straight and 0 for turn. Exploration chooses turn. Use discount 0.5 and
learning rate 0.5. An update moves the current entry towards reward plus discounted
continuation by the learning rate. Q-learning reads the largest legal continuation value.
SARSA reads the value of the action actually chosen. A terminal outcome has zero continuation.

Practice B. Calculate both updated entries. Explain when the two updates would agree.

## Card C · Counting two direct computations

A length-N discrete Fourier transform gives N frequency coefficients. Each coefficient
sums one term per sample. A full linear convolution of a length-N signal with a length-M
kernel includes every input/kernel pair once across all output positions. A direct
implementation skips zero-extension products. FFT-based convolution can use a common
transform length of at least N+M-1 to avoid wrap-around.

Practice C1. For 8 samples, how many sample terms enter a direct DFT across all bins?
Explain where the two factors come from.

Practice C2. For the same 8 samples and a length-3 kernel, count direct full-convolution
products. Give the minimum transform length if this convolution is performed with FFTs.
