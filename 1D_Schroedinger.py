import numpy as np
import matrix_solvers as ms
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import math

component_plot = False
initial_condition = 'Gaussian'
potential_shape = 'Harmonic Oscillator'

mass = 9.109e-31 #MeV/c^2
hbar = 1.054e-34 # J*s
k = 5e10 # wavenumber (m^-1)

# Create grid
L = 1e-8 # meters
N = 1000 # Number of grid points
dt = 1e-18 # seconds
tf = 5e-15 # seconds
times = np.arange(0, tf+dt, dt)
dx = L/(N-1)
x = np.linspace(0, L, N)

# Initial condition
def f(x):
	N = len(x)
	y = np.zeros(len(x), dtype='complex')
	
	if initial_condition == 'Gaussian':
		temp = np.exp(-(x-L/5)**2/(2*1e-9**2))
		y = 2*(temp-temp[0])*np.exp(1j*k*x)
		y[400:] = 0
	
	if initial_condition == 'Triangle wave':	
		for i in range(N):
			y[i] = 2/10*(x[i] - 10*math.floor(x[i]/10+0.5))*(-1)**math.floor(x[i]/10+0.5)
		y *= np.exp(1j*k*x)
	
	if initial_condition == 'Delta Function':
		y[700] = 1/dx
	
	return y

# Potential function
def potential(x):
	V = np.zeros_like(x)
	
	if potential_shape == 'Harmonic Oscillator':
		for i in range(len(x)):
			V[i] = 5*(x[i] - L/2)**2
	if potential_shape == 'Step Function':
		for i in range(len(x)):
			if i > len(x)/2:
				V[i] = 0.75*(hbar*k)**2/(2*mass)
	return V

# Set the initial condition
Psi = [f(x)]
Psi[0][0], Psi[0][-1] = 0, 0 # Infinite well means 0 at boundary

# Define reused constants
a1 = 1 + dt*1j*hbar/(2*mass*dx**2)
a2 = -dt*1j*hbar/(4*mass*dx**2)
b1 = 1 - dt*1j*hbar/(2*mass*dx**2)
b2 = dt*1j*hbar/(4*mass*dx**2)

# Create matrices for calculation
A = np.zeros([N-2,N-2],dtype='complex')
B = np.zeros_like(A)
for i in range(N-2):
	# Set diagonal elements
	A[i,i] = a1 - dt/(2j*hbar)*potential(x)[i]
	B[i,i] = b1 + dt/(2j*hbar)*potential(x)[i]
	# Set off-diag elements
	if i < len(A)-1:
		A[i,i+1] = a2
		A[i+1,i] = a2
		B[i,i+1] = b2
		B[i+1,i] = b2

# Solve for new Psi iteratively (most of the program time is here)
for i in range(len(times)):
	old = np.dot(B,Psi[i][1:-1])
	new = ms.tridiag_solve(A,old)
	new_Psi = np.concatenate([[0],new,[0]])
	
	Psi.append(new_Psi)
	
	# Print out progress
	if not i % math.ceil(len(times)/100):
		print(int(round(i/len(times)*100,0)),"% complete")


# Animation stuff
# Probability density
if component_plot == True:
	fig, (ax1,ax2,ax3) = plt.subplots(3, 1, sharex=True)
if component_plot == False:
	fig, ax1 = plt.subplots(1, 1, sharex=True)
ax1.set_ylim(0,20)
ax1.set_xlim(0,L)
ax1.set_ylabel("Psi^2, probability density")
ax1.set_xlabel("x (meters)")
line1, = ax1.plot([], [], lw=2)
# Show potential
scaled_pot = potential(x)/potential(x).max()
ax1.plot(x,10*scaled_pot,linestyle='--',color='g')

if component_plot == True:
	# Real component
	ax2.set_ylim(-5,5)
	ax2.set_xlim(0,L)
	ax2.set_ylabel("Re(Psi)")
	ax2.set_xlabel("x (meters)")
	line2, = ax2.plot([], [], color='r', lw=2)
	#Imaginary component
	ax3.set_ylim(-5,5)
	ax3.set_xlim(0,L)
	ax3.set_ylabel("Im(Psi)")
	ax3.set_xlabel("x (meters)")
	line3, = ax3.plot([], [], color='g', lw=2)

def animate(i):
	line1.set_xdata(x)
	line1.set_ydata(abs(Psi[i*5])**2)
	
	if component_plot == True:
		line2.set_xdata(x)
		line3.set_xdata(x)
		line2.set_ydata(Psi[i].real)
		line3.set_ydata(Psi[i].imag)
		return line1, line2, line3,
	else:
		return line1,

# Might be easier to use ArtistAnimation
ani = animation.FuncAnimation(fig, animate, range(int(len(Psi)/5)), interval=10, blit=True, save_count=len(Psi))
plt.show()

# Set up formatting for the movie files
Writer = animation.writers['mencoder']
writer = Writer(fps=60, metadata=dict(artist='Liam Clink'), bitrate=1800)
ani.save('../Desktop/Solution.mp4', writer=writer)