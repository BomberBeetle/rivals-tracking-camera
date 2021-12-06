import numpy as np
cimport numpy as np
np.import_array()

cpdef np.ndarray filter_points_and_apply_threshold(points: np.ndarray, thresh_decay: float):

    print(thresh_decay)

    cdef np.ndarray points_threshd = np.copy(points)

    for i in reversed(range(points.shape[0])):
        points_threshd[i][2] -= thresh_decay
        if points_threshd[i][2] <= 0:
            points_threshd = np.delete(points_threshd, i, axis=0)

    return points_threshd
