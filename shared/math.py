def clamp(val, minval, maxval):
    return minval if val < minval \
      else maxval if val > maxval \
      else val
