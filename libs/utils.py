def collect_points(img, results):
    if results.pose_landmarks:
        points = {}
        for id, lm in enumerate(results.pose_landmarks.landmark):
            h, w, c = img.shape
            cx, cy = int(lm.x * w), int(lm.y * h)
            points[id] = (cx, cy)
    return points