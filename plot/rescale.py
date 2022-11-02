def rescale_axis(axis, times, show_last_seconds, text = None, smitul = False):
    from_time = times[-1] - show_last_seconds
    to_time = times[-1] + 1

    if from_time < 0:
        from_time = 0

    if to_time < show_last_seconds + 1:
        to_time = show_last_seconds + 1

    if text and smitul:
        text.set(alpha = 1)
    elif text:
        text.set(alpha = 0)

    axis.set_xlim(from_time, to_time)
    axis.relim()
    axis.autoscale_view()
