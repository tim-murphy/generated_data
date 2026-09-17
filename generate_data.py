# Data generation for the 2026 minisclerals student project.
# Note: these data are used to generate a synthetic dataset for use in this
#       project with the understanding that it will /not/ be claimed as real
#       participant data, and will not be presented or published.
# Written by Tim Murphy <tim.murphy@canberra.edu.au> 2026.

import argparse
import numpy as np
import sympy

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--formula", type=str, default="x",
                        help="Data trend formula containing up to one 'x' (e.g. \"x**2+1\")")
    parser.add_argument("--min", type=float, default=0.0,
                        help="Minimum x value")
    parser.add_argument("--max", type=float, default=10.0,
                        help="Maximum x value")
    parser.add_argument("--step", type=float, default=1.0,
                        help="x value step size")
    parser.add_argument("--noise_sd", type=float, default=1.0,
                        help="Add noise to the data with this standard deviation")
    parser.add_argument("--round", type=float, required=False,
                        help="If set, will round values to this number")
    parser.add_argument("--separator", type=str, default="\n",
                        help="String printed between values (defaults to newline)")
    parser.add_argument("--repeats", type=int, default=1,
                        help="Number of times to generate the sequence, separated by a newline")
    parser.add_argument("--variability", type=float, default=2.0,
                        help="Standard deviation of variance between repeats")
    parser.add_argument("--measures", type=int, default=1,
                        help="Number of measures for each measurement event (default 1)")
    args = parser.parse_args()

    # Validate command-line arguments.
    if args.min > args.max:
        raise ValueError("Min x value must be less than max x value!")

    num_steps = (args.max - args.min) / args.step
    if num_steps % 1.0 != 0.0:
        raise ValueError("Step size does not fit evenly between min and max!")
    num_steps = int(num_steps) + 1

    # Generate the values.
    calc_fn = sympy.lambdify(sympy.symbols('x'),
                             sympy.parse_expr(args.formula))

    variability = np.random.normal(0.0, args.variability, args.repeats)

    for rep in range(args.repeats):
        noise = np.random.normal(0.0, args.noise_sd, num_steps * args.measures)
        y_vals = []
        for s in range(num_steps):
            x = args.min + (s * args.step)
            y = calc_fn(x) + variability[rep]

            for m in range(args.measures):
                y_val = y +  + noise[s * args.measures + m]

                if args.round is not None:
                    y_val = round(y_val / args.round) * args.round

                y_vals.append(y_val)

        print(*y_vals, sep=args.separator)

# EOF