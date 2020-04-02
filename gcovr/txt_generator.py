# -*- coding:utf-8 -*-

# This file is part of gcovr <http://gcovr.com/>.
#
# Copyright 2013-2018 the gcovr authors
# Copyright 2013 Sandia Corporation
# This software is distributed under the BSD license.

import sys

from .utils import calculate_coverage, sort_coverage, presentable_filename


def print_text_report(covdata, output_file, options):
    """produce the classic gcovr text report"""
    if output_file:
        with open(output_file, 'w') as fh:
            _real_print_text_report(covdata, fh, options)
    else:
        _real_print_text_report(covdata, sys.stdout, options)


def _real_print_text_report(covdata, OUTPUT, options):
    total_lines = 0
    total_covered = 0

    width = 78
    filename_width = 54

    # Header
    OUTPUT.write("-" * width + '\n')
    OUTPUT.write(" " * 27 + "GCC Code Coverage Report\n")
    OUTPUT.write("Directory: " + options.root + "\n")

    OUTPUT.write("-" * width + '\n')
    a = options.show_branch and "Branches" or "Lines"
    b = options.show_branch and "Taken" or "Exec"
    OUTPUT.write(
        "File".ljust(filename_width) + a.rjust(8) + b.rjust(8) + "  Cover   \n"
    )
    OUTPUT.write("-" * width + '\n')

    # Data
    keys = sort_coverage(
        covdata, show_branch=options.show_branch,
        by_num_uncovered=options.sort_uncovered,
        by_percent_uncovered=options.sort_percent)

    def _summarize_file_coverage(coverage):
        filename = presentable_filename(
            coverage.filename, root_filter=options.root_filter)
        filename = filename.ljust(filename_width)
        if len(filename) > filename_width:
            filename = filename + "\n" + " " * filename_width

        if options.show_branch:
            total, cover, percent = coverage.branch_coverage()
            uncovered_lines = coverage.uncovered_branches_str()
        else:
            total, cover, percent = coverage.line_coverage()
            uncovered_lines = coverage.uncovered_lines_str()
        percent = '--' if percent is None else str(int(percent))
        return (total, cover,
                filename + str(total).rjust(8) + str(cover).rjust(8)
                + percent.rjust(6) + "%")

    for key in keys:
        (t, n, txt) = _summarize_file_coverage(covdata[key])
        total_lines += t
        total_covered += n
        OUTPUT.write(txt + '\n')

    # Footer & summary
    OUTPUT.write("-" * width + '\n')
    percent = calculate_coverage(total_covered, total_lines, nan_value=None)
    percent = "--" if percent is None else str(int(percent))
    OUTPUT.write(
        "TOTAL".ljust(filename_width) + str(total_lines).rjust(8)
        + str(total_covered).rjust(8) + str(percent).rjust(6) + "%" + '\n'
    )
    OUTPUT.write("-" * width + '\n')
