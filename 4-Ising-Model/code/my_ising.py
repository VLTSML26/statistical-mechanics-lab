import numpy as np

class myIsing:

    def __init__(self, N=100, T=2.269185314213022, H=0., J=1.):
        """
        CONSTRUCTOR:
        generate random spin-lattice
        #
        initialize constants
        """
        self.lattice = np.random.randint(0, 2, (N, N))*2-1
        #
        self.N = N
        self.T = T
        self.H = H
        self.J = J
        
    def Metropolis(self):
        """
        METROPOLIS ALGORITHM's SINGLE UPDATE:
        set beta
        #
        choose a random site (i,j)
        s = spin_value of site (i,j)
        #
        compute energy cost of flip:
        contributes = [spin values of nearest neighbors]
        delta_E = theoretical energy cost (if flip happens)
        effDelta_E = actual energy cost = 0
        will update effDelta_E later
        #
        metropolis step:
        if(Delta_E < 0)
            flip the spin with prob = 1
            set effDelta_E to theoretical value
        else
            flip the spin with prob = exp(-beta*Delta_E)
            if(flip happens)
                effDelta_E to theoretical value
        #
        update lattice configuration (in-place)
        #
        return the effective DeltaE
        notice that if we didn't flip the spin, the change in energy is 0
        """
        beta = 1 / self.T
        #
        i = np.random.randint(0, self.N)
        j = np.random.randint(0, self.N)
        s = self.lattice[i][j]
        #
        contributes = [ self.lattice[(i+1) % self.N][j     % self.N],
                        self.lattice[(i-1) % self.N][j     % self.N],
                        self.lattice[i     % self.N][(j+1) % self.N],
                        self.lattice[i     % self.N][(j-1) % self.N] ]
        Delta_E = s * self.J * np.sum(np.asarray(contributes)) + self.H * s
        Delta_E *= 2
        effDelta_E = 0
        #
        if(Delta_E < 0):
            s *= -1
            effDelta_E = Delta_E
        else:
            if(np.random.rand() < np.exp(-beta * Delta_E)):
                s *= -1
                effDelta_E = Delta_E
        #
        self.lattice[i][j] = s
        #
        return effDelta_E
    
    def Gibbs(self):
        """
        GIBBS ALGORITHM's SINGLE UPDATE:
        set beta
        #
        choose a random site (i,j)
        s = +1
        #
        compute energy cost E_up for s = +1 (up):
        contributes = [spin values of nearest neighbors]
        E_up = theoretical energy cost (if s = +1)
        x = Gibbs probability for s down
        #
        gibbs step:
        set s = -1 with probability exp(-beta*E_up)
        #
        update lattice configuration (in-place)
        #
        return
        """
        beta = 1 / self.T
        #
        i = np.random.randint(0, self.N)
        j = np.random.randint(0, self.N)
        s = 1.
        #
        contributes = [ self.lattice[(i+1) % self.N][j     % self.N],
                        self.lattice[(i-1) % self.N][j     % self.N],
                        self.lattice[i     % self.N][(j+1) % self.N],
                        self.lattice[i     % self.N][(j-1) % self.N] ]
        E_up = s * self.J * np.sum(np.asarray(contributes)) + self.H * s
        E_up *= 2
        x = 1. / (1. + np.exp(-beta * E_up))
        #
        if(np.random.rand() > x):
            s = -1.
        #
        self.lattice[i][j] = s
        #
        return
    
    def GetEnergy(self):
        """
        ENERGY OF THE ACTUAL SPIN CONFIGURATION:
        generate list of pairs of adjacent sites as four-element tuples
        (i1, j1, i2, j2) represents two adjacent sites located at (i1, j1) and (i2, j2)
        #
        concatenate lists
        #
        sum over all neighboring spins to get the total energy
        #
        return energy
        """
        horizontal_edges = [
            (i, j, i, (j+1) % self.N)
            for i in range(self.N) for j in range(self.N)
        ]
        vertical_edges = [
            (i, j, (i+1) % self.N, j)
            for i in range(self.N) for j in range(self.N)
        ]
        #
        edges = horizontal_edges + vertical_edges
        #
        E = 0
        for i1, j1, i2, j2 in edges:
            E -= self.lattice[i1][j1] * self.lattice[i2][j2]
        #
        return E