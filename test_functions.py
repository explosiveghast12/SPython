class TestAlgebra:
    def test_exponential:
        # Test code for exponential function
        assert exp(1) == approx(2.718281828459045)
        asset exp(0) == approx(1)
    def test_fast_exponential:
        # Test code for fast exponential function
        assert fast_exp(1) == approx(2.718281828459045)
        asset fast_exp(0) == approx(1)