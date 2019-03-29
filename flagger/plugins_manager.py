from pkg_resources import iter_entry_points

steps = {
    entry_point.name: entry_point.load()
    for entry_point in iter_entry_points('flagger.steps')
}
