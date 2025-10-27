import org.junit.Test;
import static org.junit.Assert.*;

/**
 * Tests unitaires pour Calculator
 */
public class CalculatorTest {

    @Test
    public void testAdd() {
        assertEquals(5, Calculator.add(2, 3));
        assertEquals(0, Calculator.add(0, 0));
        assertEquals(-1, Calculator.add(-3, 2));
    }

    @Test
    public void testSubtract() {
        assertEquals(1, Calculator.subtract(3, 2));
        assertEquals(0, Calculator.subtract(0, 0));
        assertEquals(-5, Calculator.subtract(-3, 2));
    }

    @Test
    public void testMultiply() {
        assertEquals(6, Calculator.multiply(2, 3));
        assertEquals(0, Calculator.multiply(0, 5));
        assertEquals(-6, Calculator.multiply(-3, 2));
    }

    @Test
    public void testDivide() {
        assertEquals(2, Calculator.divide(6, 3));
        assertEquals(5, Calculator.divide(10, 2));
        assertEquals(-2, Calculator.divide(-6, 3));
    }

    @Test(expected = ArithmeticException.class)
    public void testDivideByZero() {
        Calculator.divide(10, 0);
    }
}
