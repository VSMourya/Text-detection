def union_boxes(box_a, box_b):
    """
    Merges two rectangles.
    Args:
        box_a  <tuple>  : First rectangle (x, y, w, h)
        box_b  <tuple>  : Second rectangle (x, y, w, h)

    Returns:
        merged_box  <tuple> : Merged rectangle (x, y, w, h)
    """

    ax1, ay1, aw, ah = box_a
    ax2, ay2 = ax1+aw-1, ay1+ah-1

    bx1, by1, bw, bh = box_b
    bx2, by2 = bx1+bw-1, by1+bh-1

    x1 = min(ax1, bx1)
    y1 = min(ay1, by1)
    x2 = max(ax2, bx2)
    y2 = max(ay2, by2)

    merged_box = [x1, y1, x2-x1+1, y2-y1+1]
    return merged_box


def intersects(box_a, box_b, grace, dynamic_grace):
    """
    Checks whether two rectangles intersect or inside in other.
    Args:
        box_a         <tuple>   : First rectangle (x, y, w, h)
        box_b         <tuple>   : Second rectangle (x, y, w, h)
        grace         <list>    : Relaxation for intersecting rectangles, [x_grace, y_grace]
        dynamic_grace <boolean> : Set True if using relaxation based on rectangle's height otherwise False

    Returns:
        <Boolean> : True if rectangles intersect or inside in other considering grace values otherwise False
    """

    ax1, ay1, aw, ah = box_a
    ax2, ay2 = ax1+aw-1, ay1+ah-1

    bx1, by1, bw, bh = box_b
    bx2, by2 = bx1+bw-1, by1+bh-1

    x_grace = y_grace = 0
    if dynamic_grace:
        x_grace = float(grace[0] * (ah+bh)/2)  # min(ah, bh)  # note: here height is used instead of width
        y_grace = float(grace[1] * min(ah, bh))

    x_grace = round(x_grace)
    y_grace = round(y_grace)

    if ax1-bx2 > x_grace or bx1-ax2 > x_grace or ay1-by2 > y_grace or by1-ay2 > y_grace:
        return False
    else:
        return True


def combine_boxes(boxes, grace, dynamic_grace):
    """
    Combines given list of rectangles as per specified grace configuration.
    Args:
        boxes         <list of tuples> : List of rectangles
        grace         <list>           : Relaxation for intersecting rectangles, [x_grace, y_grace]
        dynamic_grace <boolean>        : Set True if using relaxation based on rectangle's height otherwise False

    Returns:
        boxes <list of tuples> : List of merged rectangles
    """

    if not len(boxes):
        return boxes

    non_existant = [-120, -120, 0, 0]
    atleast_one_intersection = True

    while atleast_one_intersection:
        atleast_one_intersection = False

        for i, box_a in enumerate(boxes):
            if box_a[2] == 0:  # box_a[2] is width of box
                continue
            for j, box_b in enumerate(boxes):
                if j-i < 1 or box_b[2] == 0:  # box_b[2] is width of box
                    continue
                if intersects(box_a, box_b, grace, dynamic_grace):
                    new_box = union_boxes(box_a, box_b)
                    boxes.append(new_box)
                    boxes[i] = non_existant
                    boxes[j] = non_existant
                    atleast_one_intersection = True
                    break

        boxes = [list(x) for x in set(tuple(x) for x in boxes)]

    if non_existant in boxes:
        boxes.remove(non_existant)

    return boxes
