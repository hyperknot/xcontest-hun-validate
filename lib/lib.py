def interval_intersection(start1, end1, start2, end2):
    """
    Find the intersection of two intervals.

    :param start1: Starting point of the first interval.
    :param end1: Ending point of the first interval.
    :param start2: Starting point of the second interval.
    :param end2: Ending point of the second interval.
    :return: A tuple representing the intersection of the two intervals or None if there is no intersection.
    """

    if end1 < start2 or end2 < start1:
        return None
    else:
        return max(start1, start2), min(end1, end2)
