module Taylor
export trueF

function trueF(x)
    # the real function to approximate
    return cos(1/x)
end

function firstOrderF(x, a::Float64)
    # first order approximation of trueF at a
    term1 = cos(1/a)
    term2 = -sin(1/a) - a^-2
    return term1 + term2
end

function firstOrderFCurry(a::Float64)
    # use currying to make plotting easy

    function firstOrderF(x)
        # first order approximation of trueF at a
        a0 = cos(1/a)
        a1 = -sin(1/a) * (-a^-2)
        return a0 + a1*(x - a)
    end
end

function zeroOrderFCurry(a::Float64)
    # use currying to make plotting easy

    function firstOrderF(x)
        # first order approximation of trueF at a
        term1 = cos(1/a)
        return term1
    end
end

end
