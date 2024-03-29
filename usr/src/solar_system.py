#!/usr/bin/env python
import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from datetime import datetime, timedelta

class Object:                
    def __init__(self, name, rad, color, r, v):
        self.name = name
        self.r    = np.array(r, dtype=float)
        self.v    = np.array(v, dtype=float)
        self.xs = []
        self.ys = []
        self.plot = plt.scatter(r[0], r[1], color=color, s=rad**2, edgecolors='w', zorder=10)
        self.line, = plt.plot([], [], color=color, linewidth=1.4)

class SolarSystem:
    def __init__(self, thesun):
        self.thesun = thesun
        self.planets = []
        self.time = None
        self.timestamp = plt.text(.03, .94, 'Fecha: ', color='w', transform=plt.gca().transAxes, fontsize='x-large')
    def add_planet(self, planet):
        self.planets.append(planet)
    def evolve(self):
        dt = 1
        self.time += timedelta(dt)
        plots = []
        lines = []
        for i, p in enumerate(self.planets):
            p.r += p.v * dt
            acc = -2.959e-4 * p.r / np.sum(p.r**2)**(3./2)
            p.v += acc * dt
            p.xs.append(p.r[0])
            p.ys.append(p.r[1])
            p.plot.set_offsets(p.r[:2])
            plots.append(p.plot)
            p.line.set_xdata(p.xs)
            p.line.set_ydata(p.ys)
            lines.append(p.line)
        if len(p.xs) > 10000:
            raise SystemExit("Overflow de memoria maquina")
        self.timestamp.set_text('Fecha: {}'.format(self.time.isoformat()))
        return plots + lines + [self.timestamp]

def main(save=False):
    plt.style.use('dark_background')
    fig = plt.figure(figsize=[8, 8])
    ax = plt.axes([0., 0., 1., 1.], xlim=(-1.8, 1.8), ylim=(-1.8, 1.8))
    ax.set_facecolor('#060606')  # Dark background
    ax.set_aspect('equal')
    ax.axis('off')

    with open("planetas.json", 'r') as f:
        planets = json.load(f)

    ss = SolarSystem(Object("Solamen", 28, 'yellow', [0, 0, 0], [0, 0, 0]))
    ss.time = datetime.strptime(planets["date"], '%Y-%m-%d').date()

    colors = ['#FFD700', '#4CAF50', '#2196F3', '#FF5722']  # Sun, Earth, Mars, Venus
    texty = [.47, .73, 1, 1.5]

    for i, nasaid in enumerate([1, 2, 3, 4]):
        planet = planets[str(nasaid)]
        ss.add_planet(Object(nasaid, 20 * planet["size"], colors[i], planet["r"], planet["v"]))
        ax.text(0, - (texty[i] + 0.1), planet["name"], color=colors[i], zorder=1000, ha='center', fontsize='large')

    def animate(i):
        return ss.evolve()

    sim_duration = 2 * 365              
    ani = animation.FuncAnimation(fig, animate, repeat=False, frames=sim_duration, blit=True, interval=20,)

    if save:
        ani.save('sistema_solar.mp4', fps=75, dpi=150)
    else:
        plt.show()

main(save=False)
