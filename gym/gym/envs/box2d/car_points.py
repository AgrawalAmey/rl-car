import matplotlib.pyplot as plt

WHEELPOS = [
    (-55,+80), (+55,+80),
    (-55,-82), (+55,-82)
]

x = [i[0] for i in WHEELPOS]
y = [i[1] for i in WHEELPOS]

plt.scatter(x, y, c="b")

HULL_POLY1 =[
    (-60,+130), (+60,+130),
    (+60,+110), (-60,+110)
    ]

x = [i[0] for i in HULL_POLY1]
y = [i[1] for i in HULL_POLY1]

plt.scatter(x, y, c="r")

HULL_POLY2 =[
    (-15,+120), (+15,+120),
    (+20, +20), (-20,  20)
    ]

x = [i[0] for i in HULL_POLY2]
y = [i[1] for i in HULL_POLY2]

plt.scatter(x, y, c="r")

HULL_POLY3 =[
    (+25, +20),
    (+50, -10),
    (+50, -40),
    (+20, -90),
    (-20, -90),
    (-50, -40),
    (-50, -10),
    (-25, +20)
    ]

HULL_POLY4 =[
    (-50,-120), (+50,-120),
    (+50,-90),  (-50,-90)
    ]

x = [i[0] for i in HULL_POLY3]
y = [i[1] for i in HULL_POLY3]

plt.scatter(x, y, c="r")

x = [i[0] for i in HULL_POLY4]
y = [i[1] for i in HULL_POLY4]

plt.scatter(x, y, c="r")

# Six points starting from -40
IR_ARRAY = [(-60 + 24 * x, +130) for x in range(6)]

x = [i[0] for i in IR_ARRAY]
y = [i[1] for i in IR_ARRAY]

plt.scatter(x, y, c="g")

plt.show()
