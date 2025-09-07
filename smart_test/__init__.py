"""smart-test - A tool for analyzing and generating tests for Python projects."""

__version__ = "0.1.0"

from .analyzer import (
    analyze_project,
    parse_coverage_xml,
    map_coverage_to_functions,
    summarize_coverage,
    generate_test_skeleton,
    FunctionInfo
)

from .utils import (
    iter_python_files,
    read_text,
    find_config_file,
    load_config,
    create_directory_if_not_exists,
    safe_write_file
)