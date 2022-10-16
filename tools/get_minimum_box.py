def get_minimum_box(Qp):
    rows = Qp.shape[0]
    cols = Qp.shape[1]
    Q_corners = [Qp[0][0], Qp[0][cols-1], Qp[rows-1][0], Qp[rows-1][cols-1]]
    max_y = max([point[1] for point in Q_corners])
    min_y = min([point[1] for point in Q_corners])

    max_x = max([point[0] for point in Q_corners])
    min_x = min([point[0] for point in Q_corners])

    R0 = [min_x,max_y]
    R2 = [max_x,min_y]

    return R0, R2