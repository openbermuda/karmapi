BUILD_PATHS = {
    "year/{year}/{month}/{day}/{field}": build_day,
    "year/{year}/{month}/{field}": build_month,
    "year/{year}/{field}": build_year,

    "space/{lon}/{field}": not_yet_implemented,

    "total/{year}/{month}/{field}": not_yet_implemented,
    "total/{year}/{field}": not_yet_implemented,
    "baseline/{month}/{day}/{field}": not_yet_implemented,
}
