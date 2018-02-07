import numpy as np

def banded(Aa, va, up, down):
	# This is copied from the Computational Physics book
	# and it doesn't seem to work quite right
	A = np.copy(Aa)
	v = np.copy(va)
	N = len(v)
	
	# Gaussian elimination
	for m in range(N):
		
		# Normalization factor
		div = A[up,m]
		
		# Update the vector first
		v[m] /= div
		for k in range(1, down+1):
			if m+k < N:
				v[m+k] -= A[up+k,m] * v[m]
			
		# Normalize and subtract the pivot row
		for i in range(up):
			j = m + up - i
			if j<N:
				A[i,j] /= div
				for k in range(1,down+1):
					A[i+k,j] -= A[up+k,m]*A[i,j]
		

		for m in range(N-2,-1,-1):
			for i in range(up):
				j = m + up - i
				if j<N:
					v[m] -=A[i,j]*v[j]
		print(A)
	return v

def gauss_elim(Aa, va):
	
	A = np.copy(Aa)
	v = np.copy(va)
	N = len(v)
	
	for m in range(N):
		
		# pivot the rows
		# find the row with the largest initial element
		maxval = np.copy(A[m,m])
		for i in range(m,N,1):
			# This should be the element in the rows
			# under the current diagonal element
			firstval = A[i,m]
			if abs(firstval) > maxval:
				maxval = firstval
				pivotrow = i
		
		# swap with current row
		temp = np.copy(A[m])
		A[m] = A[pivotrow]
		A[pivotrow] = temp
		temp = np.copy(v[m])
		v[m] = v[pivotrow]
		v[pivotrow] = temp
		
		#normalize current row
		v[m] /= A[m,m]
		A[m] /= A[m,m]
		
		for i in range(m+1, N, 1):
			multiplier = A[i,m]
			v[i] -= multiplier*v[m]
			A[i] -= multiplier*A[m]
	
	# Backsubstitution
	x = np.empty_like(v)
	for i in range(N-1,-1,-1):
		# remember that range goes until one before the end
		# i.e. has bounds like [,)
		x[i] = v[i]
		for j in range(i+1, N):
			x[i] -= A[i,j]*x[j]
	
	return x
		
def tridiag_solve(Aa, va):
	A = np.copy(Aa)
	v = np.copy(va)
	N = len(v)
	# Check that sizes are the same
	if N != len(A):
		print("Matrix:",A.shape,"and vector",v.shape," aren't same dimension")
		
	for m in range(N):
		
		# normalize current row
		v[m] /= A[m,m]
		A[m] /= A[m,m]
		
		# subtract from next row
		if m < N-1:
			multiplier = A[m+1,m]
			v[m+1] -= multiplier*v[m]
			A[m+1] -= multiplier*A[m]
		
	# Backsubstitution
	x = np.empty_like(v)
	for i in range(N-1,-1,-1):
		# remember that range goes until one before the end
		# i.e. has bounds like [,)
		x[i] = v[i]
		if i < N-1:
			x[i] -= A[i,i+1]*x[i+1]
	
	return x
