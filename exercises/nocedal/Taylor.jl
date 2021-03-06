module Taylor
export trueF

function trueF(x)
    # the real function to approximate
    return cos(1/x)
end

function zeroOrderFCurry(a::Float64)
    # A zeroth order approximation, using currying to make plotting easy
    function firstOrderF(x)
        # first order approximation of trueF at a
        term1 = cos(1/a)
        return term1
    end
end

function firstOrderFCurry(a::Float64)
    # A zeroth order approximation, using currying to make plotting easy
    function secondOrderF(x)
        # first order approximation of trueF at a
        a0 = cos(1/a)
        a1 = -sin(1/a) * (-a^-2)
        return a0 + a1*(x - a)
    end
end

function secondOrderFCurry(a::Float64)
    # A zeroth order approximation, using currying to make plotting easy
    function secondOrderF(x)
        # first order approximation of trueF at a
        a0 = cos(1/a)
        a1 = -sin(1/a) * (-a^-2)
        gprime = -a^-2
        fprimeprimegx = -cos(1/a)
        fprimegx = -sin(1/a)
        gprimeprime = 2 * (a^-3) 
        a2 = gprime * fprimeprimegx + fprimegx * gprimeprime
        
        # wolfram alpha
        a2 = 2*a*sin(1/a) + cos(1/a)
        return a0 + a1*(x - a) + (a2/4)*(x-a)^2
    end
end


end

# r = 2.5:.1:3.5
# plot(r, [Main.Taylor.trueF, Main.Taylor.zeroOrderFCurry(3.),Main.Taylor.firstOrderFCurry(3.),Main.Taylor.secondOrderFCurry(3.)], label=["true"  "0th" "1st" "2nd"])