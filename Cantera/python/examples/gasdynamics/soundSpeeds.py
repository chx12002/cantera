from Cantera import *
import math

def equilSoundSpeeds(gas):

    """Returns the equilibrium and frozen sound speeds for a gas.  The
    gas is first set to an equilibrium state, since otherwise the
    equilibrium sound speed is not defined. Therefore, both sound
    speeds are for a gas with an equilibrium composition - not the
    composition of the gas object on entry."""

    # set the gas to equilibrium at its current T and P
    gas.equilibrate('TP')

    # save properties
    s0 = gas.entropy_mass()
    p0 = gas.pressure()
    r0 = gas.density()

    # perturb density
    r1 = r0*1.0001

    # set the gas to a state with the same entropy and composition but
    # the perturbed density
    gas.setState_SV(s0, 1.0/r1)

    # save the pressure for this case for the frozen sound speed
    pfrozen = gas.pressure()
    
    # now equilibrate the gas holding S and V constant
    gas.equilibrate("SV")

    p1 = gas.pressure()

    aequil = math.sqrt((p1 - p0)/(r1 - r0));
    afrozen = math.sqrt((pfrozen - p0)/(r1 - r0));    
    return (aequil, afrozen)


# test program
if __name__ == "__main__":
    
    gas = GRI30()
    gas.set(X = 'CH4:0.1.1, O2:2.0, N2:3.76')
    for n in range(27):
        temp = 300.0 + n*100.0
        gas.set(T = temp, P = OneAtm)
        print temp, equilSoundSpeeds(gas)

    
